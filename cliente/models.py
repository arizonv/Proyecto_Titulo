from django.db import models
from servicio.models import Agenda
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from servicio.models import Agenda



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

    def __str__(self):
        return f'{self.user.username}'

class Reserva(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    agenda = models.ForeignKey(Agenda, on_delete=models.CASCADE)
    dia = models.DateField()
    ESTADO_CHOICES = [
        ('disponible', 'Disponible'),
        ('pendiente', 'Pendiente'),
        ('finalizada', 'Finalizada'),
    ]
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='disponible')

    class Meta:
        unique_together = ('agenda', 'cliente', 'dia')

    def __str__(self):
        formatted_date = self.dia.strftime('%d-%m-%Y')
        return f"Reserva de {self.cliente} para el {formatted_date}, {self.agenda.cancha} {self.agenda.horario}"


#CREA UNA BOLETA AUTOMATICAMENTE CUANDO SE CREA UNA RESERVA
@receiver(post_save, sender=Reserva)
def crear_boleta(sender, instance, created, **kwargs):
    if created or (not instance._state.adding and instance.estado == 'pendiente'):
        # Obtén el tipo de cancha asociado a la reserva
        tipo_cancha = instance.agenda.cancha.tipo
        # Calcula la mitad del precio del tipo de cancha
        mitad_precio = tipo_cancha.precio / 2
        # Crea una instancia de Boleta con el valor calculado
        Boleta.objects.create(cliente=instance.cliente, reserva=instance, total=mitad_precio)


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

    def __str__(self):
        return f'Boleta para {self.cliente} emitida el {self.fecha_emision}'
