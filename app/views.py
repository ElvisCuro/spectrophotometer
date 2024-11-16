from django.utils import timezone
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Experimento, Mediciones
import json

# Variables globales para almacenar los datos del ESP32
mediciones = {
    'valor': 0,
    'voltaje': 0.0,
    'voltaje_corregido': 0.0,
    'id_experimento': 0,
    'absorbancia': 0.0,
    'concentracion':0,
}

@csrf_exempt
def home_view(request):
    # Obtener todos los experimentos para el dropdown
    experimentos = Experimento.objects.all().order_by('-fecha_inicio')
    
    # Obtener el experimento seleccionado del query parameter
    experimento_seleccionado = None
    mediciones_experimento = None
    page_obj = None
    
    if 'id_experimento' in request.GET:
        experimento_id = request.GET.get('id_experimento')
        experimento_seleccionado = get_object_or_404(Experimento, id_experimento=experimento_id)
        mediciones_lista = Mediciones.objects.filter(
            id_experimento=experimento_seleccionado
        ).order_by('-fecha')
        
        # Configurar la paginación
        paginator = Paginator(mediciones_lista, 20)  # 20 mediciones por página
        page_number = request.GET.get('page', 1)
        
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        
        mediciones_experimento = page_obj

    if request.method == 'POST':
        try:
            mediciones['valor'] = float(request.POST.get('valor', 0))
            mediciones['voltaje'] = float(request.POST.get('voltaje', 0.0))
            mediciones['voltaje_corregido'] = float(request.POST.get('voltaje_corregido', 0.0))
            mediciones['absorbancia'] = float(request.POST.get('absorbancia', 0.0))
            mediciones['id_experimento'] = int(request.POST.get('id_experimento'))
            mediciones['concentracion']=int(request.POST.get('concentracion'))

            experimento_instance = get_object_or_404(
                Experimento, 
                id_experimento=mediciones['id_experimento']
            )

            Mediciones.objects.create(
                id_experimento=experimento_instance,
                valor=mediciones['valor'],
                voltaje=mediciones['voltaje'],
                voltaje_corregido=mediciones['voltaje_corregido'],
                concentracion=mediciones['concentracion'],
                absorbancia=mediciones['absorbancia'],
            )
            return JsonResponse({'status': 'Datos recibidos correctamente'})
            
        except ValueError:
            return JsonResponse({'status': 'Error: Datos no válidos'}, status=400)

    # Contexto para el template
    context = {
        'valor': mediciones['valor'],
        'voltaje': mediciones['voltaje'],
        'voltaje_corregido': mediciones['voltaje_corregido'],
        'absorbancia': mediciones['absorbancia'],
        'id_experimento': mediciones['id_experimento'],
        'experimentos': experimentos,
        'experimento_seleccionado': experimento_seleccionado,
        'mediciones': mediciones_experimento,
        'page_obj': page_obj,
        'concentracion':mediciones['concentracion'],
    }
    
    return render(request, 'home.html', context)

@csrf_exempt
def obtener_datos(request):
    return JsonResponse(mediciones)

@csrf_exempt
def crear_experimento(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            nombre_experimento = data.get('nombre', '').strip()
            descripcion = data.get('descripcion', '').strip()
            
            if not nombre_experimento:
                return JsonResponse({
                    'status': 'Error: El nombre del experimento es requerido'
                }, status=400)

            nuevo_experimento = Experimento.objects.create(
                nombre_experimento=nombre_experimento,
                descripcion=descripcion,
                fecha_inicio=timezone.now(),
            )
            
            return JsonResponse({
                'status': "Nuevo experimento creado con éxito",
                'id_experimento': nuevo_experimento.id_experimento
            })
            
        except json.JSONDecodeError:
            return JsonResponse({
                'status': 'Error: Datos JSON inválidos'
            }, status=400)
            
    return JsonResponse({
        'status': 'Error: Método no permitido'
    }, status=405)