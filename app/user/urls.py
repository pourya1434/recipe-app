from django.urls import path

from user import views

# app_name used for reverce mapping
app_name = "user"

urlpatterns = [path("create/", views.CreateUserView.as_view(), name="create")]
