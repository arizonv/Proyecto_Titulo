#ESTE MODELO SOLO SE USA PARA CREAR EL DDL Y PODER OBTENER EL DIAGRAMA 
#######################################################################
#######################################################################
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



class Rol(models.Model):
    ROL_CHOICES = [
        ('admin', 'Administrador'),
        ('trabajador', 'Trabajador'),
        ('cliente', 'Cliente'),
    ]
    nombre = models.CharField(max_length=15, unique=True, choices=ROL_CHOICES)
    permisos = models.ManyToManyField(Permiso, through='RolPermiso')



class RolPermiso(models.Model):
    rol = models.ForeignKey(Rol, on_delete=models.CASCADE)
    permiso = models.ForeignKey(Permiso, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('rol', 'permiso')



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



class Cliente(models.Model):
    SEXO = [
        ('F', 'Femenino'),
        ('M', 'Masculino'),
    ]
    user = models.OneToOneField(
        'accounts.User',
        verbose_name='Usuario',
        on_delete=models.CASCADE
    )
    rut = models.CharField(max_length=10)
    sexo = models.CharField(max_length=10, choices=SEXO)

class Reserva(models.Model):
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('pendiente', 'Pendiente'),
        ('finalizada', 'Finalizada'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible')
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
    dia = models.DateField()



class Ticket(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    codigo = models.CharField(max_length=10)
    fecha_envio = models.DateTimeField(auto_now_add=True)
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)



class Boleta(models.Model):
    fecha_emision = models.DateTimeField(default=timezone.now)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    reserva = models.ForeignKey(Reserva, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2) 


class TipoCancha(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=8, decimal_places=0)
    descripcion = models.TextField()


class Cancha(models.Model):
    NUMERACION_CHOICES = [
        ('1', 'Cancha 1'),
        ('2', 'Cancha 2'),
        ('3', 'Cancha 3'),
        ('4', 'Cancha 4'),
        ('5', 'Cancha 5'),
        ('6', 'Cancha 6'),
        ('7', 'Cancha 7'),
        ('8', 'Cancha 8'),
    ]
    numeracion = models.CharField(max_length=10, choices=NUMERACION_CHOICES)
    tipo = models.ForeignKey(TipoCancha, on_delete=models.CASCADE, related_name='canchas')


class Horario(models.Model):
    AM = 'AM'
    PM = 'PM'
    MERIDIEM_CHOICES = [
        (AM, 'AM'),
        (PM, 'PM'),
    ]
    hora_inicio = models.TimeField()
    hora_fin = models.TimeField()
    meridiem = models.CharField(max_length=2, choices=MERIDIEM_CHOICES, default=PM)
    


class Agenda(models.Model):
    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE)
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)
    disponible = models.BooleanField(default=True)


