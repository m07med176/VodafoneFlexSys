# ------------ API AND  APIVIEW AND VIEWSETS-----------#

from rest_framework.generics import UpdateAPIView
from django.contrib.auth import authenticate
# API UTILS
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework.response import Response
from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from account.api import serializers
from account.api.pagination import LargeResultsSetPagination
from rest_framework import  permissions
from main.permissions import IsActivePermission
# VIEWSETS
from rest_framework import viewsets
# APIVIEW
from rest_framework.views import APIView
# ------------ SERIALIZERS -----------#
from account.api.serializers import (
	AccountS,
	SAccountManager,
	SAccountShow,
	SAccountResponse,
	SAccountAll,
	)
from rest_framework.authtoken.models import Token
# ------------ MODELS -----------#
from account.models import Account


class UsersMVS(viewsets.ModelViewSet):
    pagination_class = LargeResultsSetPagination
    queryset = Account.objects.all()
    serializer_class = SAccountAll
    filter_backends = [SearchFilter,OrderingFilter,DjangoFilterBackend]
    filterset_fields = ["is_superuser","is_admin","is_staff","is_active","type"]
    search_fields = ["email","username","phone","area"]
    ordering_fields = ['type','username','date_joined', 'last_login']
    def update(self, request, *args, **kwargs):
        super(UsersMVS, self).update(request, *args, **kwargs)
        return Response({"message": "تم تعديل المستخدم بنجاح","status":  True})
    def create(self, request, *args, **kwargs):
        super(UsersMVS, self).create(request, *args, **kwargs)
        return Response({"message": "تم إضافه المستخدم بنجاح","status":  True})
    def destroy(self, request, *args, **kwargs):
        super(UsersMVS, self).destroy(request, *args, **kwargs)
        return Response({"message": "تم حذف المستخدم بنجاح","status":  True})

# region User
# LOGIN
class ObtainAuthTokenView(APIView):
	authentication_classes 	= []
	permission_classes 		= []
	def post(self, request):
		phone = request.POST.get('phone')
		password = request.POST.get('password')
		print(phone)
		print(password)
		account = authenticate(phone=phone, password=password)
		serializers = SAccountResponse(account)
		if account :
			return Response(serializers.data)
		else:
			return Response(serializers.errors)

# REGISTER
@api_view(['POST',])
@permission_classes((AllowAny, ))
def register_account(request):
	if request.method == 'POST':
		if validate_username(request.data.get('username', '0')) != None: 
			return Response({'message':'هذا الإسم مستخدم من قبل.','status':False})

		if validate_phone(request.data.get('phone', '0')) != None: 
			return Response({'message':'رقم المحمول هذا مستخدم من قبل.','status':False})

		serializers = AccountS(data=request.data)
		if serializers.is_valid():
			account = serializers.save()
			return Response(SAccountResponse(account).data)
		else:
			return Response(serializers.errors)

# STATE
@api_view(['GET', ])
@permission_classes((permissions.AllowAny,))
def getUserState(request,id):
	try:
		account = Account.objects.get(pk=id)
		return Response(SAccountResponse(account).data)
	except Account.DoesNotExist:
		return Response(status=status.HTTP_404_NOT_FOUND)
	

# Account update properties
@api_view(['PUT',])
@permission_classes((IsAuthenticated, ))
def update_account_view(request):
	context = {}
	context['message'] = "فشل فى التعديل"
	context['status'] = False
	try:
		account = request.user
	except Account.DoesNotExist:
		return Response(data=context)
		#return Response(status=status.HTTP_404_NOT_FOUND)
		
	if request.method == 'PUT':
		serializer = SAccountShow(account, data=request.data)
		
		if serializer.is_valid():
			serializer.save()
			context['message'] = "تم التعديل بنجاح."
			context['status'] = True
			return Response(data=context)
		#return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
		return Response(data=context)


# Account properties
@api_view(['GET', ])
def account_properties_view(request):
	try: account = request.user
	except Account.DoesNotExist: return Response(status=status.HTTP_404_NOT_FOUND)
	if request.method == 'GET': return Response(SAccountResponse(account).data)
# endregion

# region Manager
@api_view(['POST',])
def registerAccountManager(request):
	if request.method == 'POST':
		username = request.data.get('username', '0')
		phone = request.data.get('phone', '0')
		if validate_username(username) != None: return Response({'message':'هذا الإسم مستخدم من قبل.','status':False})
		if validate_phone(phone) != None: return Response({'message':'رقم المحمول هذا مستخدم من قبل.','status':False})

		serializers = SAccountManager(data=request.data)
		if serializers.is_valid():
			serializers.save()
			return Response({'message': "تم التسجيل بنجاح.",'status':True})
		else:
			return Response(serializers.errors)

@api_view(['GET',])
def getAccountManager(request):
	if request.method == 'GET':
		account = Account.objects.get_queryset().order_by('id')
		return Response({"results":SAccountResponse(account,many=True).data})

@api_view(['DELETE',])
def deleteAccountManager(request,id):
	if request.method == 'DELETE':
		try:
			account = Account.objects.get(pk=id)
		except Account.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		account.delete()
		return Response({'message': "تم الحذف بنجاح .",'status':True})

@api_view(['PUT',])
def updateAccountManager(request,id):
	if request.method == 'PUT':
		try:
			account = Account.objects.get(pk=id)
		except Account.DoesNotExist:
			return Response(status=status.HTTP_404_NOT_FOUND)
		serializers = SAccountManager(instance=account,data=request.data)  
		if serializers.is_valid():
			serializers.update(account)
			return Response({'message': "تم التعديل بنجاح.",'status':True})
		else: return Response(serializers.errors)
# endregion Manager

# region Validation
def validate_username(username):
	account = None
	try:
		account = Account.objects.get(username=username)
	except Account.DoesNotExist:
		return None
	if account != None:
		return username

def validate_phone(phone):
	account = None
	try:
		account = Account.objects.get(phone=phone)
	except Account.DoesNotExist:
		return None
	if account != None:
		return phone
# endregion Validation

# region Junk
# from account.api.pagination import LargeResultsSetPagination
# class UsersMVS(viewsets.ModelViewSet):
# 	queryset = Account.objects.get_queryset().order_by('id')
# 	pagination_class = LargeResultsSetPagination
# 	serializer_class = SAccountAll
	# def destroy(self, request, *args, **kwargs):
	# 	super(SAccountManager, self).destroy(request, *args, **kwargs)
	# 	return Response({"message": "تم حذف المستخدم بنجاح","status":  True})
	# def create(self, request, *args, **kwargs):
	# 	super(SAccountManager, self).create(request, *args, **kwargs)
	# 	return Response({"message": "تم إضافة المستخدم بنجاح","status":  True})
	# def update(self, request, *args, **kwargs):
	# 	super(SAccountManager, self).update(request, *args, **kwargs)
	# 	return Response({"message": "تم تعديل المستخدم بنجاح","status":  True})
# endregion