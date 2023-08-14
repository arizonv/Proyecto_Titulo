import requests
from django.contrib import messages
import random
import string
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required

from django.shortcuts import render, get_object_or_404
from .models import Ticket, Cliente



def create_transaction(request):
    # Lógica para crear una transacción en Transbank
    url = 'https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions'
    headers = {
        'Tbk-Api-Key-Id': '597055555532',
        'Tbk-Api-Key-Secret': '579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C',
        'Content-Type': 'application/json'
    }
    data = {
        "buy_order": "ordenCompra12345678",
        "session_id": "sesion1234557545",
        "amount": 10000,
        "return_url": "http://www.comercio.cl/webpay/retorno"
    }
    
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        transaction_data = response.json()
        return render(request, 'transbank/payment.html', {'transaction_data': transaction_data})
    else:
        # Manejar el error en caso de que la transacción no se pueda crear
        return render(request, 'transbank/error.html')


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



#nota: 