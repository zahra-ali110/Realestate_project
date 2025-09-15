from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),   # homepage
    path("", include("allauth.urls")),     # adds /accounts/login/, /accounts/signup/, etc.
    path("post-property/", views.post_property, name="post_property"),

]
