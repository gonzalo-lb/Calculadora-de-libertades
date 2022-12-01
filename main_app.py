from libcalc import ComputoPenaTemporal
from libcalc_methods import *

if __name__ == '__main__':

    # SOLICITA AL USUARIO SE INDIQUE TIPO DE PENA A CALCULAR    

    user_input = Preguntas_Input()
    
    computo = ComputoPenaTemporal(fechaDelHecho=user_input._fecha_del_hecho, 
    fechaDeDetencion=user_input._fecha_de_detencion,
    montoDePena=user_input._monto_de_pena,
    otrasDetenciones=user_input._otras_detenciones,
    estimuloEducativo=user_input._estimulo_educativo,
    fechaInicioEjecucion=user_input._fecha_inicio_ejecucion,
    fechaCalificacionBUENO=user_input._fecha_calificacion_BUENO,
    fechaIngresoPeriodoDePrueba=user_input._fecha_ingreso_periodo_de_prueba,
    fechaCalificacionEJEMPLAR=user_input._fecha_calificacion_EJEMPLAR,
    vuelveARestarOtrasDetencionesyAplicar140enST=user_input._vuelve_a_restar_otras_detenciones_y_140_en_ST)