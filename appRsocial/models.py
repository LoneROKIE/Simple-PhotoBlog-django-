from django.db import models
from django.contrib.auth.models import User
# Create your models here.

# voy a crear un modelo para las publicaciones de los usuarios
class Publicacion(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE) # el autor de la publicacion
    imagen = models.ImageField(upload_to='publicaciones/%Y/%m/%d/', null=False, blank=False) # la imagen de la publicacion
    descripcion = models.TextField(max_length=500, null=True, blank=True) # la descripcion de la publicacion
    fecha = models.DateTimeField(auto_now_add=True) # la fecha de la publicacion
    
    def __str__(self):
        return f"{self.autor} - {self.fecha}"
        
    