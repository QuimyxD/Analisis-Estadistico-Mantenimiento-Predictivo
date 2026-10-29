# Analisis Estadistico y Mantenimiento Predictivo


# Práctica 01 - Análisis Estadístico y Mantenimiento Predictivo

Este repositorio contiene la implementación y desarrollo de la **Práctica 01** del curso de **Fundamentos de Análisis de Datos (FAD)**. El objetivo principal es realizar un análisis estadístico descriptivo y analítico (tanto para datos agrupados como no agrupados), visualización gráfica de datos y análisis preliminar sobre un dataset de **Mantenimiento Predictivo**.

---

## Estructura del Proyecto

La arquitectura del proyecto está organizada modularmente para facilitar la reutilización de código y mantener una separación clara entre la obtención de datos, el procesamiento estadístico y los informes finales.

```text
Analaisis-Estadistico-Mantenimiento-predictivo/
│
├── Datos/
│   └── predictive_maintenance_dataset.csv   # Dataset principal de trabajo
│
├── estadistica_analitica/
│   ├── __init__.py                          # Convierte la carpeta en paquete de Python
│   ├── utils.py                             # Funciones auxiliares de cálculo
│   │
│   ├── agrupados/                           # Módulo para análisis de datos agrupados
│   │   ├── __init__.py
│   │   ├── Frecuencias_Agrupados.py
│   │   ├── Tablas_Agrupados.py
│   │   ├── Tendencias_Agrupados.py
│   │   ├── Dispersion_Agrupados.py
│   │   └── Forma_Agrupados.py
│   │
│   ├── no_agrupados/                        # Módulo para análisis de datos no agrupados
│   │   ├── __init__.py
│   │   ├── tendencias.py
│   │   ├── dispersion.py
│   │   └── forma.py
│   │
│   └── graficos/                            # Módulo de generación de gráficos
│       ├── __init__.py
│       └── graficos.py
│
├── FAD_Practica_01_Equipo_02.pdf.pdf        # Reporte final/Documento técnico
├── main.py                                  # Punto de entrada principal
├── metadatos_ruta.txt                       # Registro o configuración de rutas
└── README.md                                # Documentación del repositorio
```
---


## Esqueleto del Proyecto (Post-Ejecución)

A continuación se muestra la estructura completa del proyecto generada automáticamente al ejecutar el script principal (`main.py`):

```text
Analaisis-Estadistico-Mantenimiento-predictivo/
├── main.py
├── FAD_Practica_01_Equipo_02.pdf
├── metadatos_ruta.txt
├── Datos/
│   └── predictive_maintenance_dataset.csv
├── estadistica_analitica/
│   ├── __init__.py
│   ├── utils.py
│   ├── graficos/
│   │   ├── __init__.py
│   │   └── graficos.py
│   ├── agrupados/
│   │   ├── __init__.py
│   │   ├── Tablas_Agrupados.py
│   │   ├── Tendencias_Agrupados.py
│   │   ├── Frecuencias_Agrupados.py
│   │   ├── Dispersion_Agrupados.py
│   │   └── Forma_Agrupados.py
│   └── no_agrupados/
│       ├── __init__.py
│       ├── tendencias.py
│       ├── forma.py
│       └── dispersion.py
├── Resultados_Agrupados/
│   ├── estadisticas_metric_5.txt
│   ├── estadisticas_metric_6.txt
│   ├── estadisticas_metric_9.txt
│   ├── tabla_frecuencias_metric_5.txt
│   ├── tabla_frecuencias_metric_6.txt
│   └── tabla_frecuencias_metric_9.txt
├── Resultados_No_Agrupados/
│   ├── estadisticas_metric_5.txt
│   ├── estadisticas_metric_6.txt
│   └── estadisticas_metric_9.txt
├── Resultados_Auditoria/
│   ├── auditoria_metric_5.txt
│   ├── auditoria_metric_6.txt
│   ├── auditoria_metric_9.txt
│   └── resumen_auditoria.txt
├── Resultados_Graficos_Agrupados/
│   ├── Histogram_metric_5.pdf
│   ├── Histogram_metric_6.pdf
│   ├── Histogram_metric_9.pdf
│   └── Boxplot_Agrupado.pdf
└── Resultados_Graficos_No_Agrupados/
    ├── Histograma_metric_5.pdf
    ├── Histograma_metric_6.pdf
    ├── Histograma_metric_9.pdf
    ├── Boxplot_No_Agrupado.pdf
    ├── Dispersion_Metricas.pdf
    └── Barras_Fallas.pdf
```

