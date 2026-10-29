# Medidas de tendencia central y de posicion (cuantiles) para DATOS AGRUPADOS.

import math

try:
    from . import Frecuencias_Agrupados as frecuencias
    from . import Tablas_Agrupados as tablas
except ImportError:
    import Frecuencias_Agrupados as frecuencias
    import Tablas_Agrupados as tablas


# Medias
def media_aritmetica(tabla):
    suma = 0.0
    for fila in tabla["clases"]:
        suma = suma + fila["fi"] * fila["xi"]
    return suma / tabla["n"]


def media_geometrica(tabla):
    suma = 0.0
    for fila in tabla["clases"]:
        if fila["fi"] > 0:
            if fila["xi"] <= 0:
                return float("nan")
            suma = suma + fila["fi"] * math.log10(fila["xi"])
    return 10 ** (suma / tabla["n"])


def media_armonica(tabla):
    suma = 0.0
    for fila in tabla["clases"]:
        if fila["fi"] > 0:
            if fila["xi"] == 0:
                return float("nan")
            suma = suma + fila["fi"] / fila["xi"]
    if suma == 0:
        return float("nan")
    return tabla["n"] / suma


def raiz_cuadratica_media(tabla):
    suma = 0.0
    for fila in tabla["clases"]:
        suma = suma + fila["fi"] * (fila["xi"] ** 2)
    return math.sqrt(suma / tabla["n"])


# ---------------------------------------------------------------------------
# Cuantiles, mediana y moda
# ---------------------------------------------------------------------------
def cuantil(tabla, k, q):
    if q <= 0 or k < 0 or k > q:
        raise ValueError("Se requiere q > 0 y 0 <= k <= q")

    n = tabla["n"]
    clases = tabla["clases"]
    c = tabla["amplitud"]

    posicion = (k * n) / q
    i = frecuencias.clase_del_acumulado(tabla, posicion)

    if i == 0:
        f_anterior = 0
    else:
        f_anterior = clases[i - 1]["Fi"]

    li = clases[i]["li"]
    f = clases[i]["fi"]
    if f == 0:
        return li
    return li + ((posicion - f_anterior) / f) * c


def mediana(tabla):
    return cuantil(tabla, 1, 2)


def indice_clase_modal(tabla):
    clases = tabla["clases"]
    i = 0
    for j in range(len(clases)):
        if clases[j]["fi"] > clases[i]["fi"]:
            i = j
    return i


def moda(tabla):
    clases = tabla["clases"]
    c = tabla["amplitud"]

    i = indice_clase_modal(tabla)
    f_modal = clases[i]["fi"]
    if i == 0:
        f_anterior = 0
    else:
        f_anterior = clases[i - 1]["fi"]
    if i == len(clases) - 1:
        f_posterior = 0
    else:
        f_posterior = clases[i + 1]["fi"]

    d1 = f_modal - f_anterior
    d2 = f_modal - f_posterior

    if (d1 + d2) == 0:
        return clases[i]["xi"]
    return clases[i]["li"] + (d1 / (d1 + d2)) * c


def cuartiles(tabla):
    return {"Q1": cuantil(tabla, 1, 4),
            "Q2": cuantil(tabla, 2, 4),
            "Q3": cuantil(tabla, 3, 4)}


def deciles(tabla):
    resultado = {}
    for k in range(1, 10):
        resultado["D" + str(k)] = cuantil(tabla, k, 10)
    return resultado


def percentiles(tabla, lista=None):
    if lista is None:
        lista = [10, 25, 50, 75, 90]
    resultado = {}
    for k in lista:
        resultado["P" + str(k)] = cuantil(tabla, k, 100)
    return resultado


# Resumenes
def resumen(tabla):
    frecuencias.validar_tabla(tabla)
    return {
        "Media aritmetica": media_aritmetica(tabla),
        "Media geometrica": media_geometrica(tabla),
        "Media armonica": media_armonica(tabla),
        "Raiz cuadratica media (RCM)": raiz_cuadratica_media(tabla),
        "Mediana": mediana(tabla),
        "Moda": moda(tabla)
    }


def resumen_cuantiles(tabla):
    frecuencias.validar_tabla(tabla)
    datos = {}
    datos.update(cuartiles(tabla))
    datos.update(deciles(tabla))
    datos.update(percentiles(tabla))
    return datos


if __name__ == "__main__":
    t = frecuencias.tabla_desde_clases(frecuencias.EJEMPLO_FILAS, "continuo")
    frecuencias.imprimir_distribucion(t)
    print()
    tablas.imprimir_resumen("MEDIDAS DE TENDENCIA CENTRAL (AGRUPADOS)", resumen(t))
    print()
    tablas.imprimir_resumen("CUANTILES (AGRUPADOS)", resumen_cuantiles(t))
