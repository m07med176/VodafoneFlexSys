# Generated by Django 3.1.5 on 2021-11-09 09:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('email', models.EmailField(help_text='مطلوب إضافة الايميل', max_length=60, unique=True, verbose_name='الإيميل')),
                ('username', models.CharField(help_text='مطلوب إضافة الإســم', max_length=30, unique=True, verbose_name='إسم المستخدم')),
                ('phone', models.CharField(help_text='مطلوب إضافة رقم التليفون', max_length=11, unique=True, verbose_name='رقم التليفون')),
                ('account_no', models.IntegerField(blank=True, help_text='مطلوب إضافة رقم الحساب', null=True, unique=True, verbose_name='الرقم الكودى')),
                ('date_joined', models.DateTimeField(auto_now_add=True, verbose_name='تاريخ التسجيل')),
                ('last_login', models.DateTimeField(auto_now=True, verbose_name='أخر دخول')),
                ('is_superuser', models.BooleanField(default=False, verbose_name='مسئول عام')),
                ('is_admin', models.BooleanField(default=False, verbose_name='مدير')),
                ('is_staff', models.BooleanField(default=False, verbose_name='محاسب')),
                ('is_active', models.BooleanField(default=False, verbose_name='نشط')),
                ('type', models.IntegerField(choices=[(0, 'محاسب'), (1, 'مندوب'), (2, 'عميل'), (3, 'محصل'), (4, 'محول'), (5, 'مدير')], default=0, verbose_name='نوع الحساب')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
