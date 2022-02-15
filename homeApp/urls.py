from django.urls import path
from homeApp.web import views as web
from django.conf import settings
from django.conf.urls.static import static
from homeApp.api import views as api
urlpatterns = [ 
                path('', web.landline), # root
                path('home/' , web.home ,name = 'home'),

                ]
urlpatterns += static(settings.STATIC_URL,document_root=settings.STATIC_URL)
