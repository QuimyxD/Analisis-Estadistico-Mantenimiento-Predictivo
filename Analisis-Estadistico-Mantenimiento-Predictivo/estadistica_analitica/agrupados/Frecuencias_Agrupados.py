# Tabla de distribucion de frecuencias para datos agrupados

import math

try:
    from . import Tablas_Agrupados as tablas
except ImportError:
    import Tablas_Agrupados as tablas


TOLERANCIA = 1e-9

EJEMPLO_FILAS = [(60, 65, 5), (65, 70, 18), (70, 75, 42), (75, 80, 27), (80, 85, 8)]


# Utilidades internas
def _cerca(a, b):
    return math.isclose(a, b, rel_tol=TOLERANCIA, abs_tol=TOLERANCIA)


def _es_numero(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x)


def _validar_tipo(tipo):
    if tipo not in ("continuo", "discreto"):
        raise ValueError("tipo debe ser 'continuo' o 'discreto'")


def _redondear_arriba(valor, decimales):
    factor = 10 ** decimales
    return math.ceil(round(valor * factor, 9)) / factor


def _fila_clase(numero, li_ap, ls_ap, li, ls, fi):
    return {
        "clase": numero,
        "li_ap": li_ap, "ls_ap": ls_ap,
        "li": li, "ls": ls,
        "xi": (li + ls) / 2, "fi": fi
    }


def _armar_tabla(tipo, clases, minimo, maximo, amplitud):
    n = 0
    for fila in clases:
        n = n + fila["fi"]
    if n <= 0:
        raise ValueError("La suma de las frecuencias debe ser mayor que 0")
    acumulada = 0
    for fila in clases:
        acumulada = acumulada + fila["fi"]
        fila["Fi"] = acumulada
        fila["hi"] = fila["fi"] / n
        fila["Hi"] = acumulada / n
    return {
        "tipo": tipo,
        "n": n,
        "minimo": minimo,
        "maximo": maximo,
        "rango": maximo - minimo,
        "total_clases": len(clases),
        "amplitud": amplitud,
        "clases": clases
    }


# Construccion de la tabla
def regla_sturges(n):
    if n < 1:
        raise ValueError("N debe ser al menos 1")
    k = 1 + 3.322 * math.log10(n)
    return max(1, int(round(k)))


