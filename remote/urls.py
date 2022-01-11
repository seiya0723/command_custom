from django.urls import path
from . import views

app_name    = "remote"
urlpatterns = [
    path('', views.index, name="index"),
]

