from Configuracion.models import Organizacion

def organizacion_info(request):
    try:
        # Asumiendo que solo hay una organización
        organizacion = Organizacion.objects.first()
    except Organizacion.DoesNotExist:
        organizacion = None
    return {'organizacion': organizacion}