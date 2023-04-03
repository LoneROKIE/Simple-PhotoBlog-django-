from django import forms # hay que importar forms para hacer forms que ironico NO
from . models import Publicacion # importamos nuestra clase
from django.contrib.auth.models import User  # importamos el Modelo Usuario 


"""
# voy a crear un modelo para las publicaciones de los usuarios
class Publicacion(models.Model):
    autor = models.ForeignKey(User, on_delete=models.CASCADE) # el autor de la publicacion
    imagen = models.ImageField(upload_to='publicaciones/%Y/%m/%d/', null=False, blank=False) # la imagen de la publicacion
    descripcion = models.TextField(max_length=500, null=True, blank=True) # la descripcion de la publicacion
    fecha = models.DateTimeField(auto_now_add=True) # la fecha de la publicacion
"""




class Publicacion_form(forms.ModelForm):
    autor = forms.ModelChoiceField(widget=forms.HiddenInput(), queryset= User.objects.all(), required=False)
    
    class Meta:
        model = Publicacion
        fields = ['imagen','descripcion']
        
    def __init__(self,*args, **kwargs):
        autor = kwargs.pop('autor', None)
        super().__init__(*args, **kwargs)
        if autor:
            self.fields['autor'].initial = autor