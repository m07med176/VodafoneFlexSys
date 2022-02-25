from pyexpat import model
from django.shortcuts import render
from django.utils.datastructures import MultiValueDictKeyError
from ropotApp.api import serializers

# djnago utils
from django.utils import timezone
# External Scripts#
from ropotApp.utils.databaseManager import DatabaseManager
from ropotApp.utils.robot import Robot

# REST FRAMEWORK
from rest_framework.response import Response
from rest_framework.decorators import api_view,permission_classes
from rest_framework import  permissions                             # permission
from rest_framework.pagination import PageNumberPagination          # pagination 

# filter and search
from rest_framework.filters import SearchFilter,OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend

# VIEWSETS
from rest_framework import viewsets
# Models
from ropotApp.models import Area,Branch,ScrappingLogs
# Serializers
from ropotApp.api.serializers import (SArea,SBranch,AreaS,BranchS,
                                      NumbersSerializer,
                                      ScrappingLogsS)
# threading 
from threading import Thread


rb = Robot()
t = None

# region Area and Branches
class AreaL(viewsets.ModelViewSet):
    pagination_class = None
    queryset = Area.objects.all()
    serializer_class = SArea

class BranchL(viewsets.ModelViewSet):
    pagination_class = None
    queryset = Branch.objects.all()
    serializer_class = SBranch

@api_view(['GET',])
@permission_classes((permissions.AllowAny,))
def getAreas(request):
    data = Area.objects.all()
    ser = AreaS(data,many=True)
    return Response({"data": ser.data })

@api_view(['POST',])
@permission_classes((permissions.AllowAny,))
def editArea(request):
    id = request.query_params.get('id')
    select = request.query_params.get('selected')
    if id == None or select == None :  return Response({"message":"حدث مشكلة","status":False})
    select = select.capitalize()
    data = Area.objects.get(id=id)
    data.selected = select
    data.save()
    return  Response({"message":"تم التعديل","status":True})


@api_view(['GET',])
def getBranches(request,id):
    data = Branch.objects.filter(area_id=id)
    ser = BranchS(data,many=True)
    return Response({"data": ser.data })

@api_view(['GET',])
def getBranchesName(request,name):
    data = Branch.objects.filter(area__area_name=name)
    ser = BranchS(data,many=True)
    return Response({"data": ser.data })


@api_view(['GET',])
def getBranchesWithCount(request):
    area = request.query_params['area']
    data = Branch.objects.filter(area__area_name=area)
    ser = SBranch(data,many=True)
    return Response({"data": ser.data })

# endregion Area and Branches



# region Scrapping

def ScrappingResponse(name = "" ,content = ""):
    date = timezone.now()
    return Response(
        ScrappingLogsS(
            ScrappingLogs(
                id = -1,
                name=name,
                content = content,
                type = 0,
                created_at=date,
                updated_at = date
            )
            ,many=False).data
        )

@api_view(['GET',])
def startScrappingNumbers(request):
    allArea = request.query_params.get('isAllArea','false')
    allArea = allArea == "true" if True else False
    allBranch = request.query_params.get('isAllBranch','false')
    allBranch = allBranch == "true" if True else False

    t  = Thread(target=rb.startApp,args=(allArea,allBranch))
    t.setDaemon(True)
    t.start()
    return ScrappingResponse(content =  "بدأ تشغيل السحب")

@api_view(['GET',])
def stopScrappingNumbers(request):
    if t is None: return ScrappingResponse(content = "قم بتشغيل الفحص أولاً")
    try:
        t.join()
        if not t.isAlive(): 
            return ScrappingResponse(content = "تم إيقاف السحب")
    except Exception:
        return ScrappingResponse(content = "يوجد مشكلة فى إيقاف عملية السحب")


@api_view(['GET',])
def checkNumber(request):
    rb = Robot()
    try:
        phoneNumber = request.query_params.get('number')
        branchSelect = request.query_params.get('branch')
        areaSelect = request.query_params.get('area')
    except MultiValueDictKeyError: 
        
        return ScrappingResponse(content = "يوجد مشكلة برجاء المحاولة مرة أخرى")
    t = Thread(target=rb.checkNumber,args=(phoneNumber,branchSelect,areaSelect))    
    t.setDaemon(True)
    t.start()
    
    return ScrappingResponse(content = f"جارى فحص صلاحية رقم {phoneNumber}")

class Logs(viewsets.ModelViewSet):
    serializer_class = ScrappingLogsS
    queryset = ScrappingLogs.objects.all()
    pagination_class = PageNumberPagination
    permission_classes = [permissions.IsAuthenticated,]
    filter_backends  =  [OrderingFilter,DjangoFilterBackend]
    filterset_fields =  ["type","content","name"]
    ordering_fields  =  ['created_at']
# endregion Scrapping

# region Numbers
class NumbersL(viewsets.ModelViewSet):
    serializer_class = NumbersSerializer
    PageNumberPagination.page_size = 20
    def get_queryset(self):
        querry = {}
        for k,v in self.request.query_params.items():
            if v.isdigit():  v = int(v)
            if v == "true" : v = True
            if v == "false": v = False
            querry[k]=v

        return DatabaseManager().showNumbers(querry)


@api_view(['PUT',])
def requestNumber(request):
    try:
        phoneNumber = request.query_params.get('order',"")
        userNumber = request.query_params.get('user',"")
        db = DatabaseManager()
        response = db.updateReservation(phoneNumber,userNumber)
        return Response(response)
    except Exception as e:
        return  Response({"message":"طلب فاشل برجاء المحاولة مرة أخرى","status":False})

@api_view(['DELETE',])
def deleteNumber(request):
    """
        request delete number

        alghrism:
        0 - put try and catch
        1 - get number 
        2 - call database manager class
        3-  create threading for delete number and put arguments
        4-  set deamon
        5 - start threading
        6 - put any response
    """
    try:
        number = request.query_params.get('number',"")
        db  = DatabaseManager()
        t  = Thread(target=db.deleteNumber,args=[number])
        t.setDaemon(True)
        t.start()
        return Response({"message":f"تم حذف رقم  {number} ","status":True})
    except Exception as e:
        return Response({"message":"يوجد مشكلة برجاء المحاولة مره أخرى ","status":False})

@api_view(['PUT',])
def updateDone(request):
    try:
        number = request.query_params.get('number',"")
        is_done = request.query_params.get('is_done',False)
        if is_done == "true" : is_done = True
        if is_done == "false": is_done = False
        db = DatabaseManager()
        response  = db.updateDone(number,is_done)
        return Response(response)
    except Exception as e:
        return Response({"message":"يوجد مشكلة برجاء المحاولة مره أخرى ","status":False})

@api_view(['GET',])
def displayNumbers(request):
    querry = {}
    for k,v in request.query_params.items():
        if v.isdigit():  v = int(v)
        if v == "true" : v = True
        if v == "false": v = False
        querry[k]=v

    queryset = DatabaseManager().showNumbers(querry)
    paginator = PageNumberPagination()
    paginator.page_size = 20
    page = paginator.paginate_queryset(queryset, request)
    serializer = NumbersSerializer(page, many=True, context={'request': request})
    return paginator.get_paginated_response(serializer.data)
# endregion Numbers