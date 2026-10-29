from pathlib import Path

from estadistica_analitica.utils import cargar_datos_csv
from estadistica_analitica.no_agrupados import tendencias as nt
from estadistica_analitica.no_agrupados import dispersion as nd
from estadistica_analitica.no_agrupados import forma as nf
from estadistica_analitica.agrupados import Frecuencias_Agrupados as ag_frec
from estadistica_analitica.agrupados import Tendencias_Agrupados as ag_tend
from estadistica_analitica.agrupados import Dispersion_Agrupados as ag_disp
from estadistica_analitica.agrupados import Forma_Agrupados as ag_forma

NOMBRE_CSV = "predictive_maintenance_dataset.csv"

METRICAS = ["metric_5", "metric_6", "metric_9"]

CARPETA_NO_AGRUPADOS = "Resultados_No_Agrupados"
CARPETA_AGRUPADOS = "Resultados_Agrupados"
CARPETA_AUDITORIA = "Resultados_Auditoria"


def crear_carpeta(nombre):
    carpeta = Path.cwd() / nombre
    carpeta.mkdir(parents=True, exist_ok=True)
    return carpeta


def validar_archivos():
    carpeta_datos = Path.cwd() / "Datos"
    if not carpeta_datos.is_dir():
        print("No se encontro la carpeta Datos en:", Path.cwd())
        print("Ejecuta main.py desde la carpeta raiz del proyecto.")
        return False
    if not (carpeta_datos / NOMBRE_CSV).is_file():
        print("No se encontro el archivo", NOMBRE_CSV, "dentro de Datos")
        return False
    return True


