from django.urls import path
from . import views
urlpatterns = [
    path("", views.iniciar_sesion, name="iniciar_sesion"),
    path('crear_cuenta/', views.crear_cuenta, name="crear_cuenta"),
    path('activar_cuenta/<uidb64>/<token>', views.activar_cuenta, name='activar_cuenta'),
    path('cerrar_sesion/',views.cerrar_sesion, name='cerrar_sesion'),
    
]
