# Analisis Estadistico y Mantenimiento Predictivo


# Práctica 01 - Análisis Estadístico y Mantenimiento Predictivo

Este repositorio contiene la implementación y desarrollo de la **Práctica 01** del curso de **Fundamentos de Análisis de Datos (FAD)**. El objetivo principal es realizar un análisis estadístico descriptivo y analítico (tanto para datos agrupados como no agrupados), visualización gráfica de datos y análisis preliminar sobre un dataset de **Mantenimiento Predictivo**.

---

## Estructura del Proyecto

La arquitectura del proyecto está organizada modularmente para facilitar la reutilización de código y mantener una separación clara entre la obtención de datos, el procesamiento estadístico y los informes finales.

```text
FAD_Practica_01_Equipo_02/
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
