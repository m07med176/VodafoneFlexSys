from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from ropotApp.models import Area
class MyAccountManager(BaseUserManager):
	def create_user(self, phone,email, username, password=None):
		if not username:
			raise ValueError('Users must have a username')
		if not phone:
			raise ValueError('Users must have a phone number')
		
		user = self.model(
			username=username,
			phone=phone,
		)

		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, phone,email, username, password):
		user = self.create_user(
			password=password,
			username=username,
			phone=phone,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.is_active = True
		user.save(using=self._db)
		return user


class Account(AbstractBaseUser):
	email = models.EmailField(verbose_name="الإيميل", max_length=60, unique=False,help_text='مطلوب إضافة الايميل')
	username = models.CharField(verbose_name="إسم المستخدم",max_length=30, unique=True,help_text='مطلوب إضافة الإســم')
	phone = models.CharField(max_length=11,unique=True,blank=False,verbose_name = "رقم التليفون",help_text='مطلوب إضافة رقم التليفون')
	area = models.ForeignKey(Area,on_delete = models.CASCADE,verbose_name="المنطقة",null=True)
	
	date_joined				= models.DateTimeField(verbose_name='تاريخ التسجيل', auto_now_add=True)
	last_login				= models.DateTimeField(verbose_name='أخر دخول', auto_now=True)
	
	is_superuser			= models.BooleanField(default=False,verbose_name = 'مسئول عام')
	is_admin				= models.BooleanField(default=False,verbose_name = 'مدير')
	is_staff				= models.BooleanField(default=False,verbose_name = 'محاسب')
	is_active				= models.BooleanField(default=False,verbose_name = 'نشط')
	choices = [
		(0, 'محاسب'),
		(1, 'مندوب'),
		(2, 'عميل'),
		(3, 'محصل'),
		(4, 'محول'),
		(5, 'مدير'),
	]
	type				= models.IntegerField(choices=choices,default=0,verbose_name="نوع الحساب")

	USERNAME_FIELD = 'phone'
	REQUIRED_FIELDS = ['username']

	objects = MyAccountManager()

	def __str__(self):
		return self.username

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created: Token.objects.create(user=instance)