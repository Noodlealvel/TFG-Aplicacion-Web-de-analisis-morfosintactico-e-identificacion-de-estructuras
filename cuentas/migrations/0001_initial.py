# Generated by Django 4.2.6 on 2024-04-25 20:29

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Analysis',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sentence', models.TextField()),
                ('type', models.TextField()),
                ('resultSyntactic', models.FileField(upload_to='D:\\Alvel\\Desktop\\Uni\\TFG\\tfg\\TFG\\static/media/svg')),
                ('resultMorphologic', models.TextField()),
                ('date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
