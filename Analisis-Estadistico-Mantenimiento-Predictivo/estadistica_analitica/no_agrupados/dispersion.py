import math
from . import tendencias

def rango(datos):
    if not datos:
        return 0.0
    ordenados = sorted(datos)
    return ordenados[-1] - ordenados[0]

def rango_intercuartilico(datos):
    q = tendencias.cuartiles(datos)
    return q["Q3"] - q["Q1"]

def rango_semi_intercuartilico(datos):
    return rango_intercuartilico(datos) / 2.0

def desviacion_media(datos):
    if not datos:
        return 0.0
    media = tendencias.media_aritmetica(datos)
    suma = sum(abs(x - media) for x in datos)
    return suma / len(datos)

def varianza(datos):
    if not datos:
        return 0.0
    media = tendencias.media_aritmetica(datos)
    suma = sum((x - media) ** 2 for x in datos)
    return suma / len(datos) # Poblacional 

def desviacion_estandar(datos):
    return math.sqrt(varianza(datos))

def coeficiente_variacion(datos):
    media = tendencias.media_aritmetica(datos)
    if media == 0:
        return 0.0
    return (desviacion_estandar(datos) / media) * 100.0

def puntaje_z(datos, x):
    media = tendencias.media_aritmetica(datos)
    sigma = desviacion_estandar(datos)
    if sigma == 0:
        return 0.0
    return (x - media) / sigma

def resumen(datos):
    return {
        "Rango": rango(datos),
        "Rango intercuartilico (IQR)": rango_intercuartilico(datos),
        "Rango semi-intercuartilico": rango_semi_intercuartilico(datos),
        "Desviacion media": desviacion_media(datos),
        "Varianza": varianza(datos),
        "Desviacion estandar": desviacion_estandar(datos),
        "Coeficiente de variacion (%)": coeficiente_variacion(datos)
    }