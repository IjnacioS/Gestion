# Reporte de Estado y Avance de Proyecto (Alineado con Plan EP3)
**Asignatura:** SCY1102 — Gestión de Proyectos de Datos (Duoc UC)  
**Docente:** Michael Palomino B.  
**Proyecto:** Caso 1 — Sistema de Alerta Temprana para el Rendimiento Académico en Matemáticas  
**Equipo:** Ignacio Sobarzo · Diego Yañez · Felipe Espinoza  
**Actores del Proyecto (Plan EP3):** Dirección (Sponsor), UTP (Contraparte), Docentes de Matemáticas, Orientación y TI  
**Repositorio GitHub:** [IjnacioS/Gestion](https://github.com/IjnacioS/Gestion)  
**Fecha de corte:** Noviembre 2026  

---

## 1. Resumen Ejecutivo y Estado Semáforo

El proyecto completó al 100% los hitos técnicos y de gestión comprometidos en el Plan de la Evaluación Parcial N°3 (EP3), articulando la exploración de datos (10M de registros), el flujo de preparación sin fuga de información ni sesgos, el modelo ganador **Gradient Boosting** (`HistGradientBoostingRegressor`), la automatización por lotes y el Dashboard interactivo en Streamlit con los 3 niveles de alerta para UTP y Orientación.

| Dimensión | Indicador Semáforo | Estado | Comentario Ejecutivo y Vínculo con Plan EP3 |
| :--- | :---: | :---: | :--- |
| **Tiempo / Cronograma** | 🟢 | **En Plazo** | Hitos H1 a H6 ejecutados dentro de los plazos comprometidos para EP5 y EP6. |
| **Alcance Técnico (E1–E6)** | 🟢 | **100% Ejecutado** | Modelo Gradient Boosting ($\text{RMSE}=5,694$; $\text{MAE}=4,550$; $R^2=0,673$), script CLI y Dashboard operativos. |
| **Cumplimiento RF y RNF** | 🟢 | **100% Validado** | **RF3** superado (42,7% ~ 43% menos error vs. $\ge 10\%$ exigido); **RF4** con 3 niveles de alerta; **RNF1** (Ley 19.628); **RNF2** (brecha 0,03 pts $\le 10$ pts); **RNF5** (`.gitignore`). |
| **Control de Desviaciones y Riesgos** | 🟢 | **Controlado** | 3 desviaciones cerradas en GitHub; **Issue #14** activó la contingencia del **Riesgo R4** de EP3 (bienestar emocional), junto con la mitigación de **R2, R3 y R7**. |
| **Entregables de Cierre (E7)** | 🟢 | **Entregados** | Informe EP5 (`.docx`/`.pdf`) y Presentación + Guion EP6 (`.pptx`/`.md`) generados en `docs/entregables/`. |

---

## 2. Vinculación de Milestones GitHub (M1–M4) con Hitos (H1–H6) y Entregables (E1–E7) de EP3

| Milestone GitHub | Hitos Plan EP3 | Entregables Plan EP3 | Issues | % Avance | Estado |
| :--- | :--- | :--- | :---: | :---: | :---: |
| [**M1: Comprensión y EDA**](https://github.com/IjnacioS/Gestion/milestone/1) | **H1 y H2** (Negocio y Datos) | **E1** (Ficha alcance) y **E2** (Notebook EDA) | 4 / 4 | **100%** | 🟢 Cerrado |
| [**M2: Preparación y Modelado**](https://github.com/IjnacioS/Gestion/milestone/2) | **H3 y H4** (Pipeline y Modelo) | **E3** (Pipeline) y **E4** (Modelo serializado) | 4 / 4 | **100%** | 🟢 Cerrado |
| [**M3: Automatización y Dashboard**](https://github.com/IjnacioS/Gestion/milestone/3) | **H5** (Operación y App Web) | **E5** (Script CLI) y **E6** (Dashboard Streamlit) | 3 / 3 | **100%** | 🟢 Cerrado |
| [**M4: Consolidación, Informe EP5 y Defensa EP6**](https://github.com/IjnacioS/Gestion/milestone/4) | **H6** (Cierre y Defensa) | **E7** (Informe EP5 + Presentación y Guion EP6) | 3 / 3 listos | **100%** | 🟢 En Cierre Hoy |

---

## 3. Matriz de Trazabilidad: Planificado vs. Ejecutado

| ID | Issue en GitHub | Hito / Entregable EP3 | Milestone | Estado | Evidencia Técnica Construida |
| :---: | :--- | :--- | :---: | :---: | :--- |
| **#1** | [#1 chore: configurar estructura inicial y requisitos](https://github.com/IjnacioS/Gestion/issues/1) | H1 / E1 (RNF5) | M1 | Closed | `requirements.txt`, `.gitignore` (bloquea `data/raw/*.csv`). |
| **#2** | [#2 eda: realizar analisis exploratorio y visualizaciones](https://github.com/IjnacioS/Gestion/issues/2) | H2 / E2 | M1 | Closed | [`notebooks/01_EDA_matematicas.ipynb`](../notebooks/01_EDA_matematicas.ipynb). |
| **#3** | [#3 feat: preparar datos y dividir conjuntos](https://github.com/IjnacioS/Gestion/issues/3) | H3 / E3 (RF1, RF2, RNF2) | M2 | Closed | Pipeline sin fuga ni atributos protegidos en [`notebooks/02_Modelado_y_automatizacion.ipynb`](../notebooks/02_Modelado_y_automatizacion.ipynb). |
| **#4** | [#4 feat: entrenar modelos baseline y diagnosticar](https://github.com/IjnacioS/Gestion/issues/4) | H4 / E4 | M2 | Closed | Comparativa en Test (500k): Línea base, Regresión Lineal y Gradient Boosting. |
| **#5** | [#5 feat: optimizacion y seleccion del modelo campeon](https://github.com/IjnacioS/Gestion/issues/5) | H4 / E4 (RF3) | M2 | Closed | [`models/modelo_matematicas.joblib`](../models/modelo_matematicas.joblib) (-42,7% error vs. base) y [`models/resumen_metricas.json`](../models/resumen_metricas.json). |
| **#6** | [#6 feat: pipeline de automatizacion batch](https://github.com/IjnacioS/Gestion/issues/6) | H5 / E5 | M3 | Closed | [`src/automatizacion_matematicas.py`](../src/automatizacion_matematicas.py) y bitácora [`registro.log`](../registro.log). |
| **#7** | [#7 feat: desarrollo de dashboard interactivo en Streamlit](https://github.com/IjnacioS/Gestion/issues/7) | H5 / E6 (RF4) | M3 | Closed | [`dashboard/app.py`](../dashboard/app.py) con 3 niveles de recomendación en el simulador. |
| **#8** | [#8 feat: prediccion por lotes CSV y monitoreo de drift](https://github.com/IjnacioS/Gestion/issues/8) | H5 / E6 | M3 | Closed | Nómina por curso en `app.py`, alerta de drift (>20% RMSE), [`entradas/`](../entradas/) y [`salidas/`](../salidas/). |
| **#9** | [#9 docs: redaccion de informe ejecutivo y tecnico EP5](https://github.com/IjnacioS/Gestion/issues/9) | H6 / E7 | M4 | **Entregado** | [`docs/entregables/Informe_EP5_Caso1_Matematicas.docx`](entregables/Informe_EP5_Caso1_Matematicas.docx) (5–8 págs.). |
| **#10** | [#10 docs: diseno de presentacion ejecutiva 10 min EP6](https://github.com/IjnacioS/Gestion/issues/10) | H6 / E7 | M4 | **Listo** | [`docs/entregables/Presentacion_EP6_Caso1_Matematicas.pptx`](entregables/Presentacion_EP6_Caso1_Matematicas.pptx) (11 láminas). |
| **#11** | [#11 docs: elaboracion de guion de defensa y FAQ EP6](https://github.com/IjnacioS/Gestion/issues/11) | H6 / E7 | M4 | **Listo** | [`docs/entregables/Guion_Defensa_EP6.md`](entregables/Guion_Defensa_EP6.md). |

---

## 4. Control de Desviaciones y Mitigación de Riesgos del Plan EP3

| Ref. | Desviación / Riesgo EP3 | Impacto | Acción Correctiva y Mitigación Implementada | Estado |
| :---: | :--- | :--- | :--- | :---: |
| [**#12**](https://github.com/IjnacioS/Gestion/issues/12) | **Volumen masivo (8M+ filas en `train.csv`)** saturaba la memoria local. | Iteraciones >45 min por corrida. | Muestreo validado de 500.000 registros comprobando convergencia en curva de aprendizaje (-90% en tiempo de cómputo). | 🟢 **Cerrada** |
| [**#13**](https://github.com/IjnacioS/Gestion/issues/13) | **Tres notebooks duplicados** con experimentos paralelos y textos pendientes. | Riesgo de inconsistencia técnica. | Consolidación en 2 notebooks oficiales (`01_EDA` y `02_Modelado`) y respaldo de versiones previas en `archive/` (Commit `96d4123`). | 🟢 **Cerrada** |
| [**#14**](https://github.com/IjnacioS/Gestion/issues/14) | **Conexión con Riesgo R4 (EP3):** Ausencia de variable de bienestar emocional y diccionario 0/1. | Falta de dimensión socioemocional directa. | Se activó la contingencia prevista en R4: documentación explícita del límite en el Dashboard e Informe EP5 y propuesta de encuesta semestral junto a Orientación. | 🟢 **Cerrada** |
| **R2, R3, R7** | **Riesgos Éticos y Pedagógicos (EP3):** Sesgo (R2), mal uso punitivo (R3) y correlación $\ne$ causalidad (R7). | Decisiones escolares sesgadas o punitivas. | **R2:** excluidos `Gender` y `Race` (brecha por educación parental de 0,03 pts $\le 10$ pts, RNF2). **R3 y R7:** simulador con 3 niveles formativos para UTP/Orientación y advertencia explícita en la interfaz. | 🟢 **Mitigados** |
