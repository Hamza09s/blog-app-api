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
router.register("blogs", views.BlogViewSet)
# router.register("likes", views.LikeViewSet)
# router.register("comments", views.CommentViewSet)
# router.register('get_likes', views.NewLikeViewSet)
# router.register('Post', views.PostViewSet)
# create endpoints,all available crud methods and register endpoints
# for them


app_name = "blog"

urlpatterns = [
    path("", include(router.urls)),
]
