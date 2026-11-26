# Predicción del Rendimiento Académico en Matemáticas

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.2%2B-F7931E?logo=scikitlearn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?logo=pandas&logoColor=white)
![Metodología](https://img.shields.io/badge/Metodolog%C3%ADa-CRISP--DM-informational)
![Estado](https://img.shields.io/badge/Estado-T%C3%A9cnico_Consolidado-success)

Proyecto desarrollado para la asignatura **SCY1102 — Gestión de Proyectos de Ciencia de Datos (Duoc UC)**, enfocado en el **Caso 1: Educación (Rendimiento Académico Estudiantil)**.

---

## 1. Contexto y Problema de Negocio

En una institución de educación secundaria, el equipo directivo y docente detectó bajos resultados sistemáticos en las evaluaciones de matemáticas. Las autoridades requieren comprender con rigor analítico los determinantes del rendimiento para diseñar e implementar **estrategias oportunas de acompañamiento académico y tutorías preventivas**.

El proyecto utiliza el dataset [`neuralsorcerer/student-performance`](https://www.kaggle.com/datasets/neuralsorcerer/student-performance) (más de 8 millones de registros en entrenamiento y 1 millón en validación/test), abordándolo mediante la metodología **CRISP-DM**.

---

## 2. Decisiones Técnicas y Metodológicas

### Enfoque de Modelado
Se formuló como un problema de **regresión supervisada continua** sobre la variable objetivo `TestScore_Math` (escala 0 a 100), evitando la imposición de categorías arbitrarias ("bajo", "medio", "alto") sin respaldo formal institucional.

### Variables Predictoras (9 Atributos)
1. `AttendanceRate`: Tasa de asistencia regular del estudiante.
2. `StudyHours`: Horas de estudio dedicadas (unidad a contrastar con diccionario institucional).
3. `Age`: Edad del estudiante.
4. `Grade`: Nivel o grado académico cursado.
5. `SES_Quartile`: Cuartil socioeconómico.
6. `ParentalEducation`: Máximo nivel educativo de los padres o apoderados.
7. `ParentSupport`: Nivel de apoyo parental percibido.
8. `InternetAccess`: Disponibilidad de conexión a internet domiciliaria (0/1).
9. `Extracurricular`: Participación en actividades extracurriculares (0/1).

### Exclusiones Críticas Justificadas
- **Fuga de Información (*Data Leakage*):** Se descartaron `TestScore_Reading`, `TestScore_Science` y `GPA`. Al medirse en el mismo período de evaluación, incorporarlas impediría el uso del modelo como herramienta de alerta temprana predictiva.
- **Ética y Mitigación de Sesgos:** Se excluyeron `Gender` y `Race` para garantizar que las recomendaciones de apoyo institucional no reproduzcan sesgos sobre atributos protegidos.

---

## 3. Resultados de Modelado y Evaluación (Conjunto Test)

Se evaluaron tres modelos con un conjunto ciego de **500.000 estudiantes** en Test:

| Modelo | MAE (puntos) | RMSE (puntos) | R² | % dentro de ±5 pts | % dentro de ±10 pts |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Línea base (Promedio)** | 7.968 | 9.952 | -0.000 | 38.21% | 68.22% |
| **Regresión Lineal** | 4.553 | 5.695 | 0.672 | 61.74% | 92.22% |
| **Gradient Boosting (Ganador)** | **4.550** | **5.694** | **0.673** | **61.78%** | **92.16%** |

### Hallazgos Principales
- **Reducción del error:** El modelo `HistGradientBoostingRegressor` reduce el error en un **42.7%** respecto a la línea base y muestra consistencia total sin sobreajuste (brecha train/val de 0.4%, sesgo medio de -0.01 puntos).
- **Importancia de variables (Permutación):** `AttendanceRate` es el predictor preponderante (+6.645 puntos de aumento en RMSE al permutarlo), seguido de `StudyHours` (+0.166 puntos).
- **Invarianza categórica:** Factores como educación de los padres, internet o actividades extracurriculares presentan diferencias marginales en promedio (máximo 0.04 puntos), evidenciando que el hábito y la asistencia presencial dominan el rendimiento.
- **Umbral de apoyo académico:** Se fijó en **68.25 puntos** (percentil 25 de la distribución histórica), permitiendo priorizar al 25% de estudiantes con mayor urgencia de nivelación.

---

## 4. Estructura del Repositorio

```text
Gestion/
├── .agents/
│   ├── rules/
│   │   └── proyecto-scy1102.md       # Reglas obligatorias de workspace y ahorro de tokens
│   └── skills/                       # Skills operativas para Antigravity
│       ├── ds-repo-cleanup/          # Limpieza y consolidación del repositorio
│       ├── streamlit-dashboard/      # Dashboard interactivo con vistas ejecutiva y técnica
│       ├── github-pm-cli/            # Gestión de seguimiento CRISP-DM con gh CLI
│       ├── ep5-informe-duoc/         # Redacción y formato del informe EP5 (5-8 págs.)
│       └── ep6-presentacion-duoc/    # Láminas ejecutivas EP6 y guion de defensa
├── archive/                          # Notebooks y experimentos versionados anteriores
│   ├── EDA_matematicas_sencillo.ipynb
│   ├── Modelado_matematicas_y_automatizacion.ipynb
│   └── modelo_matematicas.ipynb
├── data/
│   └── raw/                          # Datasets originales (ignorado por .gitignore)
├── docs/
│   └── contexto/                     # Resúmenes de materia, rúbricas EP5/EP6 y guías
├── entradas/                         # Archivos CSV de prueba para inferencia
│   ├── nuevos_estudiantes.csv
│   └── muestra_con_puntaje_real.csv
├── models/                           # Artefactos y serialización de modelos
│   ├── modelo_matematicas.joblib     # Pipeline entrenado con HistGradientBoostingRegressor
│   ├── metadatos.json                # Metadatos del modelo, features y umbral
│   └── resumen_metricas.json         # Métricas para alimentación ágil del dashboard
├── notebooks/                        # Cuadernos Jupyter consolidados y limpios
│   ├── 01_EDA_matematicas.ipynb      # Análisis exploratorio completo con conclusiones reales
│   └── 02_Modelado_y_automatizacion.ipynb # Pipeline, comparación, evaluación y CLI
├── salidas/                          # Resultados generados por la automatización
├── src/                              # Código fuente modular en producción
│   └── automatizacion_matematicas.py # Script CLI para predicción y monitoreo de drift
├── .gitignore                        # Reglas de exclusión de datos masivos y temporales
├── README.md                         # Documentación técnica principal del proyecto
└── requirements.txt                  # Dependencias del entorno Python
```

---

## 5. Instalación y Uso

### 5.1 Requisitos Previos
Clonar el repositorio y configurar un entorno virtual con Python 3.10 o superior:

```bash
git clone https://github.com/ijnacios/gestion.git
cd gestion
python -m venv .venv
source .venv/bin/activate  # En Linux/macOS
.venv\Scripts\activate     # En Windows
pip install -r requirements.txt
```

### 5.2 Inferencia Automatizada (Script CLI)
Para procesar un nuevo listado de estudiantes y generar las alertas de apoyo académico:

```bash
python src/automatizacion_matematicas.py --entrada entradas/nuevos_estudiantes.csv
```

Para procesar un lote con monitoreo automático de deriva de datos (*drift monitoring*):

```bash
python src/automatizacion_matematicas.py --entrada entradas/muestra_con_puntaje_real.csv
```

El script genera automáticamente el archivo con predicciones y rango de error en `salidas/` y registra la ejecución en `registro.log`.

---

## 6. Equipo y Asignatura

- **Asignatura:** SCY1102 — Gestión de Proyectos de Ciencia de Datos
- **Institución:** Duoc UC
- **Evaluaciones Asociadas:** EP5 (Informe Técnico de Avance y Control) y EP6 (Presentación Ejecutiva y Defensa Final)
