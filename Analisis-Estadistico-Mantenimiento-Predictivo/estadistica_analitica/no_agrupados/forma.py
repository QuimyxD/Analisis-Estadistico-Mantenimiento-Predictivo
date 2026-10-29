import math
from . import tendencias
from . import dispersion

def momento_central(datos, r):
    if not datos:
        return 0.0
    media = tendencias.media_aritmetica(datos)
    suma = sum((x - media) ** r for x in datos)
    return suma / len(datos)

def momento_adimensional(datos, r):
    m2 = momento_central(datos, 2)
    if m2 <= 0:
        return 0.0
    sigma = math.sqrt(m2)
    return momento_central(datos, r) / (sigma ** r)

def sesgo_fisher_pearson(datos):
    return momento_adimensional(datos, 3)

def sesgo_pearson_1(datos):
    sigma = dispersion.desviacion_estandar(datos)
    if sigma == 0:
        return 0.0
    m_arit = tendencias.media_aritmetica(datos)
    m_moda = tendencias.moda(datos)
    if isinstance(m_moda, list): # Si hay múltiples modas se toma la primera
        m_moda = m_moda[0]
    return (m_arit - m_moda) / sigma

def sesgo_pearson_2(datos):
    sigma = dispersion.desviacion_estandar(datos)
    if sigma == 0:
        return 0.0
    return 3 * (tendencias.media_aritmetica(datos) - tendencias.mediana(datos)) / sigma

def clasificar_sesgo(g1):
    if abs(g1) < 0.5:
        magnitud = "asimetria leve (casi simetrica)"
    elif abs(g1) < 1.0:
        magnitud = "asimetria moderada"
    else:
        magnitud = "asimetria severa"

    if g1 > 0:
        direccion = "positiva (cola a la derecha)"
    elif g1 < 0:
        direccion = "negativa (cola a la izquierda)"
    else:
        direccion = "simetrica"
    return magnitud + " / " + direccion

def curtosis_momentos(datos):
    return momento_adimensional(datos, 4) - 3.0

def clasificar_curtosis(k):
    if abs(k) < 0.1:
        return "mesocurtica"
    elif k > 0:
        return "leptocurtica"
    else:
        return "platicurtica"

def resumen(datos):
    g1 = sesgo_fisher_pearson(datos)
    k = curtosis_momentos(datos)
    return {
        "Momento central m2 (varianza)": momento_central(datos, 2),
        "Momento central m3": momento_central(datos, 3),
        "Momento central m4": momento_central(datos, 4),
        "Sesgo de Fisher-Pearson (g1)": g1,
        "Primer coef. de Pearson": sesgo_pearson_1(datos),
        "Segundo coef. de Pearson": sesgo_pearson_2(datos),
        "Interpretacion del sesgo": clasificar_sesgo(g1),
        "Exceso de curtosis (k)": k,
        "Interpretacion de la curtosis": clasificar_curtosis(k)
    }