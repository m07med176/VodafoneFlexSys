from django.shortcuts import render

def home(request):
    return render(request,'base.html')
def landline(request):
    return render(request,'landline.html')
