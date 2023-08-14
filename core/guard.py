from django.shortcuts import render
import requests

#EN PRODUCCION ESTA VALIDACION PERMITE QUE CUANDO SE INGRESE RUTAS NO CONOCIDAS ENVIE SIEMPRE EL HOME
def handler404(request, exception):
    return render(request, 'home.html')


def handler505(request, exception):
    return render(request, 'home.html')