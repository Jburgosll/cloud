from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    # Panel de administración (simulación): catálogos y películas
    path('panel/', views.panel, name='panel'),
    path('panel/catalogo/<int:pk>/eliminar/', views.delete_catalog, name='delete_catalog'),
    path('panel/pelicula/<int:pk>/eliminar/', views.delete_movie, name='delete_movie'),
]
