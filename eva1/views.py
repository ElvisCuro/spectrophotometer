from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import SensorData

# Variables globales para almacenar los datos del ESP32
sensor_data = {
    'valor': 0,
    'voltaje': 0.0,
    'voltaje_corregido': 0.0,
    'absorbancia': 0.0  # Añadimos el valor de absorbancia
}

@csrf_exempt
def home_view(request):
    if request.method == 'POST':
        # Asegúrate de obtener y convertir los datos correctamente
        sensor_data['valor'] = float(request.POST.get('valor', 0))  # Convertir a float
        sensor_data['voltaje'] = float(request.POST.get('voltaje', 0.0))  # Convertir a float
        sensor_data['voltaje_corregido'] = float(request.POST.get('voltaje_corregido', 0.0))  # Convertir a float
        sensor_data['absorbancia'] = float(request.POST.get('absorbancia', 0.0))  # Convertir a float

        # Guardar los datos en la base de datos
        SensorData.objects.create(
            valor=sensor_data['valor'],
            voltaje=sensor_data['voltaje'],
            voltaje_corregido=sensor_data['voltaje_corregido'],
            absorbancia=sensor_data['absorbancia']  # Guardar absorbancia
        )

        return JsonResponse({'status': 'Datos recibidos correctamente'})  # Responder con un JSON al ESP32

    # Si es un GET, renderiza el template con los valores actuales
    return render(request, 'home.html', sensor_data)

@csrf_exempt
def obtener_datos(request):
    # Devuelve los datos en formato JSON para que el frontend los actualice
    return JsonResponse(sensor_data)
