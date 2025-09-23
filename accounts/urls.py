from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login/", views.login_view, name="login"),
    path("signup/", views.signup_view, name="signup"),
    path("post-property/", views.post_property, name="post_property"),
    path("properties/", views.properties_page, name="properties"),  # 👈 new route
    path("property/<int:pk>/", views.property_detail, name="property_detail"),  # NEW
    path("profile/", views.profile, name="profile"),
path("edit-property/<int:property_id>/", views.edit_property, name="edit_property"),
path("edit-property/<int:property_id>/", views.edit_property, name="edit_property"),
path("delete-property/<int:property_id>/", views.delete_property, name="delete_property"),
path("delete-property-image/<int:image_id>/", views.delete_property_image, name="delete_property_image"),
    path('edit-username/', views.edit_username, name='edit_username'),  # use views.edit_username

]
