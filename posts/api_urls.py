from django.urls import path
from .api_views import PostListCreate, PostDetail, DashboardApi

urlpatterns = [
    path("posts/", PostListCreate.as_view()),
    path("posts/<int:pk>", PostDetail.as_view()),
    path("dashboard/", DashboardApi.as_view()),
]