from django.shortcuts import render
import requests


def handler404(request, exception):
    return render(request, 'home.html')


def handler505(request, exception):
    return render(request, 'home.html')