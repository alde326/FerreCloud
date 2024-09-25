import datetime
from django_cron import CronJobBase, Schedule

class CrearCostosFrecuentesCronJob(CronJobBase):
    RUN_AT_TIMES = ['00:00']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'myapp.crear_costos_frecuentes'  # Un identificador único para la tarea

    def do(self):
        from .models import Costos, CostosFrecuentes  # Mover la importación aquí

        # Verificar si es el primer día del mes
        today = datetime.date.today()
        if today.day == 1:
            # Obtener todos los costos frecuentes que no están eliminados
            costos_frecuentes = CostosFrecuentes.objects.filter(eliminado=False)

            # Crear un registro nuevo en Costos por cada costo frecuente
            for costo_frecuente in costos_frecuentes:
                Costos.objects.create(
                    nombre=costo_frecuente.nombre,
                    valor=costo_frecuente.valor,
                    fecha=today,
                    descripcion=costo_frecuente.descripcion,
                    frecuente=True,  # Marcar como frecuente
                    eliminado=False
                )
