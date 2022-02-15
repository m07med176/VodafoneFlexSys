from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate

from account.models import Account


class RegistrationForm(UserCreationForm):
	class Meta:
		model = Account
		fields = ('email','phone','area', 'username', 'password1', 'password2', )

	def clean_email(self):
		email = self.cleaned_data['email'].lower()
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
		except Account.DoesNotExist:
			return email
		raise forms.ValidationError('Email "%s" is already in use.' % account)

	def clean_username(self):
		username = self.cleaned_data['username']
		try:
			account = Account.objects.exclude(pk=self.instance.pk).get(username=username)
		except Account.DoesNotExist:
			return username
		raise forms.ValidationError('Username "%s" is already in use.' % username)

	def clean_phone(self):
		phone = self.cleaned_data['phone']
		try:
			phone = Account.objects.exclude(pk=self.instance.pk).get(phone=phone)
		except Account.DoesNotExist:
			return phone
		raise forms.ValidationError('Phone "%s" is already in use.' % phone)
	
	def clean_account_no(self):
		area = self.cleaned_data['area']
		try:
			area = Account.objects.exclude(pk=self.instance.pk).get(area=area)
		except Account.DoesNotExist:
			return area
		raise forms.ValidationError('Account No "%s" is already in use.' % area)


class AccountAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = Account
		fields = ('phone', 'password')

	def clean(self):
		if self.is_valid():
			phone = self.cleaned_data['phone']
			password = self.cleaned_data['password']
			if not authenticate(phone=phone, password=password):
				raise forms.ValidationError("دخول خاطىء")


class AccountUpdateForm(forms.ModelForm):
    
    class Meta:
        model = Account
        fields = ('username', 'email', 'phone', 'area' )

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        try:
            account = Account.objects.exclude(pk=self.instance.pk).get(email=email)
        except Account.DoesNotExist:
            return email
        raise forms.ValidationError('Email "%s" is already in use.' % account)

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            username = Account.objects.exclude(pk=self.instance.pk).get(username=username)
        except Account.DoesNotExist:
            return username
        raise forms.ValidationError('Username "%s" is already in use.' % username)


    def save(self, commit=True):
        account = super(AccountUpdateForm, self).save(commit=False)
        account.username = self.cleaned_data['username']
        account.email = self.cleaned_data['email'].lower()
        account.phone = self.cleaned_data['phone']
        account.area = self.cleaned_data['area']
        if commit:
            account.save()
        return account










