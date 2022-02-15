# Generated by Django 3.1.5 on 2021-11-17 21:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ropotApp', '0005_ror'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='account',
            name='account_no',
        ),
        migrations.AddField(
            model_name='account',
            name='area',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='ropotApp.area', verbose_name='المنطقة'),
        ),
    ]
