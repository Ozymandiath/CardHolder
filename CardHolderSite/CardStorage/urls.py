from django.urls import path
from .views import *

urlpatterns = [
    path("", Storage.as_view(), name="home"),
    path("generator/", GeneratorCard.as_view(), name="generator"),

]
