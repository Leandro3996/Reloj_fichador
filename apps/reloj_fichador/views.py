from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import Operario, Entrada, Salida


def home(request):
    return render(request, 'reloj_fichador/home.html')

def registrar_entrada(request):
    if request.method == 'POST':
        dni = request.POST['dni']
        operario = get_object_or_404(Operario, dni=dni)
        Entrada.objects.create(operario=operario, fecha=timezone.now(), hora=timezone.now())
        return redirect('reloj_fichador:lista_registros')
    return render(request, 'reloj_fichador/registrar_entrada.html')

def registrar_entrada_transitoria(request):
    if request.method == 'POST':
        dni = request.POST['dni']
        operario = get_object_or_404(Operario, dni=dni)
        Entrada.objects.create(operario=operario, fecha=timezone.now(), hora=timezone.now())
        return redirect('reloj_fichador:lista_registros')
    return render(request, 'reloj_fichador/registrar_entrada_transitoria.html')

def registrar_salida_transitoria(request):
    if request.method == 'POST':
        dni = request.POST['dni']
        operario = get_object_or_404(Operario, dni=dni)
        Salida.objects.create(operario=operario, fecha=timezone.now(), hora=timezone.now())
        return redirect('reloj_fichador:lista_registros')
    return render(request, 'reloj_fichador/registrar_salida_transitoria.html')

def registrar_salida(request):
    if request.method == 'POST':
        dni = request.POST['dni']
        operario = get_object_or_404(Operario, dni=dni)
        Salida.objects.create(operario=operario, fecha=timezone.now(), hora=timezone.now())
        return redirect('reloj_fichador:lista_registros')
    return render(request, 'reloj_fichador/registrar_salida.html')

def lista_registros(request):
    entradas = Entrada.objects.all()
    salidas = Salida.objects.all()
    return render(request, 'reloj_fichador/lista_registros.html', {'entradas': entradas, 'salidas': salidas})
