from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models.signals import post_migrate
from django.dispatch import receiver
from datetime import time



class TipoCancha(models.Model):
    nombre = models.CharField(max_length=50)
    precio = models.DecimalField(max_digits=8, decimal_places=0)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name = _('Tipo de Cancha')
        verbose_name_plural = _('Tipos de Canchas')

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

    def __str__(self):
        return f'Cancha {self.numeracion}'

    class Meta:
        verbose_name = _('Cancha')
        verbose_name_plural = _('Canchas')

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

    #ESTA FUNCION GENERA LOS HORARIOS AUTOMATICAMENTE POR DEFECTO RELLENA LA CLASE HORARIO
    @classmethod
    def generar_horarios_default(cls):
        horarios_default_am = [
            (time(9, 0), time(10, 0)),
            (time(10, 0), time(11, 0)),
            (time(11, 0), time(12, 0)),
        ]

        horarios_default_pm = [
            (time(12, 0), time(13, 0)),
            (time(16, 0), time(17, 0)),
            (time(17, 0), time(18, 0)),
            (time(18, 0), time(19, 0)),
            (time(19, 0), time(20, 0)),
            (time(20, 0), time(21, 0)),
            (time(21, 0), time(22, 0)),
        ]

        for inicio, fin in horarios_default_am:
            horario, created = cls.objects.get_or_create(
                hora_inicio=inicio,
                hora_fin=fin,
                meridiem=cls.AM
            )
            if created:
                print(f'Se creó el horario AM: {horario}')

        for inicio, fin in horarios_default_pm:
            horario, created = cls.objects.get_or_create(
                hora_inicio=inicio,
                hora_fin=fin,
                meridiem=cls.PM
            )
            if created:
                print(f'Se creó el horario PM: {horario}')
    
    def __str__(self):
        return f'{self.hora_inicio.strftime("%I:%M %p")} - {self.hora_fin.strftime("%I:%M %p")}'

class Agenda(models.Model):
    cancha = models.ForeignKey(Cancha, on_delete=models.CASCADE)
    horario = models.ForeignKey(Horario, on_delete=models.CASCADE)
    disponible = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.cancha.tipo} {self.cancha} - {self.horario}'

    class Meta:
        verbose_name = _('Agenda')
        verbose_name_plural = _('Agendas')
        unique_together = ('cancha', 'horario')

#SE LAMA LA FUNCION GENERAR HORARIOS
@receiver(post_migrate)
def generar_horarios_default(sender, **kwargs):
    if sender.name == 'cliente': 
        Horario.generar_horarios_default()