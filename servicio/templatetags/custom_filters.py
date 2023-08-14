from django import template

register = template.Library()
#ESTE ES UNA FUNCION QUE CREA UN FILTRO PARA UTILIZAR EN LOS HTML  AL FINAL DEL PROYETO LO UTILIZAREMOS HAY EJE,PLOS DE USO EN LA CARPETA TEMPLATE/PARTIALS/NAV
@register.filter(name='has_permission')
def has_permission(user, permission_name):
    try:
        return user.roles.permisos.filter(nombre=permission_name).exists()
    except AttributeError:
        return False
