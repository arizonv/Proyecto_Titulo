from django import template

register = template.Library()

@register.filter(name='has_permission')
def has_permission(user, permission_name):
    try:
        return user.roles.permisos.filter(nombre=permission_name).exists()
    except AttributeError:
        return False
