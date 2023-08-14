from django.contrib import messages
from django.shortcuts import redirect


#ESTA FUNCION ES LA QUE CREA LOS DECORADORES PARA ASIGNAR DESPUES LOS PERMISOS A LAS FUNCIONES PARA QUE SEGUN SU PERMISO PUEDA ACCEDER O O A ELLAS 
def has_permission(permiso_nombres):
    def decorator(view_func):
        def check_permission(request, *args, **kwargs):
            if request.user.is_authenticated:
                user_roles = request.user.roles
                if any(user_roles.permisos.filter(nombre=permiso).exists() for permiso in permiso_nombres):
                    return view_func(request, *args, **kwargs)
            # Mostrar mensaje de información para indicar que no tiene permisos
            messages.info(request, "No tienes permisos para acceder a esta vista.")
            return redirect('home')  # Agregar el paréntesis aquí
        return check_permission
    return decorator


