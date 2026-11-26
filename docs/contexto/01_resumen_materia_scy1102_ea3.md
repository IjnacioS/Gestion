# Resumen Extenso de Materia — SCY1102 Gestión de Proyectos de Datos (EA3)

Este documento consolida todo el contenido teórico, técnico y metodológico de la **Experiencia de Aprendizaje 3 (EA3): Ejecución, monitoreo y control del proyecto** de la asignatura **SCY1102 — Gestión de Proyectos de Datos (Duoc UC)**, integrando las presentaciones y guías oficiales (Actividades 3.1, 3.2, 3.3 y 3.4) junto con referencias técnicas externas actualizadas para ejecutar con rigor las evaluaciones **EP5 (Encargo)** y **EP6 (Presentación)**.

---

## 1. Marco Curricular de la Unidad (EA3)

- **Resultado de Aprendizaje (RA3):** Implementa un proyecto de ciencia de datos realizando acciones de ejecución, monitoreo y control del proyecto, por medio de herramientas de gestión y reportes de estados de avance, para resguardar el cumplimiento del plan.
- **Indicadores de Logro:**
  - **IL 3.1:** Aplica herramientas de programación en las etapas del ciclo de desarrollo para la implementación del proyecto de ciencia de datos.
  - **IL 3.2:** Utiliza herramientas de gestión de proyectos para registrar y dar seguimiento al avance de las tareas y actividades planificadas en el proyecto de ciencia de datos.
  - **IL 3.3:** Defiende el proyecto ante clientes y/o actores relevantes de la organización para evidenciar el cumplimiento del plan del proyecto de ciencia de datos.

**Qué se espera demostrar al cierre de EA3:**
1. Que el proyecto **funciona técnica y metodológicamente**.
2. Que el equipo **gestionó el proyecto y controló las desviaciones** (evidenciando seguimiento real, no solo planificación estática).
3. Que los resultados pueden **comunicarse y defenderse de forma ejecutiva**, traduciendo hallazgos técnicos en decisiones de negocio.

---

## 2. Actividad 3.1 — Implementación Técnica de un Proyecto de Ciencia de Datos

### 2.1 Del Plan a la Implementación
Ejecutar un proyecto de ciencia de datos significa traducir la planificación (alcance, cronograma, metodología) en **soluciones técnicas funcionales, reproducibles y trazables**. El rol del programador / *data scientist* no se limita a escribir código, sino a tomar **decisiones técnicas fundamentadas** (selección de variables, prevención de fuga de datos, elección de algoritmo, umbrales de alerta) alineadas al objetivo de negocio.

