from django.urls import path
from ropotApp.api import views as api
app_name = 'ropotApp'

urlpatterns = [
    # region Scrapping
    path('start_scrapping/',api.startScrappingNumbers),
    path('stop_scrapping/',api.stopScrappingNumbers),
    path('checking/',api.checkNumber),
    # endregion Scrapping

    # region Areas and Branches
    path("branches_count/",api.getBranchesWithCount),
    path("areas/",api.getAreas),
    path("edit_area/",api.editArea),
    path("branches/<int:id>/",api.getBranches),
    # endregion 

    # region numbers
    path('display/',api.displayNumbers),
    path('done/',api.updateDone),
    path('delete/',api.deleteNumber),
    path('order/',api.requestNumber),
    # endregion
    
]