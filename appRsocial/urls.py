from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('home/', views.home, name='home'),
    path('crear_publicacion/', views.crear_publicacion, name='crear_publicacion'),
    path('eliminar_publicacion<int:pk>/', views.eliminar_publicacion, name='eliminar_publicacion'),
    path('detalles_publicacion<int:pk>/', views.detalles_publicacion, name='detalles_publicacion'),
    path('perfil/', views.perfil, name='perfil'),
    

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
