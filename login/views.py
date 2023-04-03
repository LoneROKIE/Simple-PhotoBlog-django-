from django.shortcuts import render, redirect
from django.contrib.auth.models import User # MODELO USUARIO
from django.contrib.auth import authenticate, login, logout # metodo para autenticar
from django.contrib import messages # importamos el modulo messages para imprimir los mensajes por pantalla
from django.contrib.auth.decorators import login_required 

from . token import account_activation_token as GeneradorDeToken # importamos el generador de token
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode # para decodificar el token
from django.utils.encoding import force_bytes
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from loginStyle import settings




def crear_cuenta(request):
    """
    Vista para crear la cuenta de usuario
    """
    username = ''
    email = ''
    password = ''
    
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        
        # validaciones para comprobar que la informacion del usuario sea unica (username,email)
        if User.objects.filter(username=username).exists():
            messages.error(request,'Ups !!, Ese nombre de usuario ya existe :-( ') # mensaje de error si ya existe username
            return redirect('crear_cuenta') # redirije hacia la pagina de crear cuenta
        if User.objects.filter(email=email).exists():
             messages.error(request,'Ups !!, Ese nombre de usuario ya existe :-( ') # mensaje de error si ya existe email
             return redirect('crear_cuenta') # redirije hacia la pagina crear cuenta
    
        usuario = User.objects.create_user(username,email,password) # creacion del usuario 
        usuario.username = username
        usuario.is_active = False # establecemos a el usuario como inactivo, hasta que se verifique su cuenta cambiara a activo
        usuario.save()
        
        # codigo para enviarle el email de confirmacion a el usuario
        
        subject = 'Bienvenido, Por favor Confirma tu email'
        
        message = render_to_string('autentication/confirmacion_email.html',{
            'user': usuario,
            'domain': get_current_site(request).domain,
            'uid': urlsafe_base64_encode(force_bytes(usuario.pk)),
            'token': GeneradorDeToken.make_token(usuario),
        })
        
        email = EmailMessage(subject,message,settings.EMAIL_HOST_USER, [usuario.email])
        email.fail_silently = True
        email.send()
        
        return redirect('iniciar_sesion')
    
    return render(request, 'autenticacion/signup.html')



def iniciar_sesion(request):
    """
    Vista para que el usuario inicie sesion
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        validar = authenticate(username=username, password=password)    
        
        if validar is not None:
            login(request, validar)
            messages.success(request,'Exito al iniciar sesion')
            return redirect('home') # esto debe llevarnos al menu principal       
    
    return render(request, "autenticacion/login.html")

def cerrar_sesion(request):
    logout(request)
    return redirect('iniciar_sesion') # luego puedo cambiar esto xd a una pagina donde elijamos iniciar sesion - registrar 
    

def activar_cuenta(request,uidb64, token):
    """
    Se intenta decodificar el valor de uidb64 en una cadena usando la función urlsafe_b64decode de la 
    biblioteca base64. Luego, se intenta obtener un objeto de usuario de la base de datos con el 
    identificador de usuario decodificado (uid).
    
    Si no se puede decodificar uidb64 o no se encuentra un objeto de usuario con el 
    identificador proporcionado, la variable user se establece en None.
    
    Si user no es None, se verifica si el token proporcionado es 
    válido usando el método check_token del generador de tokens (tokenGenerator).
    
    Si el token es válido, se establece el atributo is_active del usuario en True, 
    se guarda el usuario en la base de datos y se inicia la sesión del usuario con la 
    función login. Después, el usuario es redirigido a la página de inicio (home).
    
    Si el token no es válido, se renderiza la plantilla authentication/activar_cuenta.html 
    en el contexto de la petición request.
    """
    try:
        uid = force_bytes(urlsafe_base64_decode(uidb64)).decode('utf-8')
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and GeneradorDeToken.check_token(user, token):
        user.is_active = True
        user.save()
        return redirect('iniciar_sesion')
    else:
        messages.error(request, 'No se pudo activar la cuenta!')
        return render(request,'autenticacion/fallo_activar.html')