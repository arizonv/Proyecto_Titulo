from django.contrib import admin
from .models import Cliente,Reserva,Boleta,Ticket


class TicketAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'codigo', 'fecha_envio')
    list_filter = ('cliente',)

class ClienteAdmin(admin.ModelAdmin):
    list_display = ('user', 'rut', 'sexo')
    list_filter = ('sexo',)

class ReservaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'agenda', 'dia')
    list_filter = ('agenda__cancha__numeracion','agenda__cancha__tipo')  # Filtrar por numeración de cancha

class BoletaAdmin(admin.ModelAdmin):
    list_display = ('cliente', 'reserva', 'fecha_emision')
    list_filter = ('fecha_emision',)


admin.site.register(Ticket, TicketAdmin)
admin.site.register(Cliente, ClienteAdmin)
admin.site.register(Reserva, ReservaAdmin)
admin.site.register(Boleta, BoletaAdmin)
