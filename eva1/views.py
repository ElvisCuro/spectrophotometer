from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Mediciones

# Variables globales para almacenar los datos del ESP32
mediciones = {
    'valor': 0,
    'voltaje': 0.0,
    'voltaje_corregido': 0.0,
    'id_experimento':0.0,
    'absorbancia': 0.0  # Añadimos el valor de absorbancia
}

@csrf_exempt
def home_view(request):
    if request.method == 'POST':
        # Asegúrate de obtener y convertir los datos correctamente
        mediciones['valor'] = float(request.POST.get('valor', 0))  # Convertir a float
        mediciones['voltaje'] = float(request.POST.get('voltaje', 0.0))  # Convertir a float
        mediciones['voltaje_corregido'] = float(request.POST.get('voltaje_corregido', 0.0))  # Convertir a float
        mediciones['absorbancia'] = float(request.POST.get('absorbancia', 0.0))  # Convertir a float
        mediciones['id_experimento']= float(request.POST.get('id_experimento',0.0))

        # Guardar los datos en la base de datos
        Mediciones.objects.create(
            id_experimento=mediciones['id_experimento_id'],
            valor=mediciones['valor'],
            voltaje=mediciones['voltaje'],
            voltaje_corregido=mediciones['voltaje_corregido'],
            absorbancia=mediciones['absorbancia']  # Guardar absorbancia
        )

        return JsonResponse({'status': 'Datos recibidos correctamente'})  # Responder con un JSON al ESP32

    # Si es un GET, renderiza el template con los valores actuales
    return render(request, 'home.html', mediciones)

@csrf_exempt
def obtener_datos(request):
    # Devuelve los datos en formato JSON para que el frontend los actualice
    return JsonResponse(mediciones)
