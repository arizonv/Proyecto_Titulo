from django.urls import path

from . import transbank
from . import views
from .transbank import confirm_transaction

app_name = 'cliente'

urlpatterns = [
    path('list/', views.cliente_list, name='cliente_list'),
    path('create/', views.crear_cliente, name='cliente_create'),
    path('update/<int:pk>/', views.cliente_update, name='cliente_update'),
    path('delete/<int:pk>/', views.cliente_delete, name='cliente_delete'),

    path('reservas/', views.reserva_list, name='reserva_list'),
    path('reservas_user/', views.listar_reservas_usuario, name='listar_reservas_usuario'),
    path('reserva/crear/<int:agenda_id>/', views.crear_reserva, name='crear_reserva'),
    path('confirm-transaction/', confirm_transaction, name='confirm_transaction'),
    
]




