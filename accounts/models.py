
from django.contrib.auth.models import UserManager
import re
from django.db import models
from django.core import validators
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)
from django.db.models.signals import pre_save,post_migrate
from django.dispatch import receiver
from django.db import models, transaction 


class Permiso(models.Model):
    CLASES_CHOICES = [
        ('Permiso', 'Permiso'),
        ('Rol', 'Rol'),
        ('User', 'User'),
        ('Cliente', 'Cliente'),
        ('Reserva', 'Reserva'),
        ('Ticket', 'Ticket'),
        ('Boleta', 'Boleta'),
        ('TipoCancha', 'TipoCancha'),
        ('Cancha', 'Cancha'),
        ('Horario', 'Horario'),
        ('Agenda', 'Agenda'),
    ]
    clase = models.CharField(max_length=15, choices=CLASES_CHOICES)
    nombre = models.CharField(max_length=50)

    class Meta:
        unique_together = ('clase', 'nombre')  

    def __str__(self):
        return self.nombre

#ESTE TIPO DE FUNCIONES ES PARA CUANDO SE HAGA EL MIGRATE RELLENAR AUTOMATICO CON PERMISOS POR DEFECTO
@receiver(post_migrate)
def create_default_permissions(sender, **kwargs):
    if sender.name == 'accounts':
        with transaction.atomic():
            for choice_value, choice_display in Permiso.CLASES_CHOICES:
                for perm_action in ['crear', 'leer', 'actualizar', 'eliminar']:
                    perm_name = f'{perm_action} {choice_display.lower()}'
                    permiso, _ = Permiso.objects.get_or_create(
                        clase=choice_value,
                        nombre=perm_name
                    )


class Rol(models.Model):
    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('trabajador', 'Trabajador'),
        ('cliente', 'Cliente'),
    ]

    nombre = models.CharField(max_length=15, unique=True, choices=ROL_CHOICES)
    permisos = models.ManyToManyField(Permiso)

    def __str__(self):
        return self.get_nombre_display()

    class Meta:
        verbose_name_plural = 'roles'


class CustomUserManager(UserManager):
    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        admin_role, created = Rol.objects.get_or_create(nombre='admin')
        extra_fields['roles'] = admin_role

        return self._create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(primary_key=True, unique=True)
    username = models.CharField(
        'Usuario', max_length=30, unique=True, validators=[
            validators.RegexValidator(
                re.compile('^[\w.@+-]+$'),
                'ingrese un nombre de usuario valido '
                'Este valor debe contener solo letras, números '
                'excepto: @/./+/-/_.',
                'invalid'
            )
        ],
        help_text='Un nombre corto que sera usado'+
                  ' para identificarlo de forma unica en la plataforma.'
    )
    name = models.CharField('Nombre', max_length=20)
    apellidos = models.CharField('Apellidos', max_length=30)
    email = models.EmailField('Email', unique=True)
    is_staff = models.BooleanField('Admin', default=False)
    is_active = models.BooleanField('Ativo', default=True)
    date_joined = models.DateTimeField('Data de Entrada', auto_now_add=True)
    roles = models.ForeignKey(Rol, on_delete=models.CASCADE)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.name or self.username

    def get_full_name(self):
        return str(self)

    def get_short_name(self):
        return str(self).split(' ')[0]


#ESTA FUNCION HACE QUE CUANDO SE GUARDE UN USUARIO ESTE TENGA EL ROL POR DEFECTO DE CLIENTE
@receiver(pre_save, sender=User)
def assign_default_role(sender, instance, **kwargs):
    if not instance.roles:
        default_role, created = Rol.objects.get_or_create(nombre='cliente')
        instance.roles = default_role

#ESTA FUNCION HACE QUE SI EL USUARIO CAMBIA SU ROL A ADMINISTRADOR SEA LO MISMO QUE UN SUPER USUARIO
@receiver(pre_save, sender=User)
def update_is_staff(sender, instance, **kwargs):
    if instance.roles and instance.roles.nombre == 'admin':
        instance.is_staff = True
    else:
        instance.is_staff = False


