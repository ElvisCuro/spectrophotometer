from django.urls import path
from . import views
from django.contrib import admin
from .models import Mediciones,Experimento

# Registrar el modelo en el administrador
admin.site.register(Mediciones)
admin.site.register(Experimento)

urlpatterns = [
    path('', views.home_view, name='index'),  # Ruta que muestra el template con los valores
    path('obtener-datos/', views.obtener_datos, name='obtener_datos'),  # Ruta para obtener los datos en JSON
    path('admin/', admin.site.urls),  # Ruta para acceder al panel de administración
]
