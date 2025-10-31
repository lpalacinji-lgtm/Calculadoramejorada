from datetime import datetime, timedelta, date
import math

# ============================================================
# 🔧 FUNCIÓN AUXILIAR: CÁLCULO DE DISTRIBUCIÓN MENSUAL
# ============================================================
def calcular_distribucion_mensual(fecha_inicio, duracion_dias):
    """
    Calcula cuántos días del tratamiento pertenecen al mes actual
    y cuántos al siguiente mes.
    """

    # Asegurar que sea tipo date
    if isinstance(fecha_inicio, datetime):
        fecha_inicio = fecha_inicio.date()

    # Fecha final del tratamiento
    fecha_fin = fecha_inicio + timedelta(days=duracion_dias - 1)

    # Último día del mes de inicio
    if fecha_inicio.month < 12:
        fin_mes = date(fecha_inicio.year, fecha_inicio.month + 1, 1) - timedelta(days=1)
    else:
        fin_mes = date(fecha_inicio.year, 12, 31)

    # Días en cada mes
    if fecha_fin <= fin_mes:
        dias_mes_actual = duracion_dias
        dias_mes_siguiente = 0
    else:
        dias_mes_actual = (fin_mes - fecha_inicio).days + 1
        dias_mes_siguiente = duracion_dias - dias_mes_actual

    return dias_mes_actual, dias_mes_siguiente, fecha_fin


# ============================================================
# 💊 CÁLCULO PARA TABLETAS
# ============================================================
def calcular_tabletas(frecuencia_horas, duracion_dias, dosis_toma, unidades_presentacion, fecha_orden, inicio_mismo_dia):
    """
    Calcula dosis totales, número de presentaciones y fechas de dispensación para tabletas.
    """

    tomas_por_dia = 24 / frecuencia_horas
    total_tomas = tomas_por_dia * duracion_dias
    total_tabletas = total_tomas * dosis_toma

    presentaciones_necesarias = math.ceil(total_tabletas / unidades_presentacion)

    # Fecha de inicio y finalización
    fecha_inicio = fecha_orden if inicio_mismo_dia else fecha_orden + timedelta(days=1)
    dias_mes_actual, dias_mes_siguiente, fecha_fin = calcular_distribucion_mensual(fecha_inicio, duracion_dias)

    # Cálculo mensual
    tabletas_mes_actual = round(dosis_toma * (24 / frecuencia_horas) * dias_mes_actual, 1)
    tabletas_mes_siguiente = round(total_tabletas - tabletas_mes_actual, 1)

    resultados = {
        "Total de tomas": round(total_tomas, 1),
        "Total de tabletas": round(total_tabletas, 1),
        "Presentaciones necesarias": presentaciones_necesarias,
        "Fecha de inicio": fecha_inicio.strftime("%Y-%m-%d"),
        "Fecha de finalización": fecha_fin.strftime("%Y-%m-%d"),
        "Días este mes": dias_mes_actual,
        "Días próximo mes": dias_mes_siguiente,
        "Tabletas este mes": tabletas_mes_actual,
        "Tabletas próximo mes": tabletas_mes_siguiente
    }

    return resultados


# ============================================================
# 💉 CÁLCULO PARA AMPOLLAS
# ============================================================
def calcular_ampollas(frecuencia_horas, duracion_dias, dosis_inyeccion, volumen_ampolla, esterilidad_horas, fecha_orden, inicio_mismo_dia):
    """
    Calcula número de ampollas necesarias y aprovechamiento según esterilidad.
    """

    tomas_por_dia = 24 / frecuencia_horas
    total_inyecciones = tomas_por_dia * duracion_dias
    volumen_total = total_inyecciones * dosis_inyeccion

    ampollas_necesarias = math.ceil(volumen_total / volumen_ampolla)

    # Control de esterilidad
    horas_totales = duracion_dias * 24
    reaperturas = math.ceil(horas_totales / esterilidad_horas)

    # Fecha de inicio y finalización
    fecha_inicio = fecha_orden if inicio_mismo_dia else fecha_orden + timedelta(days=1)
    dias_mes_actual, dias_mes_siguiente, fecha_fin = calcular_distribucion_mensual(fecha_inicio, duracion_dias)

    # Distribución mensual
    inyecciones_mes_actual = round((24 / frecuencia_horas) * dias_mes_actual, 1)
    inyecciones_mes_siguiente = round(total_inyecciones - inyecciones_mes_actual, 1)

    volumen_mes_actual = round(inyecciones_mes_actual * dosis_inyeccion, 2)
    volumen_mes_siguiente = round(volumen_total - volumen_mes_actual, 2)

    ampollas_mes_actual = math.ceil(volumen_mes_actual / volumen_ampolla)
    ampollas_mes_siguiente = math.ceil(volumen_mes_siguiente / volumen_ampolla)

    resultados = {
        "Total de inyecciones": round(total_inyecciones, 1),
        "Volumen total (ml)": round(volumen_total, 2),
        "Ampollas necesarias": ampollas_necesarias,
        "Reaperturas por esterilidad": reaperturas,
        "Fecha de inicio": fecha_inicio.strftime("%Y-%m-%d"),
        "Fecha de finalización": fecha_fin.strftime("%Y-%m-%d"),
        "Días este mes": dias_mes_actual,
        "Días próximo mes": dias_mes_siguiente,
        "Ampollas este mes": ampollas_mes_actual,
        "Ampollas próximo mes": ampollas_mes_siguiente,
        "Volumen este mes (ml)": volumen_mes_actual,
        "Volumen próximo mes (ml)": volumen_mes_siguiente
    }

    return resultados
