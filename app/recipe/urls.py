from recipe import views
from django.urls import path, include

from rest_framework.routers import DefaultRouter

router = DefaultRouter()

router.register("recipes", views.RecipeViewSet)
router.register("tags", views.TagViewSet)

app_name = "recipe"
urlpatterns = [path("", include(router.urls))]
