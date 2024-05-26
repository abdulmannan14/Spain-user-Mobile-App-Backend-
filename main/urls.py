from django.urls import path
from . import views as main_views

urlpatterns = [
    path('userdetails/', main_views.UserDetails.as_view(), name='userdetails'),
    path('alldone/', main_views.AllDone.as_view(), name='userdetails'),
]
