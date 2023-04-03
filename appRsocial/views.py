from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required
from . forms import Publicacion_form
from . models import Publicacion
from django.contrib import messages
from django.contrib.auth.models import User # importamos el modelo User

from login import * 
# Create your views here.
  
@login_required
def home(request):
    """
    En esta pagina se veran todas las publicaciones de los usuarios
    """
    publicaciones = Publicacion.objects.all()   
    return render(request, 'appRs/home.html', {'publicaciones':publicaciones})

@login_required
def crear_publicacion(request):
    """
    En esta pagina se creara una publicacion
    """       
    if request.method == 'POST':
        form = Publicacion_form(request.POST, request.FILES, autor=request.user)
        if form.is_valid():
            publicacion = form.save(commit=False)
            publicacion.autor = request.user
            publicacion.save()
            messages.success(request, 'Publicacion creada con exito')
            return render(request, 'appRs/crear_publicacion.html', {'form':form})   
    else:
        form = Publicacion_form(autor=request.user)
    return render(request, 'appRs/crear_publicacion.html', {'form':form})

@login_required
def eliminar_publicacion(request, pk):
    """
    Vista para eliminar una publicacion
    """
    publicacion = get_object_or_404(Publicacion, pk=pk)
    publicacion.delete()
    messages.success(request, 'Publicacion eliminada con exito')
    return redirect('perfil')

@login_required
def detalles_publicacion(request,pk):
    publicacion = get_object_or_404(Publicacion, pk=pk)
    return render(request, 'appRs/detalles_publicacion.html', {'publicacion':publicacion})

@login_required
def perfil(request):
    """
    Vista para desplegar el perfil de usuario
    """
    usuario = request.user
    publicaciones = Publicacion.objects.filter(autor=usuario)
    return render(request, 'appRs/pagina_usuario.html', {'usuario':usuario, 'publicaciones': publicaciones})

    
