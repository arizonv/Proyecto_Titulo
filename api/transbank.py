from rest_framework.views import APIView
from rest_framework.response import Response
import requests


#EN ESTE ARCHIVO SE EXPONE LA API DE TRANSBANK DESDE DJANGO PARA SER UTILIZADA

# MÉTODO QUE CREA LA CABECERA SOLICITADA POR TRANSBANK EN UN REQUEST (SOLICITUD)
def header_request_transbank():
    headers = {
        "Authorization": "Token",
        "Tbk-Api-Key-Id": "597055555532",
        "Tbk-Api-Key-Secret": "579B532A7440BB0C9079DED94D31EA1615BACEB56610332264630D42D0A36B1C",
        "Content-Type": "application/json",
        "Access-Control-Allow-Origin": "*",
        "Referrer-Policy": "origin-when-cross-origin",
    }
    return headers

class TransbankCreateView(APIView):
    def post(self, request):
        data = request.data
        url = "https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions"
        headers = header_request_transbank()
        response = requests.post(url, json=data, headers=headers)
        return Response(response.json())

class TransbankCommitView(APIView):
    def put(self, request, tokenws):
        url = f"https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions/{tokenws}"
        headers = header_request_transbank()
        response = requests.put(url, headers=headers)
        return Response(response.json())

class TransbankReverseOrCancelView(APIView):
    def post(self, request, tokenws):
        data = request.data
        url = f"https://webpay3gint.transbank.cl/rswebpaytransaction/api/webpay/v1.2/transactions/{tokenws}/refunds"
        headers = header_request_transbank()
        response = requests.post(url, json=data, headers=headers)
        return Response(response.json())
