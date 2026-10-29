import math

def media_aritmetica(datos):
    if not datos:
        return 0.0
    return sum(datos) / len(datos)

def media_geometrica(datos):
    if not datos:
        return 0.0
    suma = 0.0
    n = len(datos)
    for x in datos:
        if x > 0:
            suma += math.log10(x)
        else:
            return 0.0 # No soporta ceros ni negativos
    return 10 ** (suma / n)

def media_armonica(datos):
    if not datos:
        return 0.0
    suma = 0.0
    n = len(datos)
    for x in datos:
        if x == 0:
            return 0.0
        suma += 1.0 / x
    return n / suma

def raiz_cuadratica_media(datos):
    if not datos:
        return 0.0
    suma = sum(x ** 2 for x in datos)
    return math.sqrt(suma / len(datos))

def mediana(datos):
    if not datos:
        return 0.0
    ordenados = sorted(datos)
    n = len(ordenados)
    mitad = n // 2
    if n % 2 == 0:
        return (ordenados[mitad - 1] + ordenados[mitad]) / 2.0
    else:
        return ordenados[mitad]

def moda(datos):
    if not datos:
        return None
    frecuencias = {}
    for x in datos:
        frecuencias[x] = frecuencias.get(x, 0) + 1
    max_freq = max(frecuencias.values())
    modas = [k for k, v in frecuencias.items() if v == max_freq]
    return modas[0] if len(modas) == 1 else modas

def cuantil(datos, k, q):
    if not datos:
        return 0.0
    ordenados = sorted(datos)
    n = len(ordenados)
    posicion = (k * (n - 1)) / q
    indice_inferior = int(math.floor(posicion))
    indice_superior = int(math.ceil(posicion))
    
    if indice_inferior == indice_superior:
        return ordenados[indice_inferior]
    
    fraccion = posicion - indice_inferior
    return ordenados[indice_inferior] + fraccion * (ordenados[indice_superior] - ordenados[indice_inferior])

def cuartiles(datos):
    return {
        "Q1": cuantil(datos, 1, 4),
        "Q2": cuantil(datos, 2, 4),
        "Q3": cuantil(datos, 3, 4)
    }

def deciles(datos):
    return {f"D{i}": cuantil(datos, i, 10) for i in range(1, 10)}

def percentiles(datos, lista=None):
    if lista is None:
        lista = [10, 25, 50, 75, 90]
    return {f"P{p}": cuantil(datos, p, 100) for p in lista}

def resumen(datos):
    return {
        "Media aritmetica": media_aritmetica(datos),
        "Media geometrica": media_geometrica(datos),
        "Media armonica": media_armonica(datos),
        "Raiz cuadratica media (RCM)": raiz_cuadratica_media(datos),
        "Mediana": mediana(datos),
        "Moda": str(moda(datos))
    }