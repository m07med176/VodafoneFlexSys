from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.pagination import PageNumberPagination
from rest_framework.generics import ListAPIView

# class GetNumbersAPI(ListAPIView):
#     # def __init__(self,branch):
#     #     self.branch = branch
#     #     print(self.branch)
#     # queryset = VodafoneNumber.objects.all()
#     serializer_class = VodafoneNumberSer
#     pagination_class = PageNumberPagination
#     def get_queryset(self):
#         # branch = self.request.branch
#         branch = self.kwargs['branch']
#         return VodafoneNumberShow.objects.filter(branch=branch)
