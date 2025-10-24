from django.urls import path
from . import views
from .views import *

urlpatterns = [
 #path("list/", views.list_conferences, name="list_conferences"),
    path("list/", ConferenceList.as_view(), name="list_conferences"),
    path("<int:pk>/", ConferenceDetail.as_view(), name="conference_detail"),
    path("add/", ConferenceCreate.as_view(), name="conference_add"),
]
