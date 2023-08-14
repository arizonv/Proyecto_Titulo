from django.contrib import admin
from .models import TipoCancha, Cancha, Agenda, Horario


@admin.register(TipoCancha)
class TipoCanchaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio', 'descripcion']
    list_filter = ['nombre']
    search_fields = ['nombre', 'descripcion']


@admin.register(Horario)
class HorarioAdmin(admin.ModelAdmin):
    list_display = ['hora_inicio','hora_fin','meridiem']
    search_fields = ['hora_inicio','hora_fin']


@admin.register(Cancha)
class CanchaAdmin(admin.ModelAdmin):
    list_display = ['numeracion', 'tipo']
    list_filter = ['tipo']
    search_fields = ['numeracion', 'tipo__nombre']


@admin.register(Agenda)
class AgendaAdmin(admin.ModelAdmin):
    list_display = ['cancha', 'tipo_cancha', 'horario', 'disponible']
    list_filter = ['cancha','cancha__tipo', 'horario']
    search_fields = ['cancha__tipo__nombre', 'cancha__numeracion', 'horario__horario']

    def tipo_cancha(self, obj):
        return obj.cancha.tipo.nombre
    tipo_cancha.short_description = 'Tipo de Cancha'


