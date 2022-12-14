from django.urls import path
from .views import *

urlpatterns = [
    path("", Storage.as_view(), name="home"),
    path("generator/", GeneratorCard.as_view(), name="generator"),
    path("profile/<int:pk>", ProfileCard.as_view(), name="profile"),
    path("profile/<int:pk>/activate", ActivateCard.as_view(), name="activate"),
    path("profile/<int:pk>/delete", DeleteCard.as_view(), name="delete"),

]
