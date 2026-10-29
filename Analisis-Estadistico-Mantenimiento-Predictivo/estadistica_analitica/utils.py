import csv
from pathlib import Path

def cargar_datos_csv(nombre_archivo="predictive_maintenance_dataset.csv"):

    ruta_actual = Path.cwd()
    ruta_archivo = ruta_actual / 'Datos' / nombre_archivo
    
    if not ruta_archivo.is_file():
        # Si se ejecuta desde la raíz del proyecto
        ruta_archivo = ruta_actual / 'Proyecto_Estadistica_Python' / 'Datos' / nombre_archivo
        if not ruta_archivo.is_file():
            # Buscar un nivel más arriba
            ruta_archivo = Path('Datos') / nombre_archivo

    if not ruta_archivo.is_file():
        raise FileNotFoundError(f"No se pudo localizar el archivo en la ruta: {ruta_archivo}")

    info_metadatos = (
        f"REPORTE DE METADATOS DE ARCHIVO\n"
        f"Directorio de trabajo actual: {Path.cwd()}\n"
        f"Nombre del archivo: {ruta_archivo.name}\n"
        f"Extensión: {ruta_archivo.suffix}\n"
        f"Nombre sin extensión: {ruta_archivo.stem}\n"
        f"Directorio padre: {ruta_archivo.parent}\n"
        f"Ruta construida completa: {ruta_archivo.resolve()}\n"
    )
    print(info_metadatos)

    ruta_txt = Path.cwd() / 'metadatos_ruta.txt'
    with open(ruta_txt, 'w', encoding='utf-8') as f_txt:
        f_txt.write(info_metadatos)

    metricas_continuas = {f'metric_{i}': [] for i in range(1, 10)}
    variables_discretas = {'failure': [], 'device': []}

    with open(ruta_archivo, mode='r', encoding='utf-8') as archivo_csv:
        lector = csv.DictReader(archivo_csv)
        for fila in lector:
            variables_discretas['failure'].append(int(fila.get('failure', 0)))
            variables_discretas['device'].append(fila.get('device', ''))

            for i in range(1, 10):
                col = f'metric{i}'
                valor = fila.get(col, '').strip()
                if valor:
                    metricas_continuas[f'metric_{i}'].append(float(valor))
                else:
                    metricas_continuas[f'metric_{i}'].append(0.0)

    return {
        'continuas': metricas_continuas,
        'discretas': variables_discretas
    }

if __name__ == "__main__":
    datos = cargar_datos_csv()
    print("Datos cargados correctamente")
    print("Muestra Métrica 1:", datos['continuas']['metric_1'][:5])