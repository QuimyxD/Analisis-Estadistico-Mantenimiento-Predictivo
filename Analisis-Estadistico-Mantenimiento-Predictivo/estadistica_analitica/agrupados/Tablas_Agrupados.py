# Tablas

def _linea(anchos):
    partes = []
    for a in anchos:
        partes.append("-" * (a + 2))
    return "+" + "+".join(partes) + "+"


def _fila(valores, anchos, alineacion="izq"):
    celdas = []
    for i in range(len(valores)):
        texto = str(valores[i])
        if alineacion == "der":
            celdas.append(f" {texto:>{anchos[i]}} ")
        elif alineacion == "cen":
            celdas.append(f" {texto:^{anchos[i]}} ")
        else:
            celdas.append(f" {texto:<{anchos[i]}} ")
    return "|" + "|".join(celdas) + "|"


def _titulo(texto, ancho_total):
    print("+" + "-" * (ancho_total - 2) + "+")
    print("|" + f"{texto:^{ancho_total - 2}}" + "|")


def _ajustar_al_titulo(titulo, anchos):
    ancho_total = sum(anchos) + 3 * len(anchos) + 1
    faltante = (len(titulo) + 2) - ancho_total
    if faltante > 0:
        anchos[-1] = anchos[-1] + faltante
        ancho_total = sum(anchos) + 3 * len(anchos) + 1
    return ancho_total


def imprimir_tabla(titulo, encabezados, filas):
    anchos = []
    for i in range(len(encabezados)):
        mayor = len(str(encabezados[i]))
        for f in filas:
            if len(str(f[i])) > mayor:
                mayor = len(str(f[i]))
        anchos.append(mayor)

    ancho_total = _ajustar_al_titulo(titulo, anchos)

    if titulo != "":
        _titulo(titulo, ancho_total)
    print(_linea(anchos))
    print(_fila(encabezados, anchos, "cen"))
    print(_linea(anchos))
    for f in filas:
        print(_fila(f, anchos, "der"))
    print(_linea(anchos))


def imprimir_resumen(titulo, resultados, decimales=4):
    filas = []
    for clave in resultados:
        valor = resultados[clave]
        if isinstance(valor, float):
            valor = f"{valor:.{decimales}f}"
        elif isinstance(valor, (list, tuple)):
            partes = []
            for v in valor:
                if isinstance(v, float):
                    partes.append(f"{v:.{decimales}f}")
                else:
                    partes.append(str(v))
            valor = ", ".join(partes)
        filas.append([clave, valor])

    anchos = [len("Concepto"), len("Valor")]
    for f in filas:
        if len(str(f[0])) > anchos[0]:
            anchos[0] = len(str(f[0]))
        if len(str(f[1])) > anchos[1]:
            anchos[1] = len(str(f[1]))

    ancho_total = _ajustar_al_titulo(titulo, anchos)
    if titulo != "":
        _titulo(titulo, ancho_total)
    print(_linea(anchos))
    print(_fila(["Concepto", "Valor"], anchos, "cen"))
    print(_linea(anchos))
    for f in filas:
        print("|" + f" {str(f[0]):<{anchos[0]}} " + "|" + f" {str(f[1]):>{anchos[1]}} " + "|")
    print(_linea(anchos))


if __name__ == "__main__":
    imprimir_tabla("PRUEBA DE TABLA", ["i", "Clase", "fi"],
                   [[1, "10 - 20", 5], [2, "20 - 30", 12]])
    print()
    imprimir_resumen("PRUEBA DE RESUMEN", {"Media": 25.5, "Moda": 23.125})
