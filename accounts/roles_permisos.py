from .models import User,Rol,Permiso
from django.shortcuts import render
#este archivo es como el view.py pero solo para roles y permisos, en urls ya esta importado.
#MANTENEDORES DE ROLES Y PERMISOS


def roles_list(request):
    rol = Rol.objects.all()
    permiso = Permiso.objects.all()
    context = { 'rol': rol,
                'permiso': permiso}
    return render(request, 'roles/roles_permisos.html', context)

def permisos_list(request):
    permiso = Permiso.objects.all()
    context = {'permiso': permiso}
    return render(request, 'roles/roles_permisos.html', context)

