from django.urls import path,include
from ropotApp.api import views as api

from rest_framework import routers
router = routers.DefaultRouter()
router.register('branch',api.BranchL,basename = "branch")
router.register('area',api.AreaL,basename = "area")
router.register('numbers',api.NumbersL,basename="numbers")
router.register('logs',api.Logs,basename="Logs")

urlpatterns = [
    path('api/', include('ropotApp.api.urls')),
    path('', include('ropotApp.web.urls')),
    path('apis/', include(router.urls)),
]