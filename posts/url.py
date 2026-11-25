from django.urls import path
from . import views



urlpatterns = [
    path(
        '',
        views.listar_posts,
        name='posts'
    ),
    path(
        'new_post', 
        views.criar_post,
        name='create_post'
    ),
    path(
        'dashboard',
        views.exibir_dashboard,
        name='dashboard'
    ),
    path(
        'dashboard/exportar/',
        views.exportar_csv,
        name='exportar_csv'
    ),
]