# Generated by Django 3.1.5 on 2021-11-10 20:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ropotApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='config',
            name='name',
            field=models.CharField(max_length=50, unique=True, verbose_name='Variable Name'),
        ),
    ]
