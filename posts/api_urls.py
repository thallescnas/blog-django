from django.urls import path
from .api_views import PostListCreateView, PostDetailView, DashboardApiView

urlpatterns = [
    path("posts/", PostListCreateView.as_view()),
    path("posts/<int:pk>", PostDetailView.as_view()),
    path("dashboard/", DashboardApiView.as_view()),
]