def es_numero(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def es_nan(x):
    return x != x


def moda_numerica(datos):
    m = nt.moda(datos)
    if isinstance(m, list):
        m = m[0]
    return m


def juntar(*diccionarios):
    todo = {}
    for d in diccionarios:
        todo.update(d)
    return todo


def calcular_no_agrupado(datos):
    tendencia = nt.resumen(datos)
    tendencia["Moda"] = moda_numerica(datos) 

    cuantiles = juntar(nt.cuartiles(datos), nt.deciles(datos), nt.percentiles(datos))

    return {
        "Tendencia central": tendencia,
        "Cuantiles": cuantiles,
        "Dispersion": nd.resumen(datos),
        "Forma": nf.resumen(datos)
    }


def calcular_agrupado(tabla):
    return {
        "Tendencia central": ag_tend.resumen(tabla),
        "Cuantiles": ag_tend.resumen_cuantiles(tabla),
        "Dispersion": ag_disp.resumen(tabla),
        "Forma": ag_forma.resumen(tabla)
    }


def aplanar(resultado):
    plano = {}
    for seccion in resultado:
        for nombre in resultado[seccion]:
            plano[nombre] = resultado[seccion][nombre]
    if "Rango (limites reales)" in plano:
        plano["Rango"] = plano["Rango (limites reales)"]
    return plano

# Auditoria de error
def error_relativo(exacto, aprox):
    if not (es_numero(exacto) and es_numero(aprox)):
        return None
    if es_nan(exacto) or es_nan(aprox):
        return None
    if exacto == 0:
        return None
    return abs(aprox - exacto) / abs(exacto) * 100


def auditar(res_no_agr, res_agr):
    plano_no = aplanar(res_no_agr)
    plano_ag = aplanar(res_agr)
    errores = {}
    for nombre in plano_no:
        if nombre in plano_ag:
            exacto = plano_no[nombre]
            aprox = plano_ag[nombre]
            if es_numero(exacto) and es_numero(aprox):
                errores[nombre] = {
                    "exacto": exacto,
                    "agrupado": aprox,
                    "error": error_relativo(exacto, aprox)
                }
    return errores


def resumen_errores(errores):
    lista = []
    maximo = 0.0
    nombre_max = ""
    for nombre in errores:
        e = errores[nombre]["error"]
        if e is not None:
            lista.append(e)
            if e > maximo:
                maximo = e
                nombre_max = nombre
    if len(lista) == 0:
        return {"promedio": None, "mediana": None, "maximo": None,
                "nombre_max": "", "validos": 0}

    lista.sort()
    mitad = len(lista) // 2
    if len(lista) % 2 == 0:
        mediana = (lista[mitad - 1] + lista[mitad]) / 2
    else:
        mediana = lista[mitad]

    return {"promedio": sum(lista) / len(lista), "mediana": mediana,
            "maximo": maximo, "nombre_max": nombre_max, "validos": len(lista)}

# Texto para los archivos .txt
def formato(valor):
    if es_numero(valor) and not isinstance(valor, int):
        if es_nan(valor):
            return "N/A"
        return f"{valor:.4f}"
    return str(valor)


def texto_estadisticas(titulo, resultado):
    lineas = [titulo, "=" * len(titulo), ""]
    for seccion in resultado:
        lineas.append(seccion.upper())
        lineas.append("-" * len(seccion))
        for nombre in resultado[seccion]:
            lineas.append(f"{nombre}: {formato(resultado[seccion][nombre])}")
        lineas.append("")
    return "\n".join(lineas)


def texto_tabla_frecuencias(metrica, tabla):
    lineas = [f"TABLA DE DISTRIBUCION DE FRECUENCIAS - {metrica}", ""]
    lineas.append(f"N = {tabla['n']}   K = {tabla['total_clases']}   "
                  f"Amplitud c = {tabla['amplitud']:.4f}")
    lineas.append(f"Minimo = {tabla['minimo']}   Maximo = {tabla['maximo']}")
    lineas.append("")
    encabezado = (f"{'No.':>4} {'Li':>16} {'Ls':>16} {'xi':>16} "
                  f"{'fi':>8} {'Fi':>8} {'hi':>8} {'Hi':>8}")
    lineas.append(encabezado)
    lineas.append("-" * len(encabezado))
    for fila in tabla["clases"]:
        lineas.append(f"{fila['clase']:>4} {fila['li']:>16.2f} {fila['ls']:>16.2f} "
                      f"{fila['xi']:>16.2f} {fila['fi']:>8} {fila['Fi']:>8} "
                      f"{fila['hi']:>8.4f} {fila['Hi']:>8.4f}")
    return "\n".join(lineas)


def texto_auditoria(metrica, errores):
    lineas = [f"AUDITORIA DE ERROR (AGRUPADO vs NO AGRUPADO) - {metrica}", ""]
    encabezado = f"{'Estadistico':<34} {'No agrupado':>18} {'Agrupado':>18} {'Error %':>12}"
    lineas.append(encabezado)
    lineas.append("-" * len(encabezado))
    for nombre in errores:
        e = errores[nombre]
        if e["error"] is None:
            texto_error = "N/A"
        else:
            texto_error = f"{e['error']:.4f}"
        lineas.append(f"{nombre:<34} {formato(e['exacto']):>18} "
                      f"{formato(e['agrupado']):>18} {texto_error:>12}")
    r = resumen_errores(errores)
    lineas.append("")
    if r["validos"] > 0:
        lineas.append(f"Error promedio: {r['promedio']:.4f} %")
        lineas.append(f"Error mediano: {r['mediana']:.4f} %")
        lineas.append(f"Error maximo: {r['maximo']:.4f} % ({r['nombre_max']})")
    lineas.append("N/A = no se pudo calcular (valor exacto en cero o dato no numerico)")
    return "\n".join(lineas)


def guardar(carpeta, nombre_archivo, texto):
    ruta = carpeta / nombre_archivo
    with open(ruta, "w", encoding="utf-8") as f:
        f.write(texto + "\n")
    return ruta

# Programa principal
def analizar_metrica(nombre, datos):
    # no agrupado
    res_no = calcular_no_agrupado(datos)

    # agrupado
    tabla = ag_frec.construir_tabla(datos, "continuo")
    res_ag = calcular_agrupado(tabla)

    errores = auditar(res_no, res_ag)

    return {
        "n": len(datos),
        "no_agrupado": res_no,
        "agrupado": res_ag,
        "tabla": tabla,
        "errores": errores,
        "resumen_error": resumen_errores(errores)
    }


def exportar(resultados):
    carpeta_no = crear_carpeta(CARPETA_NO_AGRUPADOS)
    carpeta_ag = crear_carpeta(CARPETA_AGRUPADOS)
    carpeta_aud = crear_carpeta(CARPETA_AUDITORIA)

    for metrica in resultados:
        r = resultados[metrica]
        guardar(carpeta_no, f"estadisticas_{metrica}.txt",
                texto_estadisticas(f"ESTADISTICOS NO AGRUPADOS - {metrica}", r["no_agrupado"]))
        guardar(carpeta_ag, f"estadisticas_{metrica}.txt",
                texto_estadisticas(f"ESTADISTICOS AGRUPADOS - {metrica}", r["agrupado"]))
        guardar(carpeta_ag, f"tabla_frecuencias_{metrica}.txt",
                texto_tabla_frecuencias(metrica, r["tabla"]))
        guardar(carpeta_aud, f"auditoria_{metrica}.txt",
                texto_auditoria(metrica, r["errores"]))

    # archivo con el resumen de todas las metricas
    lineas = ["RESUMEN DE LA AUDITORIA POR METRICA", ""]
    encabezado = f"{'Metrica':<10} {'N':>8} {'K':>4} {'Error prom %':>14} {'Error med %':>14} {'Error max %':>14}  Estadistico con mas error"
    lineas.append(encabezado)
    lineas.append("-" * len(encabezado))
    for metrica in resultados:
        r = resultados[metrica]
        re = r["resumen_error"]
        if re["validos"] > 0:
            lineas.append(f"{metrica:<10} {r['n']:>8} {r['tabla']['total_clases']:>4} "
                          f"{re['promedio']:>14.4f} {re['mediana']:>14.4f} {re['maximo']:>14.4f}  {re['nombre_max']}")
    guardar(carpeta_aud, "resumen_auditoria.txt", "\n".join(lineas))


def mostrar_en_consola(resultados):
    print()
    print("RESUMEN DE LA AUDITORIA")
    for metrica in resultados:
        r = resultados[metrica]
        re = r["resumen_error"]
        print(f"\n{metrica}: N = {r['n']}, K = {r['tabla']['total_clases']} clases, "
              f"c = {r['tabla']['amplitud']:.2f}")
        for nombre in ["Media aritmetica", "Mediana", "Moda", "Desviacion estandar",
                       "Sesgo de Fisher-Pearson (g1)", "Exceso de curtosis (k)"]:
            if nombre in r["errores"]:
                e = r["errores"][nombre]
                if e["error"] is None:
                    texto = "N/A"
                else:
                    texto = f"{e['error']:.4f} %"
                print(f"  {nombre:<32} exacto = {formato(e['exacto']):>16}  "
                      f"agrupado = {formato(e['agrupado']):>16}  error = {texto}")
        if re["validos"] > 0:
            print(f"  Error mediano: {re['mediana']:.4f} %   Error promedio: {re['promedio']:.4f} %   "
                  f"Error maximo: {re['maximo']:.4f} % ({re['nombre_max']})")


def main():
    print("PRACTICA 1 - ANALISIS ESTADISTICO AGRUPADO vs NO AGRUPADO\n")

    if not validar_archivos():
        return

    datos = cargar_datos_csv(NOMBRE_CSV)
    continuas = datos["continuas"]

    resultados = {}
    for metrica in METRICAS:
        resultados[metrica] = analizar_metrica(metrica, continuas[metrica])

    exportar(resultados)
    mostrar_en_consola(resultados)

    print("\nArchivos .txt guardados en:")
    print(" ", CARPETA_NO_AGRUPADOS)
    print(" ", CARPETA_AGRUPADOS)
    print(" ", CARPETA_AUDITORIA)

    # graficos del EDA
    try:
        from estadistica_analitica.graficos import graficos
        graficos.generar_graficos_eda(datos, resultados)
    except Exception as error:
        print("\nNo se pudieron generar los graficos:", error)


if __name__ == "__main__":
    main()