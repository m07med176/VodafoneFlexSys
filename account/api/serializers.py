from rest_framework import serializers
from account.models import Account
from rest_framework.authtoken.models import Token


class SAccountShow(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['pk', 'email', 'username','phone' ,'area']
class SAccountAll(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = '__all__'
class SAccountResponse(serializers.ModelSerializer):
    area_name = serializers.SerializerMethodField('get_area_name')
    token = serializers.SerializerMethodField('get_username_token')
    class Meta:
        model = Account
        fields = [
            'pk', 
            'email', 'username','phone','area' ,"area_name",
            'is_admin','is_active','is_staff','is_superuser',
            "type",
            'token',"password",
            "date_joined","last_login"]
    def get_username_token(self, account):
        try:
            token = Token.objects.get(user=account).key
        except Token.DoesNotExist:
            token = Token.objects.create(user=account)
        return token
    def get_area_name(self, account): return account.area.area_name
# post serializers fror user
class AccountS(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'},write_only=True)
    class Meta:
        model = Account
        fields = ["email","username","phone","area","password","password2"]
        extra_kwargs = {
            'password':{'write_only':True}
        }

    def save(self):
        account= Account(
            email=self.validated_data['email'],
            username=self.validated_data['username'],
            area=self.validated_data['area'],
            phone=self.validated_data['phone'],
        )

        password=self.validated_data['password']
        password2=self.validated_data['password2']
        if password!=password2:
            raise serializers.ValidationError({'password':'password must match'})
        
        account.set_password(password)
        account.save()
        return account

# post serializers for manager
class SAccountManager(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ["password","email","username","phone","area","is_superuser","is_admin","is_staff","is_active","type"]
        extra_kwargs = { 'password':{'write_only':True} }
    

    def save(self):
        account= Account(
            email           = self.validated_data['email'],
            username        = self.validated_data['username'],
            area      = self.validated_data['area'],
            phone           = self.validated_data['phone'],
            is_superuser    = self.validated_data['is_superuser'],
            is_admin        = self.validated_data['is_admin'],
            is_staff        = self.validated_data['is_staff'],
            is_active       = self.validated_data['is_active'],
            type            = self.validated_data['type']
        )
        password = self.validated_data['password']
        account.set_password(password)
        account.save()
        return account
    def update(self, instance):
        instance.email = self.validated_data.get('email', instance.email)
        instance.username = self.validated_data.get('username', instance.username)
        instance.area = self.validated_data.get('area', instance.area)
        instance.phone = self.validated_data.get('phone', instance.phone)

        instance.is_superuser = self.validated_data.get('is_superuser', instance.is_superuser)
        instance.is_admin = self.validated_data.get('is_admin', instance.is_admin)
        instance.is_staff = self.validated_data.get('is_staff', instance.is_staff)
        instance.is_active = self.validated_data.get('is_active', instance.is_active)
        instance.type = self.validated_data.get('type', instance.type)

        password = self.validated_data['password']
        instance.set_password(password)
        instance.save()
        return instance

