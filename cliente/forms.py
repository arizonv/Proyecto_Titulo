from django import forms
from .models import Reserva
from django.utils import timezone
import datetime
from .models import Cliente
import calendar
from datetime import timedelta
from django.core.exceptions import ValidationError


class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ['rut','sexo']

    def clean_rut(self):
        rut = self.cleaned_data['rut']
        rut = rut.upper()  # Convertir el Rut a mayúsculas
        rut = rut.replace(".", "")  # Eliminar los puntos del Rut
        rut = rut.replace("-", "")  # Eliminar el guión del Rut

        # Extraer el dígito verificador y el número base del Rut
        dv = rut[-1]
        rut_base = rut[:-1]

        # Validar que el número base del Rut sea un entero
        try:
            int(rut_base)
        except ValueError:
            raise forms.ValidationError('El Rut ingresado no es válido.')

        # Calcular el dígito verificador esperado
        suma = 0
        multiplicador = 2
        for digito in reversed(rut_base):
            suma += int(digito) * multiplicador
            multiplicador += 1
            if multiplicador == 8:
                multiplicador = 2

        resto = suma % 11
        dv_esperado = str(11 - resto) if resto > 1 else '0'

        # Comparar el dígito verificador calculado con el ingresado
        if dv != dv_esperado:
            raise forms.ValidationError('El Rut ingresado no es válido.')

        return rut



class ReservaForm(forms.ModelForm):
    dia = forms.DateField(widget=forms.DateInput(attrs={'class': 'datepicker'}))

    class Meta:
        model = Reserva
        fields = ['dia']
        
    def clean_dia(self):
        dia = self.cleaned_data.get('dia')
        fecha_actual = timezone.now().date()
        fecha_limite = fecha_actual + timedelta(days=1)
        fecha_maxima = fecha_actual + timedelta(weeks=2) 

        if dia < fecha_limite:
            raise forms.ValidationError("Debes realizar la reserva con al menos un día de anticipación.")
        if dia < fecha_actual:
            raise forms.ValidationError("No puedes reservar una fecha pasada.")
        if dia > fecha_maxima:
            raise forms.ValidationError("No puedes reservar con más de dos semanas de anticipación.")

        if dia.weekday() == calendar.SUNDAY:
            raise forms.ValidationError("Los domingos no se pueden reservar.")
    
        agenda = self.cleaned_data.get('agenda')
        if Reserva.objects.filter(agenda=agenda, dia=dia).exists():
            raise forms.ValidationError("La fecha ya está reservada.")

        return dia





