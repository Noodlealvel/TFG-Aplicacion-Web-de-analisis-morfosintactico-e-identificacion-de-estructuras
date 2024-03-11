from re import A
import os
from turtle import end_fill
from django.shortcuts import redirect, render
from django.http import FileResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.conf import settings
import benepar, spacy
import constituent_treelib as ct
#import constituent_treelib
nlp = spacy.load("en_core_web_sm")
if spacy.__version__.startswith('2'):
    nlp.add_pipe(benepar.BeneparComponent("benepar_en3"))
else:
    nlp.add_pipe("benepar", config={"model": "benepar_en3"})
#from nltk import pos_tag, word_tokenize
#from nltk.corpus import wordnet2021
#from nltk import CFG
#from nltk.ccg.chart import CCGChartParser
# Create your views here.
        
def home(request):
    if request.user.is_authenticated:
        return redirect("/analyze")
    else:
        return render (request, "cuentas/index.html")

def signup(request):

    if request.method=="POST":
        username= request.POST.get('username')
        firstname=request.POST.get('firstname')
        lastname=request.POST.get('lastname')
        email=request.POST.get('email')
        passwd=request.POST.get('passwd')
        passwd2=request.POST.get('passwd2')
        if (not username or not firstname or not lastname or not email or not passwd or not passwd2):
            messages.error(request, "All fields are required.")
            return redirect ("signup")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect ("signup")

        if User.objects.filter(email=email).exists():
            messages.error(request, "E-mail already has another account associated.")
            return redirect ("signup")
        
        if passwd!=passwd2:
            messages.error(request, "Passwords don't match.")
            return redirect ("signup")
        
        user = User.objects.create_user(username, email, passwd)
        user.first_name=firstname
        user.last_name=lastname

        user.save()

        parent_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static/images/")
        path = os.path.join(parent_dir, username)
        os.mkdir(path)

        messages.success(request, "Your account was created succesfully.")

        return redirect ('signin')

    return render (request, "cuentas/signup.html")

def signin(request):
    
    if request.method=="POST":
        username = request.POST.get('username')
        passwd = request.POST.get('passwd')

        user = authenticate(username=username, password=passwd)

        if user is not None:
            login(request, user)
            #return render (request, "cuentas/index.html", {'user': request.user})
            return redirect("analyze")
        else:
            messages.error(request, "Invalid credentials.")
            return redirect ("signin")

    return render (request, "cuentas/login.html")

@login_required
def modifyParameters(request):
    if request.method == 'POST':
        if request.POST.get('verify')=="verify":
            password = request.POST.get('password')
            if request.user.check_password(password):
                return render(request, "cuentas/modifyParameters.html", {'verified': 'true'})
            else:
                messages.error(request, "Incorrect password.")
                return redirect("modifyParameters")
        elif request.POST.get('delete')=="delete": #borrar usuario
            user = request.user
            logout(request)
            user.delete()
            messages.success(request, "Your account has been deleted.")  
            return redirect ('home')
        else: #actualizar datos
            user=request.user
            username= request.POST.get('username')
            firstname=request.POST.get('firstname')
            lastname=request.POST.get('lastname')
            email=request.POST.get('email')
            passwd=request.POST.get('passwd')
            passwd2=request.POST.get('passwd2')
            if (not username or not firstname or not lastname or not email or not passwd or not passwd2):
                messages.error(request, "All fields are required.")
                return render(request, "cuentas/modifyParameters.html", {'verified': 'true'})

            if user.get_username()!=username:
                if User.objects.filter(username=username).exists():
                    messages.error(request, "Username already exists.")
                    return render(request, "cuentas/modifyParameters.html", {'verified': 'true'})

            if user.email!=email:
                if User.objects.filter(email=email).exists():
                    messages.error(request, "E-mail already has another account associated.")
                    return render(request, "cuentas/modifyParameters.html", {'verified': 'true'})
            
            if passwd!=passwd2:
                messages.error(request, "Passwords don't match.")
                return render(request, "cuentas/modifyParameters.html", {'verified': 'true'})

            user.username=username
            user.set_password(passwd)
            user.email=email
            user.first_name=firstname
            user.last_name=lastname

            user.save()

            login(request, user)

            messages.success(request, "Your account's parameters were modified succesfully.")

            return redirect ('home')
    else:
        return render(request, "cuentas/modifyParameters.html")

@login_required
def log_out(request):
    logout(request)
    return render(request, "cuentas/index.html")

@login_required
def analyze(request):
    if request.method=='POST':
        sentence=request.POST.get('sentence')
        doc = nlp(sentence)
        if request.POST.get('analyze')=="syntactic":
            sent = list(doc.sents)[0]
            
            #sent = list(doc.sents)[0]
            #displacy.serve(doc, style="dep")
            #for token in doc:
            #   print(token.text, token.pos_, token.dep_)
            constituency=sent._.parse_string
            print(constituency)
            tree=ct.ConstituentTree(sentence, nlp)
            imagepath=os.path.join(os.path.dirname(os.path.dirname(__file__)),'static/images/' + request.user.get_username() + '/resultados.svg')
            tree.export_tree(destination_filepath=imagepath, verbose=True)
            resultspath= "/images/" + request.user.get_username() + "/resultados.svg"
            return render(request, "cuentas/analyze.html", {'user': request.user, 'doc': doc, 'sentence': sentence, 'method': "syntactic", 'constituency':constituency, 'resultspath': resultspath})
        else:
            morph=[]
            for token in doc:
                #expl=spacy.explain(token.tag_)
                morph.append(str(token.morph))

            return render(request, "cuentas/analyze.html", {'user': request.user, 'doc': doc, 'sentence': sentence, 'method': "morphologic", 'morph': morph})
    else:
        return render(request, "cuentas/analyze.html", {'user': request.user})

@login_required
def download(request):
    if request.method=="POST":
        if request.POST.get('method')=="syntactic":
            sentence=request.POST.get('sentence')
            format=request.POST.get('format')
            tree=ct.ConstituentTree(sentence, nlp)
            filepath=os.path.join(os.path.dirname(os.path.dirname(__file__)),'static/images/' + request.user.get_username() + '/resultados.'+ format)
            if format=="pdf":
                wkhtmltopdf=os.path.join(os.path.dirname(os.path.dirname(__file__)), settings.WKHTMLTOPDF_PATH)
                print(wkhtmltopdf)
                tree.export_tree(destination_filepath=filepath, wkhtmltopdf_bin_filepath=wkhtmltopdf, verbose=True)
            else:
                tree.export_tree(destination_filepath=filepath, verbose=True)
            return FileResponse(open(filepath, 'rb'), as_attachment=True)


