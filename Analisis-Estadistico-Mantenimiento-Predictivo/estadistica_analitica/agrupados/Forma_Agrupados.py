# Momentos, sesgo y curtosis para los datos agrupados

import math

try:
    from . import Frecuencias_Agrupados as frecuencias
    from . import Tendencias_Agrupados as tendencias
    from . import Dispersion_Agrupados as dispersion
    from . import Tablas_Agrupados as tablas
except ImportError:
    import Frecuencias_Agrupados as frecuencias
    import Tendencias_Agrupados as tendencias
    import Dispersion_Agrupados as dispersion
    import Tablas_Agrupados as tablas

KQ_NORMAL = 1.90

# Momentos
def momento_crudo(tabla, r):
    suma = 0.0
    for fila in tabla["clases"]:
        suma = suma + fila["fi"] * (fila["xi"] ** r)
    return suma / tabla["n"]


def momento_central(tabla, r):
    media = tendencias.media_aritmetica(tabla)
    suma = 0.0
    for fila in tabla["clases"]:
        suma = suma + fila["fi"] * ((fila["xi"] - media) ** r)
    return suma / tabla["n"]


def momento_origen_arbitrario(tabla, r, A):
    suma = 0.0
    for fila in tabla["clases"]:
        suma = suma + fila["fi"] * ((fila["xi"] - A) ** r)
    return suma / tabla["n"]


def momento_adimensional(tabla, r):
    m2 = momento_central(tabla, 2)
    if m2 <= 0:
        return 0.0
    sigma = math.sqrt(m2)
    return momento_central(tabla, r) / (sigma ** r)


def momentos_desde_origen(tabla, A):
    m1p = momento_origen_arbitrario(tabla, 1, A)
    m2p = momento_origen_arbitrario(tabla, 2, A)
    m3p = momento_origen_arbitrario(tabla, 3, A)
    m4p = momento_origen_arbitrario(tabla, 4, A)

    m2 = m2p - m1p ** 2
    m3 = m3p - 3 * m1p * m2p + 2 * (m1p ** 3)
    m4 = m4p - 4 * m1p * m3p + 6 * (m1p ** 2) * m2p - 3 * (m1p ** 4)

    return {"m'1": m1p, "m'2": m2p, "m'3": m3p, "m'4": m4p,
            "m2 (desde A)": m2, "m3 (desde A)": m3, "m4 (desde A)": m4}


def resumen_origen_arbitrario(tabla, A=None):
    if A is None:
        A = tabla["clases"][tendencias.indice_clase_modal(tabla)]["xi"]
    datos = {"A (origen arbitrario)": float(A)}
    datos.update(momentos_desde_origen(tabla, A))
    return datos


# Sesgo
def sesgo_fisher_pearson(tabla):
    return momento_adimensional(tabla, 3)


def sesgo_pearson_1(tabla):
    sigma = dispersion.desviacion_estandar(tabla)
    if sigma == 0:
        return 0.0
    return (tendencias.media_aritmetica(tabla) - tendencias.moda(tabla)) / sigma


def sesgo_pearson_2(tabla):
    sigma = dispersion.desviacion_estandar(tabla)
    if sigma == 0:
        return 0.0
    return 3 * (tendencias.media_aritmetica(tabla) - tendencias.mediana(tabla)) / sigma


def sesgo_cuantiles(tabla):
    q = tendencias.cuartiles(tabla)
    if (q["Q3"] - q["Q1"]) == 0:
        return 0.0
    return (q["Q3"] + q["Q1"] - 2 * q["Q2"]) / (q["Q3"] - q["Q1"])


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

# Curtosis
def curtosis_momentos(tabla):
    """Exceso de curtosis = a4 - 3"""
    return momento_adimensional(tabla, 4) - 3


def curtosis_percentilica(tabla):
    """KQ = (P90 - P10) / (P75 - P25)"""
    p90 = tendencias.cuantil(tabla, 90, 100)
    p10 = tendencias.cuantil(tabla, 10, 100)
    p75 = tendencias.cuantil(tabla, 75, 100)
    p25 = tendencias.cuantil(tabla, 25, 100)
    if (p75 - p25) == 0:
        return 0.0
    return (p90 - p10) / (p75 - p25)


def clasificar_curtosis(k):
    if abs(k) < 0.1:
        return "mesocurtica"
    elif k > 0:
        return "leptocurtica"
    else:
        return "platicurtica"


def clasificar_curtosis_percentilica(kq):
    """Compara KQ contra el de la normal (KQ_NORMAL = 1.90)."""
    if abs(kq - KQ_NORMAL) < 0.05:
        return "mesocurtica"
    elif kq > KQ_NORMAL:
        return "leptocurtica"
    else:
        return "platicurtica"

def resumen(tabla):
    frecuencias.validar_tabla(tabla)
    g1 = sesgo_fisher_pearson(tabla)
    k = curtosis_momentos(tabla)
    kq = curtosis_percentilica(tabla)
    return {
        "Momento crudo r=1": momento_crudo(tabla, 1),
        "Momento crudo r=2": momento_crudo(tabla, 2),
        "Momento central m1": momento_central(tabla, 1),
        "Momento central m2 (varianza)": momento_central(tabla, 2),
        "Momento central m3": momento_central(tabla, 3),
        "Momento central m4": momento_central(tabla, 4),
        "Momento adimensional a3": momento_adimensional(tabla, 3),
        "Momento adimensional a4": momento_adimensional(tabla, 4),
        "Sesgo de Fisher-Pearson (g1)": g1,
        "Primer coef. de Pearson": sesgo_pearson_1(tabla),
        "Segundo coef. de Pearson": sesgo_pearson_2(tabla),
        "Sesgo por cuantiles (Bowley)": sesgo_cuantiles(tabla),
        "Interpretacion del sesgo": clasificar_sesgo(g1),
        "Exceso de curtosis (k)": k,
        "Curtosis percentilica (KQ)": kq,
        "Interpretacion de la curtosis": clasificar_curtosis(k) + " / " +
                                         clasificar_curtosis_percentilica(kq)
    }


if __name__ == "__main__":
    t = frecuencias.tabla_desde_clases(frecuencias.EJEMPLO_FILAS, "continuo")
    tablas.imprimir_resumen("MOMENTOS, SESGO Y CURTOSIS (AGRUPADOS)", resumen(t))
    print()
    tablas.imprimir_resumen("MOMENTOS DESDE UN ORIGEN ARBITRARIO", resumen_origen_arbitrario(t))
