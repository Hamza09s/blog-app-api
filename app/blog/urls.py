"""
URL mappings for the recipe app.
"""
from django.urls import (
    path,
    include,
)

from rest_framework.routers import DefaultRouter

from blog import views


router = DefaultRouter()
router.register('blogs', views.BlogViewSet)
# create endpoints,all available crud methods and register endpoints
# for them


app_name = 'blog'

urlpatterns = [
    path('', include(router.urls)),
]
