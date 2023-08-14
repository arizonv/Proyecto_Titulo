from django.urls import path
from .views import (
    CanchaListView,
    CanchaCreateView,
    CanchaUpdateView,
    CanchaDeleteView,
    TipoCanchaListView,
    TipoCanchaCreateView,
    TipoCanchaUpdateView,
    TipoCanchaDeleteView,
    AgendaListView,
    AgendaCreateView,
    AgendaUpdateView,
    AgendaDeleteView,
    PreReserva,
)

app_name = 'servicio'

urlpatterns = [
    # Cancha URLs
    path('listar/', CanchaListView.as_view(), name='cancha-listar'),
    path('agregar/', CanchaCreateView.as_view(), name='cancha-crear'),
    path('actualizar/<int:pk>/', CanchaUpdateView.as_view(), name='cancha-actualizar'),
    path('eliminar/<int:pk>/', CanchaDeleteView.as_view(), name='cancha-eliminar'),

    # TipoCancha URLs
    path('tipo/listar/', TipoCanchaListView.as_view(), name='tipo-listar'),
    path('tipo/agregar/', TipoCanchaCreateView.as_view(), name='tipo-agregar'),
    path('tipo/actualizar/<int:pk>/', TipoCanchaUpdateView.as_view(), name='tipo-actualizar'),
    path('tipo/eliminar/<int:pk>/', TipoCanchaDeleteView.as_view(), name='tipo-eliminar'),

    # Agenda URLs
    path('agenda/listar/', AgendaListView.as_view(), name='agenda-listar'),
    path('agenda/agregar/', AgendaCreateView.as_view(), name='agenda-agregar'),
    path('agenda/actualizar/<int:pk>/', AgendaUpdateView.as_view(), name='agenda-actualizar'),
    path('agenda/eliminar/<int:pk>/', AgendaDeleteView.as_view(), name='agenda-eliminar'),

    # PreReserva URL
    path('agenda/reserva/', PreReserva.as_view(), name='agenda-reserva'),
]
