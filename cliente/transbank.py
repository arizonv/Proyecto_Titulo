import requests
from django.contrib import messages
import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from .models import Reserva, Agenda, Cliente, Ticket
from django.utils import timezone
from datetime import datetime



# ESTE ES UNA RCHIVO APARTE QUE TIENE FUNCIONES DE VIEW LAS CUALES CONSUMEN LA API DE TRANSBANK 
def crear_transaccion(request, agenda, amount):
    BASE_URL = 'http://127.0.0.1:8000/'
    return_url = f"{BASE_URL}cliente/confirm-transaction/"

    url = 'https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions'
    headers = {
        'Tbk-Api-Key-Id': '597055555532',
        'Tbk-Api-Key-Secret': '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C',
        'Content-Type': 'application/json'
    }

    digits = string.digits
    buy_order = "00-" + ''.join(random.choice(digits) for _ in range(13))

    session_id = str(request.session.session_key)
    
    data = {
        "buy_order": buy_order,
        "session_id": session_id,
        "amount": int(amount),
        "return_url": return_url
    }

    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        transaction_data = response.json()
        return transaction_data
    else:
        return None

def confirm_transaction(request):
    token = request.GET.get('token_ws')  # Obtener el valor del parámetro 'token_ws' de la URL
    if token:
        # Lógica para confirmar una transacción en Transbank
        url = f'https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions/{token}'
        headers = {
            'Tbk-Api-Key-Id': '597055555532',
            'Tbk-Api-Key-Secret': '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C',
            'Content-Type': 'application/json'
        }
        response = requests.put(url, headers=headers)
        if response.status_code == 200:
            transaction_data = response.json()
            # Recuperar la reserva desde la sesión
            reserva = request.session.get('reserva_actual')
            if reserva:
                # HACE FALTA VALIDAR SI LA RESPUESTA DE LA API DE TRANSBANK DE CONFIRMACION (TARJETA) ES AUTORIZADA O FAILED
                # Cambiar el estado de la reserva a 'pendiente'
                reserva.estado = 'pendiente'
                reserva.save()
                messages.success(request, 'Reserva Exitosa!')
                print(f'reserva recibida: {reserva}')
                # Eliminar la reserva de la sesión
                del request.session['reserva_actual']
                return render(request, 'transbank/confirmation.html', {'transaction_data': transaction_data})
        else:
            # Manejar el error en caso de que la transacción no se pueda confirmar
            return render(request, 'transbank/error.html')
    else:
        # Manejar el caso en que no se haya proporcionado el parámetro 'token_ws'
        return render(request, 'transbank/error.html')


