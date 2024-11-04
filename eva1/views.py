from datetime import timezone
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Experimento, Mediciones

import json

# Variables globales para almacenar los datos del ESP32
mediciones = {
    'valor': 0,
    'voltaje': 0.0,
    'voltaje_corregido': 0.0,
    'id_experimento':0,
    'absorbancia': 0.0  # Añadimos el valor de absorbancia
}

@csrf_exempt
def home_view(request):
    if request.method == 'POST':
        try:
            mediciones['valor'] = float(request.POST.get('valor', 0))
            mediciones['voltaje'] = float(request.POST.get('voltaje', 0.0))
            mediciones['voltaje_corregido'] = float(request.POST.get('voltaje_corregido', 0.0))
            mediciones['absorbancia'] = float(request.POST.get('absorbancia', 0.0))
            mediciones['id_experimento'] = int(request.POST.get('id_experimento'))

            # Obtener la concentración y utilizar la última guardada si no se proporciona una nueva
            nueva_concentracion = request.POST.get('concentracion')
            if nueva_concentracion:
                mediciones['concentracion'] = float(nueva_concentracion)
            else:
                ultima_medicion = Mediciones.objects.filter(id_experimento=mediciones['id_experimento']).order_by('-fecha').first()
                if ultima_medicion:
                    mediciones['concentracion'] = ultima_medicion.concentracion
        except ValueError:
            return JsonResponse({'status': 'Error: Datos no válidos'}, status=400)

        # Obtener la instancia del experimento sin cambiar el ID seleccionado
        try:
            experimento_instance = Experimento.objects.get(id_experimento=mediciones['id_experimento'])
        except Experimento.DoesNotExist:
            return JsonResponse({'status': 'Error: El experimento no existe'}, status=400)

        # Guardar la medición con el ID del experimento actual y la concentración
        Mediciones.objects.create(
            id_experimento=experimento_instance,
            valor=mediciones['valor'],
            voltaje=mediciones['voltaje'],
            voltaje_corregido=mediciones['voltaje_corregido'],
            concentracion=mediciones['concentracion'],
            absorbancia=mediciones['absorbancia']
        )

        return JsonResponse({'status': 'Datos recibidos correctamente'})

    # Si es un GET, renderiza el template con los valores actuales
    return render(request, 'home.html', mediciones)

@csrf_exempt
def obtener_datos(request):
    # Devuelve los datos en formato JSON para que el frontend los actualice
    return JsonResponse(mediciones)

@csrf_exempt
def crear_experimento(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        nombre_experimento = data.get('nombre_experimento', '').strip()
        descripcion = data.get('descripcion', '').strip()
        
        # Crear el nuevo experimento
        nuevo_experimento = Experimento.objects.create(
            nombre_experimento=nombre_experimento,
            descripcion=descripcion,
            fecha_inicio=timezone.now()
        )
        
        return JsonResponse({'status': 'Experimento creado correctamente', 'id_experimento': nuevo_experimento.id_experimento})

    return JsonResponse({'status': 'Error: Método no permitido'}, status=405)