def construir_tabla(datos, tipo="continuo", num_clases=None, decimales=2):
    _validar_tipo(tipo)
    datos = list(datos)
    n = len(datos)
    if n == 0:
        raise ValueError("La lista de datos esta vacia")

    minimo = maximo = datos[0]
    for x in datos:
        if not _es_numero(x):
            raise ValueError("Dato no valido (se esperan numeros finitos): " + repr(x))
        if x < minimo:
            minimo = x
        if x > maximo:
            maximo = x

    if num_clases is None:
        k = regla_sturges(n)
    else:
        k = int(num_clases)
        if k < 1:
            raise ValueError("num_clases debe ser al menos 1")

    clases = []

    if tipo == "discreto":
        for x in datos:
            if x != int(x):
                raise ValueError("Una variable discreta solo admite enteros: " + repr(x))
        minimo = int(minimo)
        maximo = int(maximo)
        rango = maximo - minimo
        c = math.ceil((rango + 1) / k)
        k = math.ceil((rango + 1) / c)
        for j in range(k):
            li_ap = minimo + j * c
            ls_ap = li_ap + c - 1
            clases.append(_fila_clase(j + 1, li_ap, ls_ap,
                                      li_ap - 0.5, ls_ap + 0.5, 0))
        for x in datos:
            clases[(int(x) - minimo) // c]["fi"] += 1
    else:
        rango = maximo - minimo
        if rango == 0:
            raise ValueError("Todos los datos son iguales (rango = 0): "
                             "no hay nada que agrupar")
        c = _redondear_arriba(rango / k, decimales)
        for j in range(k):
            li = float(round(minimo + j * c, 10))
            ls = float(round(minimo + (j + 1) * c, 10))
            if j == k - 1 and ls < maximo:
                ls = maximo
            clases.append(_fila_clase(j + 1, li, ls, li, ls, 0))

        for x in datos:
            j = int((x - minimo) / c)
            if j > k - 1:
                j = k - 1
            while j > 0 and x < clases[j]["li"]:
                j -= 1
            while j < k - 1 and x >= clases[j]["ls"]:
                j += 1
            clases[j]["fi"] += 1

    return _armar_tabla(tipo, clases, minimo, maximo, c)


def tabla_desde_clases(filas, tipo="continuo"):
    _validar_tipo(tipo)
    filas = list(filas)
    if len(filas) == 0:
        raise ValueError("La tabla no tiene clases")

    clases = []
    for j in range(len(filas)):
        numero = j + 1
        try:
            li, ls, fi = filas[j]
        except (TypeError, ValueError):
            raise ValueError("La clase " + str(numero) + " debe ser una tupla (li, ls, fi)")
        if not (_es_numero(li) and _es_numero(ls) and _es_numero(fi)):
            raise ValueError("La clase " + str(numero) + " tiene valores no numericos")
        if fi < 0 or fi != int(fi):
            raise ValueError("La frecuencia de la clase " + str(numero) +
                             " debe ser un entero >= 0")
        fi = int(fi)
        if tipo == "discreto":
            if li != int(li) or ls != int(ls):
                raise ValueError("Los limites de la clase " + str(numero) +
                                 " deben ser enteros (variable discreta)")
            if ls < li:
                raise ValueError("En la clase " + str(numero) + " el limite superior "
                                 "es menor que el inferior")
            clases.append(_fila_clase(numero, li, ls, li - 0.5, ls + 0.5, fi))
        else:
            if ls <= li:
                raise ValueError("En la clase " + str(numero) + " el limite superior "
                                 "debe ser mayor que el inferior")
            li = float(li)
            ls = float(ls)
            clases.append(_fila_clase(numero, li, ls, li, ls, fi))

    amplitud = clases[0]["ls"] - clases[0]["li"]
    tabla = _armar_tabla(tipo, clases, clases[0]["li_ap"], clases[-1]["ls_ap"], amplitud)
    validar_tabla(tabla)
    return tabla


def validar_tabla(tabla):
    for clave in ("n", "amplitud", "clases"):
        if clave not in tabla:
            raise ValueError("A la tabla le falta la clave '" + clave + "'")
    clases = tabla["clases"]
    if len(clases) == 0:
        raise ValueError("La tabla no tiene clases")
    if not tabla["amplitud"] > 0:
        raise ValueError("La amplitud de clase debe ser positiva")

    acumulada = 0
    for j in range(len(clases)):
        fila = clases[j]
        numero = j + 1
        for clave in ("li", "ls", "xi", "fi", "Fi"):
            if clave not in fila:
                raise ValueError("La clase " + str(numero) + " no tiene '" + clave + "'")
        if fila["fi"] < 0:
            raise ValueError("La clase " + str(numero) + " tiene frecuencia negativa")
        acumulada = acumulada + fila["fi"]
        if not _cerca(fila["Fi"], acumulada):
            raise ValueError("Fi de la clase " + str(numero) + " no coincide con la "
                             "suma de las frecuencias")
        if not _cerca(fila["ls"] - fila["li"], tabla["amplitud"]):
            raise ValueError("La clase " + str(numero) + " no tiene la amplitud c "
                             "(todas las clases deben medir lo mismo)")
        if not _cerca(fila["xi"], (fila["li"] + fila["ls"]) / 2):
            raise ValueError("La marca de la clase " + str(numero) + " no es el "
                             "punto medio de sus limites")
        if j > 0 and not _cerca(fila["li"], clases[j - 1]["ls"]):
            raise ValueError("Las clases " + str(j) + " y " + str(numero) +
                             " no son contiguas")

    if tabla["n"] <= 0 or not _cerca(tabla["n"], acumulada):
        raise ValueError("N no coincide con la suma de las frecuencias")
    return True

# Consultas sobre la tabla
def marcas_clase(tabla):
    return [fila["xi"] for fila in tabla["clases"]]


def frecuencias_absolutas(tabla):
    return [fila["fi"] for fila in tabla["clases"]]


def frecuencias_relativas(tabla):
    return [fila["hi"] for fila in tabla["clases"]]


def frecuencias_acumuladas(tabla):
    return [fila["Fi"] for fila in tabla["clases"]]


def frecuencias_relativas_acumuladas(tabla):
    return [fila["Hi"] for fila in tabla["clases"]]


def clase_del_acumulado(tabla, posicion):
    clases = tabla["clases"]
    for i in range(len(clases)):
        if clases[i]["Fi"] >= posicion:
            return i
    return len(clases) - 1


def resumen(tabla):
    validar_tabla(tabla)
    return {
        "Tipo de variable": tabla["tipo"],
        "Total de datos (N)": tabla["n"],
        "Valor minimo": float(tabla["minimo"]),
        "Valor maximo": float(tabla["maximo"]),
        "Rango de datos": float(tabla["rango"]),
        "Total de clases (K)": tabla["total_clases"],
        "Amplitud de clase (c)": float(tabla["amplitud"])
    }


def _decimales_para(valor):
    texto = f"{valor:.10f}".rstrip("0")
    decimales = len(texto.split(".")[1]) if "." in texto else 0
    return min(max(decimales, 2), 6)


def imprimir_distribucion(tabla):
    d = _decimales_para(tabla["amplitud"])
    filas = []
    total_hi = 0.0
    for fila in tabla["clases"]:
        if tabla["tipo"] == "discreto":
            intervalo = f"{fila['li_ap']} - {fila['ls_ap']}"
            reales = f"{fila['li']:.1f} - {fila['ls']:.1f}"
        else:
            intervalo = f"{fila['li_ap']:.{d}f} - {fila['ls_ap']:.{d}f}"
            reales = intervalo
        total_hi = total_hi + fila["hi"]
        filas.append([
            fila["clase"], intervalo, reales,
            f"{fila['xi']:.{max(3, d + 1)}f}", fila["fi"], fila["Fi"],
            f"{fila['hi']:.4f}", f"{fila['Hi']:.4f}"
        ])
    filas.append(["", "Total", "", "", tabla["n"], "", f"{total_hi:.4f}", ""])

    tablas.imprimir_tabla(
        "TABLA DE DISTRIBUCION DE FRECUENCIAS (DATOS AGRUPADOS)",
        ["No.", "Intervalo", "Limites reales", "xi", "fi", "Fi", "hi", "Hi"],
        filas
    )


if __name__ == "__main__":
    t = tabla_desde_clases(EJEMPLO_FILAS, "continuo")
    imprimir_distribucion(t)
    print()
    tablas.imprimir_resumen("DATOS GENERALES", resumen(t))

    print()
    prueba = [12.4, 15.1, 18.9, 11.0, 14.2, 19.5, 13.3, 16.8, 17.2, 12.9,
              15.5, 18.1, 11.7, 14.9, 16.2]
    imprimir_distribucion(construir_tabla(prueba, "continuo"))
