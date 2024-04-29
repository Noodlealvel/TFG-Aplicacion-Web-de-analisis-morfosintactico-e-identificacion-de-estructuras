from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('logout', views.log_out, name="logout"),
    path('modifyParameters', views.modifyParameters, name="modifyParameters"),
    path('analyze', views.analyze, name="analyze"),
    path('correct', views.correct, name="correct"),
    path('tone', views.tone, name="tone"),
    #path('generate', views.generate, name="generate"),
    path('download', views.download, name="download"),
]