### 2.2 Ciclo Técnico y Trazabilidad CRISP-DM
La asignatura utiliza la metodología estándar [CRISP-DM (Cross-Industry Standard Process for Data Mining)](https://www.ibm.com/docs/es/spss-modeler/saas?topic=dm-crisp-help-overview), estructurada en seis fases iterativas:

| Fase CRISP-DM | Propósito Principal | Entregables Técnicos Esperados |
| :--- | :--- | :--- |
| 1. Comprensión del negocio | Definir problema, objetivos, KPIs y restricciones | Enunciado de problema, criterios de éxito, supuestos |
| 2. Comprensión de los datos | Explorar fuentes, distribuciones, calidad y sesgos | Notebook de EDA, perfilamiento de calidad, gráficos clave |
| 3. Preparación de los datos | Limpiar, imputar, escalar, codificar y crear *features* | Script/Pipeline de preprocesamiento, división train/val/test |
| 4. Modelado | Seleccionar algoritmos, entrenar y ajustar hiperparámetros | Modelos candidatos (línea base + modelos supervisados) |
| 5. Evaluación | Medir desempeño en datos no vistos y validar valor de negocio | Tabla de métricas, análisis de errores/residuos, curva de aprendizaje |
| 6. Despliegue | Poner el modelo a disposición de usuarios o procesos | Script de automatización, dashboard interactivo, monitoreo de *drift* |

### 2.3 Herramientas de Programación y Buenas Prácticas
- **Python** como lenguaje estándar del ecosistema de datos.
- **Librerías clave:**
  - *Manipulación de datos:* `pandas`, `numpy`.
  - *Modelado y ML:* `scikit-learn`, `joblib` (serialización de modelos).
  - *Visualización y dashboards:* `matplotlib`, `seaborn`, `plotly`, `streamlit`.
  - *Automatización:* scripts CLI (`argparse`, `logging`, `pathlib`), tareas programadas (`cron`, Programador de Tareas de Windows o GitHub Actions).
- **Buenas prácticas obligatorias:** combinar **notebooks** (para exploración, narrativa y trazabilidad), **scripts modulares `.py`** (para automatización y producción) y **control de versiones con Git/GitHub** (commits descriptivos, `.gitignore` para no subir CSVs masivos ni entornos virtuales, `requirements.txt` actualizado).

### 2.4 Preparación de Datos y *Feature Engineering*
- **Limpieza y transformación:** revisar valores faltantes, filas duplicadas, tipos de datos y rangos válidos. No eliminar outliers ni duplicados automáticamente sin entender su origen.
- **Prevención de fuga de información (*data leakage*):**
  - Excluir variables que se miden en el mismo instante que la variable objetivo o que la contienen implícitamente (por ejemplo, en educación, excluir `GPA` o puntajes de otras pruebas del mismo examen al predecir `TestScore_Math`).
  - Separar los conjuntos (`train`, `validation`, `test`) **antes** de ajustar imputadores, escaladores o codificadores.
- **Encapsulamiento reproducible con Scikit-Learn:** utilizar [`Pipeline`](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html) y [`ColumnTransformer`](https://scikit-learn.org/stable/modules/generated/sklearn.compose.ColumnTransformer.html) para que todas las transformaciones (imputación por mediana/moda, `StandardScaler`, `OneHotEncoder(handle_unknown="ignore")`) se aprendan exclusivamente con `train` y se apliquen de forma idéntica en `validation`, `test` y datos nuevos en producción.

### 2.5 Modelado, Evaluación y Validación
- **Línea base (*baseline*):** siempre entrenar primero un modelo ingenuo (por ejemplo, `DummyRegressor(strategy="mean")`) para verificar si los modelos reales aportan mejora real.
- **Comparación progresiva de modelos:** iniciar con modelos interpretables (ej. `LinearRegression`) y contrastar con modelos no lineales o de ensamble (ej. `RandomForestRegressor`, `HistGradientBoostingRegressor`).
- **Métricas según tipo de problema:**
  - *Regresión (puntajes continuos):* **MAE** (error absoluto medio en la unidad original), **RMSE** (penaliza más errores grandes), **R²** (proporción de varianza explicada) y métricas orientadas a negocio (ej. % de predicciones dentro de ±5 o ±10 puntos).
  - *Clasificación:* Accuracy, Precision, Recall, F1-Score, ROC-AUC y Matriz de Confusión.
- **Validación y control de sobreajuste (*overfitting*):**
  - Comparar métricas de entrenamiento vs. validación (una brecha grande indica sobreajuste).
  - Usar validación cruzada ([`cross_val_score`](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_val_score.html)) o un conjunto dedicado de `validation` para elegir modelo e hiperparámetros, reservando `test` estrictamente para la evaluación final honesta.
  - Complementar con **análisis de residuos** (errores centrados en cero, sin sesgos sistemáticos por subgrupo), **curvas de aprendizaje** (para saber si más datos mejorarían el error o si se necesitan nuevas variables) e **importancia de variables** (ej. *permutation importance*).

### 2.6 Monitoreo del Modelo, Dashboards, Automatización y Despliegue
- **Qué pasa después del entrenamiento:** los modelos se degradan con el tiempo debido a:
  - **Data Drift:** cambios en la distribución de las variables de entrada (ej. cambia el perfil de asistencia o estudio de nuevas cohortes).
  - **Concept Drift:** cambios en la relación entre variables de entrada y resultado (ej. cambia la metodología pedagógica o la escala de evaluación).
  - **Acción práctica:** registrar logs de ejecución y recalcular métricas (ej. RMSE) cuando ingresan nuevos datos con puntaje real, disparando una alerta de reentrenamiento si el error supera un umbral (ej. +20% respecto al RMSE de validación).
- **Dashboards técnicos vs. ejecutivos:**
  - *Técnico:* métricas de error (MAE/RMSE/R²), distribución de residuos, importancia de variables, estado de *drift* y calidad de datos.
  - *Ejecutivo:* KPIs de negocio, perfiles de riesgo (ej. porcentaje de estudiantes bajo umbral de apoyo), simulador de escenarios (*what-if*) y recomendaciones accionables. El dashboard debe concebirse como **producto final para tomar decisiones**, no como una colección aislada de gráficos.
- **Automatización y operación:** empaquetar el pipeline serializado (`.joblib`) + archivo de metadatos (`.json` con variables esperadas, umbral y versión de `scikit-learn`) + script automatizable por lote (CSV de entrada -> validación de esquema -> predicción + rango de incertidumbre + bandera de alerta -> CSV de salida + `registro.log`).

### 2.7 Los 8 Pasos Prácticos de la Guía 3.1.2
Para asegurar cobertura total del indicador IL 3.1, el notebook/código técnico debe evidenciar:
1. Carga del dataset del proyecto.
2. Análisis de clases/categorías y gráficos representativos.
3. Preparación de datos y selección justificada de variables dependiente e independientes.
4. Separación en conjuntos de entrenamiento, validación y test.
5. Entrenamiento del modelo y veredicto crítico sobre si los pasos previos fueron suficientes.
6. Evaluación de resultados con métricas de desempeño.
7. Uso del modelo con datos nuevos para generar 5 predicciones interpretadas.
8. Propuesta e implementación de una automatización funcional.

---

## 3. Actividad 3.2 — Monitoreo y Control de un Proyecto de Ciencia de Datos

### 3.1 Por Qué el Seguimiento Es Crítico en Ciencia de Datos
A diferencia del software tradicional, los proyectos de datos enfrentan **alta incertidumbre técnica** (calidad real de los datos, poder predictivo incierto), **iteraciones frecuentes**, dependencia de roles especializados (*Data Engineer*, *Data Scientist*, *Product Owner*) y el riesgo de **"avanzar mucho técnicamente sin generar valor real"**.

En línea con el enfoque orientado a la entrega de valor y dominios de desempeño de la [Guía PMBOK® 8va Edición del PMI](https://www.pmi.org/standards/pmbok) (6 principios, 7 dominios de desempeño y 5 áreas de enfoque que integran ejecución, monitoreo y control), controlar un proyecto no es burocracia ni castigo, sino **gestión adaptativa basada en evidencia**.

### 3.2 Las 5 Dimensiones Clave del Control
1. **Cronograma:** hitos, tareas, fechas planificadas vs. reales y dependencias.
2. **Alcance:** entregables comprometidos vs. efectivamente construidos (evitar *scope creep* o recortes sin justificación).
3. **Recursos:** carga de trabajo del equipo, uso de tiempo y disponibilidad de herramientas/cómputo.
4. **Calidad:** validación de integridad de datos, desempeño de modelos (sin fuga ni sobreajuste) y usabilidad de dashboards.
5. **Riesgos:** técnicos (datos masivos, faltantes, *drift*), éticos (uso de variables sensibles como género o etnia, etiquetado indebido de personas) y operacionales (reproducibilidad, dependencias de entorno).

### 3.3 Herramientas Modernas de Seguimiento
La asignatura valida el uso sistemático de herramientas digitales para dar transparencia y trazabilidad:
- **GitHub (Issues, Milestones, Projects/Kanban):** ideal para integrar directamente el control técnico (commits, ramas, pull requests) con el seguimiento de gestión.
- **Jira / Trello:** tableros visuales Kanban (`Pendiente / To Do`, `En Progreso / Doing`, `Completada / Done`) y sprints.
- **Notion / Hojas de Cálculo (Sheets) / BI:** documentación viva, matrices de hitos y reportes ejecutivos.

**Estructura mínima de seguimiento (Guía 3.2.2):**
- **Hitos:** puntos clave de validación que marcan el progreso.
- **Tareas:** actividades concretas y medibles asociadas a cada hito.
- **Responsable:** persona asignada.
- **Fechas:** inicio y término (planificado vs. real).
- **Dependencias:** qué tarea debe finalizar antes de iniciar la siguiente.
- **Estado:** Pendiente / En Progreso / Completada / Bloqueada.

### 3.4 Reportes de Estado de Avance
Un reporte efectivo está pensado para **stakeholders no técnicos** (menos texto denso, más síntesis y visualización) y responde a **4 preguntas fundamentales**:
1. ¿Qué estaba planificado?
2. ¿Qué se ha avanzado?
3. ¿Qué desviaciones existen?
4. ¿Qué decisiones o acciones se requieren?

**Componentes sugeridos de un reporte de avance:**
- **Estado general tipo semáforo:** Verde (en curso según plan), Amarillo (desviación controlada con acción correctiva), Rojo (riesgo crítico que requiere escalamiento).
- **Avance por hito (%).**
- **Principales logros del período.**
- **Desviaciones detectadas y causas raíz.**
- **Riesgos activos, prioridades próximas y acciones correctivas.**

### 3.5 Control de Desviaciones y Acciones Correctivas
Registrar desviaciones reales **demuestra madurez en gestión, no un error**.

- **Causas frecuentes de desviación en ciencia de datos:**
  - Retrasos por problemas de calidad o volumen inesperado de datos (ej. dataset de millones de filas que supera la RAM local).
  - Mayor esfuerzo en limpieza, verificación de diccionario de datos o prevención de fuga de información.
  - Cambios de requerimientos del cliente o redefinición del alcance.
  - Limitaciones de infraestructura, acceso o versiones de librerías.
- **Las 5 opciones de control (acciones correctivas):**
  1. **Repriorizar tareas** (enfocar esfuerzo en el camino crítico y entregables de mayor valor).
  2. **Ajustar alcance** (negociar entregables o trabajar con muestras estadísticamente validadas).
  3. **Redistribuir recursos** (rebalancear carga entre integrantes del equipo).
  4. **Aumentar automatización** (reemplazar ejecuciones manuales repetitivas por scripts/pipelines).
  5. **Escalar decisiones al sponsor/cliente** (cuando una definición institucional, como el umbral de apoyo académico, excede al equipo técnico).

---

## 4. Actividad 3.3 — Consolidación de Resultados y Storytelling

### 4.1 Visión Integral: Del Problema al Valor
Al consolidar el proyecto se deben conectar cinco piezas en un hilo único y coherente:
1. Problema / oportunidad abordada.
2. Objetivo del proyecto.
3. Principales entregables funcionales.
4. Usuario o cliente objetivo.
5. Valor generado (impacto esperado en la toma de decisiones).

### 4.2 Matriz de Consolidación (Guía 3.3.2)
Herramienta puente entre el trabajo técnico y la comunicación ejecutiva que vincula tres columnas:
- **Entregable técnico:** análisis de datos, modelos entrenados, métricas de desempeño y automatización.
- **Evidencia de gestión:** cumplimiento de hitos, tablero actualizado, control de desviaciones y acciones correctivas.
- **Mensaje clave para el cliente:** principales *insights* accionables traducidos a lenguaje de negocio.

### 4.3 Estructura del Informe Final Integrado
Debe ser un **documento único, coherente y trazable** que integre:
1. Contexto y objetivos del proyecto.
2. Desarrollo técnico documentado (enfoque en decisiones técnicas, diagramas de flujo de datos y visualizaciones claras, no solo bloques de código).
3. Gestión del proyecto y seguimiento (planificado vs. real, evidencias de herramienta, reportes de avance, desviaciones y acciones correctivas).
4. Resultados, conclusiones y limitaciones (honestidad metodológica: correlación ≠ causalidad, variables faltantes, consideraciones éticas).
5. Próximos pasos y recomendaciones.

### 4.4 Storytelling con Datos y Presentación Ejecutiva
Los datos cuentan una historia, no se presentan solos. Para defender ante stakeholders se recomienda:
- **Menos detalle de código, más impacto, valor, riesgos y decisiones.**
- **Estructura narrativa en 5 pasos:**
  1. Situación inicial / problema.
  2. Enfoque y solución propuesta.
  3. Evidencia (datos + visuales claros).
  4. Resultados y valor generado.
  5. Recomendaciones finales.
- **Regla de balance visual (Guía 3.3.2):** combinar láminas técnicas (metodología, arquitectura del pipeline/modelo, métricas) con láminas ejecutivas (problema de negocio, hallazgos clave, impacto y próximos pasos).
- **Dos preguntas que toda lámina debe ayudar a responder:** *¿Por qué esto importa?* y *¿Qué decisión habilita?*

---

## 5. Actividad 3.4 — Presentación y Defensa del Proyecto Final

### 5.1 Guion Estructural de la Defensa Ejecutiva (10 minutos)
La presentación final debe cubrir secuencialmente:
1. **Contexto y problema de negocio:** situar al cliente, contexto sectorial, problema detectado, impacto esperado y stakeholders clave.
2. **Objetivo del proyecto y criterios de éxito:** objetivo general, objetivos específicos, KPIs/métricas de éxito, supuestos y restricciones.
3. **Metodología y trazabilidad CRISP-DM:** fases aplicadas, qué se hizo en cada fase, entregables y cómo se validaron.
4. **Implementación técnica:** fuentes de datos, preparación, herramientas (Python, notebooks, librerías), modelos desarrollados, automatización y dashboard.
5. **Resultados obtenidos:** hallazgos clave, métricas de desempeño, visualizaciones y comparación vs. línea base / situación inicial.
6. **Gestión del proyecto:** planificación inicial (fases, tareas, hitos), herramientas usadas (Kanban/GitHub/Gantt), estado del proyecto y lecciones.
7. **Monitoreo y control:** indicadores de avance, gestión de riesgos, desviaciones detectadas, ajustes y decisiones tomadas.
8. **Valor entregado y cumplimiento del plan:** grado de cumplimiento del alcance, beneficios concretos y evidencias verificables.
9. **Conclusiones y próximos pasos:** conclusiones, limitaciones actuales, recomendaciones y escalabilidad futura.

### 5.2 Perspectivas del Jurado / Audiencia (Guía 3.4.2)
Durante la ronda de preguntas, el docente o los evaluadores adoptan tres roles críticos; el equipo debe prepararse para responder a todos:
- **Cliente / Contraparte del proyecto:** pregunta por utilidad práctica, interpretación de resultados, umbrales de intervención, ética y acciones concretas.
- **Gerente de Informática / Técnico:** pregunta por arquitectura, calidad de datos, prevención de *data leakage*, por qué se eligió un algoritmo sobre otro, reproducibilidad, *drift* y automatización.
- **Gerente General / Dirección:** pregunta por cumplimiento del plan, desviaciones de tiempo/alcance, retorno/impacto esperado, riesgos y qué se necesita para escalar a producción.

---

## 6. Bibliografía Oficial y Referencias Técnicas

- **Géron, A. (2023).** *Aprende machine learning con Scikit-Learn, Keras y TensorFlow: conceptos, herramientas y técnicas para conseguir sistemas inteligentes.* Anaya.
- **Project Management Institute (2025).** [*A Guide to the Project Management Body of Knowledge (PMBOK® Guide) — Eighth Edition*](https://www.pmi.org/standards/pmbok). Project Management Institute.
- **IBM Documentation.** [*Conceptos básicos de CRISP-DM*](https://www.ibm.com/docs/es/spss-modeler/saas?topic=dm-crisp-help-overview).
- **Scikit-Learn Documentation.** [*Pipeline*](https://scikit-learn.org/stable/modules/generated/sklearn.pipeline.Pipeline.html), [*ColumnTransformer*](https://scikit-learn.org/stable/modules/generated/sklearn.compose.ColumnTransformer.html) y [*cross_val_score*](https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.cross_val_score.html).
