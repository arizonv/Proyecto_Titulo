from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from .models import Reserva, Agenda, Cliente,Ticket
from django.contrib import messages
from .forms import ReservaForm, ClienteForm
from django.contrib.auth.decorators import login_required
import json
from django.utils import timezone
from datetime import datetime
import requests
from django.conf import settings
from django.urls import reverse
import random
import string
from .transbank import crear_transaccion

#cliente
def cliente_list(request):
    clientes = Cliente.objects.all()
    context = {'clientes': clientes}
    return render(request, 'cliente/listar.html', context)

#ESTA FUNCION ES PARA RECORDAR RELLENAR TODOS SUS DATOS
def crear_cliente(request):
    cliente_existente = Cliente.objects.filter(user=request.user).first()  # Verificar si existe un cliente para el usuario actual

    if cliente_existente:  # Si el cliente existe, rellenar los datos en el formulario
        form = ClienteForm(instance=cliente_existente)
    else:
        form = ClienteForm()

    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente_existente)  # Pasar la instancia existente al formulario en caso de edición

        try:
            if form.is_valid():
                cliente = form.save(commit=False)
                cliente.user = request.user
                cliente.save()
                return redirect('servicio:agenda-reserva')
        except Exception as e:
            error_message = str(e)
            form.add_error(None, error_message)

    return render(request, 'cliente/agregar.html', {'form': form})

def cliente_update(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        form = ClienteForm(request.POST, instance=cliente)
        if form.is_valid():
            form.save()
            return redirect('cliente:cliente_list')
    else:
        form = ClienteForm(instance=cliente)
    return render(request, 'cliente/modificar.html', {'form': form})

def cliente_delete(request, pk):
    cliente = get_object_or_404(Cliente, pk=pk)
    if request.method == 'POST':
        cliente.delete()
        messages.success(request, 'Cliente deleted successfully.')
        return redirect(to='cliente_list')
    else:
        messages.warning(request, 'Invalid request.')
        return redirect(to='cliente_list')

#reservas ( las reservas no se eliminan , solo de lista,crean,modifican)
def reserva_list(request):
    reservas = Reserva.objects.all()
    today = timezone.now().date()
    return render(request, 'reserva/listar.html', {'reservas': reservas, 'today': today})

def listar_reservas_usuario(request):
    try:
        cliente = request.user.cliente
    except Cliente.DoesNotExist:
        messages.warning(request, 'Necesitas crear un Cliente para acceder a esta página')
        return redirect(reverse('cliente:cliente_create'))

    reservas = Reserva.objects.filter(cliente=cliente)
    return render(request, 'reserva/reservas_usuario.html', {'reservas': reservas})


def crear_reserva(request, agenda_id):
    agenda = get_object_or_404(Agenda, id=agenda_id)
    form = ReservaForm(initial={'agenda': agenda})

    try:
        cliente = request.user.cliente
    except Cliente.DoesNotExist:
        messages.warning(request, 'Necesitas los DATOS COMPLEMENTARIOS para realizar una reserva')
        return redirect(to='cliente:cliente_create')

    if request.method == 'POST':
        form = ReservaForm(request.POST)
        if form.is_valid():
            reserva = form.save(commit=False)
            reserva.agenda = agenda
            reserva.cliente = cliente
            if Reserva.objects.filter(agenda=agenda, dia=reserva.dia).exists():
                messages.error(request, 'La fecha ya está reservada.')
            else:
                amount = agenda.cancha.tipo.precio / 2
                transaction_data = crear_transaccion(request, agenda, amount)
                if transaction_data:
                    #guardar reserva en la sesion
                    reserva_session = request.session['reserva_actual'] = reserva
                    print(f'reserva actual: {reserva_session}')
                    return render(request, 'reserva/crear.html', {'transaction_data': transaction_data})
                else:
                    return render(request, 'transbank/error.html')

    dias_reservados = Reserva.objects.filter(agenda__cancha=agenda.cancha, agenda__horario=agenda.horario).values_list('dia', flat=True)
    dias_reservados_str = ', '.join([dia.strftime('%d/%m/%Y') for dia in dias_reservados])
    dias_reservados_json = json.dumps(dias_reservados_str)

    contexto = {
        'form': form,
        'agenda': agenda,
        'dias_reservados_json': dias_reservados_json,
    }
    return render(request, 'reserva/crear.html', contexto)
#Modificar reserva

#Ticket
#Boleta


