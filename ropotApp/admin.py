from django.contrib import admin
from ropotApp.models import Config,ROR,Area,Branch,ScrappingLogs
admin.site.register(ROR)
admin.site.register(Area)
admin.site.register(Branch)
admin.site.register(Config)
admin.site.register(ScrappingLogs)