---

## Explicación del Proceso y Resultados Generados

### 1. Arquitectura Modular (`estadistica_analitica/`)
El proyecto se organiza de manera modular para garantizar la reutilización y claridad en los cálculos:
* **`agrupados/`**: Calcula las tablas de distribución de frecuencias, tendencia central, dispersión y forma utilizando intervalos de clase.
* **`no_agrupados/`**: Evalúa los datos cuantitativos exactos para obtener las métricas de tendencia central, dispersión y asimetría/curtosis sin agrupar.
* **`graficos/`**: Módulo responsable del renderizado de gráficos vectoriales utilizando librerías estándar como `matplotlib`.

### 2. Flujo de Ejecución (`main.py`)
Al ejecutar el script `main.py`, se realiza el siguiente procesamiento:
1. **Carga y Lectura de Datos:** Lee la fuente de datos desde `Datos/predictive_maintenance_dataset.csv`.
2. **Generación de Carpetas de Salida:** Se crean automáticamente los directorios `Resultados_Agrupados/`, `Resultados_No_Agrupados/`, `Resultados_Auditoria/`, `Resultados_Graficos_Agrupados/` y `Resultados_Graficos_No_Agrupados/`.
3. **Cálculos y Exportación de Textos:**
   * Archivos `.txt` en **Resultados_Agrupados/** con estadísticos descriptivos y tablas de frecuencias por métrica.
   * Archivos `.txt` en **Resultados_No_Agrupados/** con los estadísticos calculados de forma exacta.
   * Archivos `.txt` en **Resultados_Auditoria/** con la comparación y cálculo de errores relativos ($E_{rel}$) entre ambos enfoques.
4. **Generación de Gráficos Vectoriales (`.pdf`):**
   * Cada figura se ajusta con `fig.tight_layout()`, se exporta en formato vectorial `.pdf` para mantener máxima calidad gráfica y se cierra con `plt.close(fig)` para liberar memoria.


---

## Requisitos e Instalación

### Prerrequisitos
- **Python:** 3.10 o superior.
- **Git:** Instalado en el sistema para control de versiones.

### Librerías Sugeridas
Para ejecutar este script sin problemas, asegúrate de tener instaladas las siguientes dependencias de Python:

```bash
pip install pandas numpy matplotlib seaborn
```

---

## Instrucciones de Uso

Para ejecutar el análisis completo y generar los reportes y visualizaciones, ejecuta el archivo principal desde la raíz del proyecto:

```bash
python main.py
```

---

## Descripción de los Módulos

- **`main.py`**: Orquesta la carga de datos (`predictive_maintenance_dataset.csv`), invoca los cálculos estadísticos (agrupados y no agrupados) y genera las gráficas correspondientes.
- **`estadistica_analitica/agrupados/`**: Contiene módulos orientados a la agrupación en intervalos, construcción de tablas de frecuencias y cálculo de medidas de tendencia central, dispersión y forma.
- **`estadistica_analitica/no_agrupados/`**: Contiene las funciones de cálculo directo sobre series continuas o discretas sin reagrupar.
- **`estadistica_analitica/graficos/`**: Módulo encargado de la generación de histogramas, diagramas de caja (boxplots), gráficos de dispersión y de frecuencias.

---

## Guía para la Creación del Esqueleto (Línea de Comandos)

Si deseas recrear la estructura de carpetas y archivos vacíos desde tu terminal antes de subir a GitHub, puedes usar los siguientes comandos:

### En Bash / Terminal (Linux / macOS / Git Bash en Windows):

```bash
# 1. Crear directorio principal e ingresar
mkdir -p FAD_Practica_01_Equipo_02
cd FAD_Practica_01_Equipo_02

# 2. Crear las carpetas de la estructura
mkdir -p Datos
mkdir -p estadistica_analitica/agrupados
mkdir -p estadistica_analitica/no_agrupados
mkdir -p estadistica_analitica/graficos

# 3. Crear archivos en la raíz
touch main.py metadatos_ruta.txt README.md .gitignore

# 4. Crear archivos dentro de los módulos
touch estadistica_analitica/__init__.py
touch estadistica_analitica/utils.py

touch estadistica_analitica/agrupados/__init__.py
touch estadistica_analitica/agrupados/Frecuencias_Agrupados.py
touch estadistica_analitica/agrupados/Tablas_Agrupados.py
touch estadistica_analitica/agrupados/Tendencias_Agrupados.py
touch estadistica_analitica/agrupados/Dispersion_Agrupados.py
touch estadistica_analitica/agrupados/Forma_Agrupados.py

touch estadistica_analitica/no_agrupados/__init__.py
touch estadistica_analitica/no_agrupados/tendencias.py
touch estadistica_analitica/no_agrupados/dispersion.py
touch estadistica_analitica/no_agrupados/forma.py

touch estadistica_analitica/graficos/__init__.py
touch estadistica_analitica/graficos/graficos.py
```

### En PowerShell (Windows):

```powershell
# 1. Crear estructuras de carpetas
New-Item -ItemType Directory -Path "Datos", `
  "estadistica_analitica/agrupados", `
  "estadistica_analitica/no_agrupados", `
  "estadistica_analitica/graficos" -Force

# 2. Crear archivos principales
New-Item -ItemType File -Path "main.py", "metadatos_ruta.txt", "README.md", ".gitignore" -Force

# 3. Crear archivos de paquetes y scripts
New-Item -ItemType File -Path "estadistica_analitica/__init__.py", `
  "estadistica_analitica/utils.py", `
  "estadistica_analitica/agrupados/__init__.py", `
  "estadistica_analitica/agrupados/Frecuencias_Agrupados.py", `
  "estadistica_analitica/agrupados/Tablas_Agrupados.py", `
  "estadistica_analitica/agrupados/Tendencias_Agrupados.py", `
  "estadistica_analitica/agrupados/Dispersion_Agrupados.py", `
  "estadistica_analitica/agrupados/Forma_Agrupados.py", `
  "estadistica_analitica/no_agrupados/__init__.py", `
  "estadistica_analitica/no_agrupados/tendencias.py", `
  "estadistica_analitica/no_agrupados/dispersion.py", `
  "estadistica_analitica/no_agrupados/forma.py", `
  "estadistica_analitica/graficos/__init__.py", `
  "estadistica_analitica/graficos/graficos.py" -Force
```

---

## Recomendación para GitHub (`.gitignore`)

Es recomendable crear un archivo `.gitignore` para omitir los archivos temporales compilados de Python (`__pycache__` / `.pyc`) y configuraciones locales como `.vscode`:

```text
# .gitignore
__pycache__/
*.pyc
.vscode/
.DS_Store
```

---

## Autor y Créditos

**Cecil Quimey Azuara Yáñez**

- **Carrera:** Licenciatura en Ingeniería de Datos e Inteligencia Artificial (LIDIA).
- **Institución:** Universidad de Guanajuato – División de Ingenierías (Campus Irapuato - Salamanca).
- **Asignatura:** Fundamentos del Análisis de Datos.
