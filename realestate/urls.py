from django.contrib import admin
from django.urls import path, include
from accounts import views   # import your app views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", views.index, name="index"),   # 👈 homepage at /
    path("accounts/", include("allauth.urls")),  # django-allauth
    path("", include("accounts.urls")),
]
