# Configuración de Google Antigravity — Skills, MCP y Optimización de Tokens

Esta guía está diseñada específicamente para tu entorno actual (**Google Antigravity** + **GitHub CLI `gh` ya instalado y autenticado**) con el objetivo de producir entregables pulidos para **EP5 y EP6** consumiendo **la menor cantidad posible de tokens de tus modelos más potentes**.

---

## 1. Cómo Funciona la Personalización en Antigravity (y Por Qué Ahorra Tokens)

Según la [documentación oficial de Agent Skills de Google Antigravity](https://antigravity.google/docs/skills/), el agente utiliza un mecanismo de **carga progresiva (*progressive disclosure*)**:

1. **Descubrimiento:** En cada turno, Antigravity solo lee el **nombre y la descripción corta** de tus skills (muy pocos tokens).
2. **Activación:** Solo cuando la tarea actual coincide con una skill (o cuando la invocas manualmente con `/nombre-skill`), el agente carga el contenido completo de su `SKILL.md`.
3. **Ejecución:** Sigue los pasos exactos sin que tengas que repetir instrucciones largas en cada prompt.

> **Nota importante sobre migración:** En las versiones actuales de Antigravity, los *Legacy Workflows* fueron deprecados en favor de **Agent Skills** ubicadas en `.agents/skills/<nombre-skill>/SKILL.md` (ver [guía oficial de migración](https://antigravity.google/docs/migration/workflows-to-skills/)). Toda skill definida ahí se puede invocar directamente con `/<nombre-skill>`.

### Estructura mínima recomendada en tu repositorio

```text
Gestion/
├── .agents/
│   ├── rules/
│   │   └── proyecto-scy1102.md       # Reglas globales MUY cortas (<40 líneas)
│   └── skills/
│       ├── ds-repo-cleanup/SKILL.md  # Limpieza de notebooks y scripts
│       ├── streamlit-dashboard/SKILL.md # Creación del dashboard funcional
│       ├── github-pm-cli/SKILL.md    # Gestión de hitos/issues vía `gh` CLI
│       ├── ep5-informe-duoc/SKILL.md # Redacción informe 5-8 págs.
│       └── ep6-presentacion-duoc/SKILL.md # Presentación ejecutiva + defensa
└── docs/
    └── contexto/                     # Aquí guardas los 4 archivos .md generados
```

---

## 2. Regla Persistente del Workspace (`.agents/rules/proyecto-scy1102.md`)

Crea este archivo corto (se carga siempre, por eso debe ser breve y directo) para evitar que Antigravity cometa errores costosos en tokens:

```markdown
# Reglas del Proyecto SCY1102 — Caso 1 (Rendimiento en Matemáticas)

1. **Protección de tokens (CRÍTICO):**
   - NUNCA leas archivos CSV dentro de `data/raw/` (`train.csv` tiene 8M+ filas). Usa scripts Python cortos que solo lean `nrows=5` o estadísticas agregadas.
   - NUNCA leas archivos `.ipynb` completos en crudo (contienen imágenes base64 pesadas). Para inspeccionar un notebook, ejecuta un script Python que imprima solo código y texto sin el campo `image/png`.
2. **Herramienta de gestión:** Usa siempre GitHub CLI (`gh`) por terminal para crear/consultar milestones, issues y proyectos. No instales MCPs redundantes.
3. **Idioma y rigor:** Todos los entregables, gráficos, comentarios de código y reportes deben estar en español. Nunca inventes métricas; usa únicamente salidas reales ejecutadas del modelo (`Gradient Boosting`, RMSE Test 5.694, MAE 4.550, R² 0.673).
4. **Ética y fuga de datos:** Mantén excluidas `TestScore_Reading`, `TestScore_Science`, `GPA` (fuga de datos) y `Gender`, `Race` (atributos sensibles).
```

---

## 3. Las 5 Skills Necesarias (Listas para Copiar en `.agents/skills/`)

Mantener cada `SKILL.md` por debajo de 100 líneas y enfocada en una sola tarea sigue las [mejores prácticas oficiales de Antigravity](https://antigravity.google/docs/skills/) y minimiza el consumo de contexto.

### Skill 1: `.agents/skills/ds-repo-cleanup/SKILL.md`
```markdown
---
name: ds-repo-cleanup
description: Limpia, consolida y valida notebooks Jupyter, scripts Python, requirements.txt y README.md del proyecto de rendimiento académico en matemáticas. Usar al ordenar el repositorio o corregir issues del EDA y modelado.
---
# Limpieza y Consolidación Técnica del Repositorio

1. Inspecciona la estructura con `ls` y lee `docs/contexto/02_requisitos_y_rubricas_EP5_EP6.md` (sección 5).
2. No leas `.ipynb` en crudo con base64; usa Python (`json.load`) filtrando `outputs` de imagen.
3. Consolida los notebooks en dos archivos limpios dentro de `notebooks/`:
   - `01_EDA_matematicas.ipynb`: completa la sección 14 (Conclusiones) con los datos reales ya observados, sin placeholders.
   - `02_Modelado_y_automatizacion.ipynb`: basado en `modelo_matematicas.ipynb` (Gradient Boosting, 3 CSVs). Archiva `Modelado_matematicas_y_automatizacion.ipynb` en `archive/` o elimínalo previa confirmación.
4. Mueve el modelo y metadatos a `models/` y el script CLI a `src/automatizacion_matematicas.py` actualizando las rutas relativas, y verifica que `python src/automatizacion_matematicas.py --entrada ...` ejecute sin errores.
5. Crea `.gitignore` excluyendo `data/raw/*.csv`, `.venv/`, `__pycache__/`, `.ipynb_checkpoints/`.
6. Actualiza `README.md` eliminando marcas residuales (`[cite: 1]`), reflejando la estructura real, las 9 variables usadas, las métricas en Test y cómo ejecutar el script y dashboard.
```

### Skill 2: `.agents/skills/streamlit-dashboard/SKILL.md`
```markdown
---
name: streamlit-dashboard
description: Construye un dashboard interactivo en Streamlit para el Caso 1 (Rendimiento en Matemáticas) con vista ejecutiva, simulador de estudiante, vista técnica de métricas y predicción por lotes CSV. Usar al crear o mejorar el dashboard funcional para EP5 y EP6.
---
# Dashboard Interactivo de Acompañamiento Académico (Streamlit)

1. Crea `dashboard/app.py` y agrega `streamlit` y `plotly` a `requirements.txt`.
2. **No cargues `train.csv` (8M filas) en la app.** Usa `models/modelo_matematicas.joblib`, `models/metadatos.json`, las muestras de `automatizacion_modelo/entradas/` y un archivo ligero `models/resumen_metricas.json` con las métricas agregadas precalculadas.
3. Estructura el dashboard en **3 pestañas claras**:
   - **Vista Ejecutiva:** KPIs clave (promedio 75.0, R² 0.673, MAE 4.55 pts, umbral de apoyo 68.25), gráfico de factores más influyentes (`AttendanceRate`, `StudyHours`), y conclusiones accionables.
   - **Simulador Individual:** controles deslizantes para las 9 variables del estudiante que ejecutan `modelo.predict()` en vivo, muestran el puntaje estimado, rango probable (±5.70 pts) y alerta visual de "Requiere Apoyo Académico".
   - **Vista Técnica y Monitoreo (Batch):** comparación de modelos (Baseline vs. Regresión Lineal vs. Gradient Boosting), cargador de archivo CSV para predicción en lote con descarga de resultados, y chequeo automático de *drift* si el CSV incluye `TestScore_Math`.
4. Verifica que la app arranque sin errores (`streamlit run dashboard/app.py --server.headless true`) y toma capturas de pantalla para el informe EP5 y la presentación EP6.
```

### Skill 3: `.agents/skills/github-pm-cli/SKILL.md`
```markdown
---
name: github-pm-cli
description: Gestiona el seguimiento y control del proyecto SCY1102 usando GitHub CLI (gh) para crear milestones CRISP-DM, issues, etiquetas de desviaciones y reportes de avance. Usar para cumplir el 50% de gestión en EP5 y 30% en EP6.
---
# Monitoreo y Control de Proyecto con GitHub CLI (`gh`)

1. Verifica autenticación con `gh auth status` y el repositorio activo con `gh repo view`.
2. Crea etiquetas de control (`fase-crisp-dm`, `entregable-tecnico`, `gestion`, `desviacion`, `accion-correctiva`) usando `gh label create --force`.
3. Crea 4 Milestones alineados a CRISP-DM y EA3 vía `gh api repos/:owner/:repo/milestones`:
   - M1: Comprensión y EDA
   - M2: Preparación y Modelado
   - M3: Automatización y Dashboard
   - M4: Consolidación, Informe EP5 y Defensa EP6
4. Crea Issues concretos (planificados vs. ejecutados), cerrando los ya completados con comentarios de evidencia (commit/archivo) y documentando al menos **3 desviaciones reales con su acción correctiva**:
   - Desviación 1: Dataset de 8M+ filas excede memoria/tiempo local -> Acción: muestreo validado (500k) + verificación de curva de aprendizaje.
   - Desviación 2: Tres notebooks duplicados con modelos distintos -> Acción: consolidación técnica en 2 notebooks estándar y archivo del duplicado.
   - Desviación 3: Ausencia de variable de bienestar emocional y códigos 0/1 sin diccionario -> Acción: documentación explícita de limitaciones y recomendación de captura institucional.
5. Genera `docs/reporte_estado_avance.md` con tabla Planificado vs. Ejecutado, semáforo (Verde/Amarillo/Rojo), % de avance por hito, logros, desviaciones y enlaces reales a los issues.
```

### Skill 4: `.agents/skills/ep5-informe-duoc/SKILL.md`
```markdown
---
name: ep5-informe-duoc
description: Redacta y genera el informe escrito de la Evaluación Parcial N°5 (5 a 8 páginas) en formato DOCX y PDF cumpliendo 100% la rúbrica oficial de SCY1102 Duoc UC. Usar al elaborar el informe final del encargo.
---
# Generación del Informe Final EP5 (5–8 Páginas)

1. Lee `docs/contexto/02_requisitos_y_rubricas_EP5_EP6.md` (secciones 2 y 5) y `docs/reporte_estado_avance.md`.
2. Estructura el informe en `docs/entregables/Informe_EP5_Caso1_Matematicas.docx` (y exporta a PDF) respetando estrictamente **5 a 8 páginas**:
   - Portada breve + Contexto y Objetivos (Caso 1 Educación + CRISP-DM).
   - **1.1 Implementación Técnica:** arquitectura de datos (diagrama de flujo), decisiones técnicas (exclusión de fuga y variables sensibles), tabla comparativa de modelos (Test), hallazgos de importancia de variables, automatización CLI y capturas del Dashboard.
   - **1.2 Monitoreo y Control:** evidencia del tablero GitHub Projects/Issues (capturas + URLs reales), tabla de tareas Planificadas vs. Ejecutadas, Reporte de Estado de Avance con semáforo, y matriz de Desviaciones + Acciones Correctivas.
   - Conclusiones, limitaciones (bienestar emocional, correlación ≠ causalidad) y próximos pasos.
3. Incluye enlaces clicables al repositorio, notebooks, script de automatización y tablero de issues.
```

### Skill 5: `.agents/skills/ep6-presentacion-duoc/SKILL.md`
```markdown
---
name: ep6-presentacion-duoc
description: Genera la presentación ejecutiva en PowerPoint (.pptx) para 10 minutos y el guion de defensa con preguntas frecuentes para la Evaluación Parcial N°6 de SCY1102. Usar al crear las láminas y preparar la exposición.
---
# Presentación Ejecutiva y Guion de Defensa EP6 (10 Minutos)

1. Lee `docs/contexto/01_resumen_materia_SCY1102_EA3.md` (secciones 4 y 5) y `docs/contexto/02_requisitos_y_rubricas_EP5_EP6.md` (sección 3).
2. Genera `docs/entregables/Presentacion_EP6_Caso1_Matematicas.pptx` (10–12 láminas, diseño limpio y visual, sin bloques largos de texto):
   - Lámina 1: Portada (Caso 1, equipo, asignatura SCY1102).
   - Lámina 2: Contexto, problema de negocio y stakeholders.
   - Lámina 3: Objetivos, KPIs y trazabilidad CRISP-DM.
   - Lámina 4 (Técnica 1): Datos, calidad y decisiones clave (no *leakage*, ética).
   - Lámina 5 (Técnica 2): Comparación de modelos y métricas en Test (gráfico).
   - Lámina 6 (Técnica 3): Factores clave (`AttendanceRate` vs. categorías) y automatización/monitoreo de *drift*.
   - Lámina 7 (Demo): Dashboard de acompañamiento académico (capturas + flujo de uso).
   - Lámina 8 (Gestión 1): Planificación y evidencia en GitHub Issues/Projects.
   - Lámina 9 (Gestión 2): Reporte de estado de avance (semáforo y % por hito).
   - Lámina 10 (Gestión 3): Desviaciones detectadas y acciones correctivas.
   - Lámina 11: Valor generado, cumplimiento del plan, limitaciones y próximos pasos.
3. Crea `docs/entregables/Guion_Defensa_EP6.md` con tiempos por lámina (total 10 min) y 10 preguntas difíciles respondidas desde los 3 roles del jurado (Cliente, Gerente de Informática y Gerente General).
```

---

## 4. ¿Necesitas Servidores MCP? (Análisis Real Costo vs. Beneficio en Tokens)

Según la [documentación oficial de MCP de Google Antigravity](https://antigravity.google/docs/mcp/) y pruebas comparativas de consumo de tokens publicadas por [Google Cloud en Medium (*Agent Skills are Great but CLIs are Better*)](https://medium.com/google-cloud/tokens-to-deploy-experimenting-with-antigravity-and-cloud-run-to-prove-skills-are-great-but-clis-61584c191230), **cada servidor MCP activo inyecta decenas de definiciones de herramientas en JSON**, lo que consume presupuesto de tokens y puede distraer al modelo si no se configura con cuidado.

### Recomendación concreta para tu proyecto

| Servidor MCP / Herramienta | ¿Recomendado aquí? | Por qué (Impacto en Tokens y Calidad) |
| :--- | :---: | :--- |
| **GitHub CLI (`gh`)** *(ya lo tienes)* | **SÍ (Principal)** | Reemplaza por completo al GitHub MCP. Consume **cero tokens de esquema** en reposo; el agente solo ejecuta `gh issue create`, `gh project`, `gh pr` cuando lo necesita. |
| **GitHub MCP Server** | **NO** | Redundante si ya tienes `gh` CLI autenticado. Suele exponer 30+ herramientas que inflan innecesariamente el contexto. |
| **Jupyter / Filesystem MCP** | **NO** | Antigravity ya trae herramientas nativas de sistema de archivos y terminal (`execute_bash`/Python). Agregar un MCP de archivos duplica herramientas. |
| **Context7 MCP** *(opcional)* | **Solo si falla Streamlit/python-pptx** | Útil solo si quieres consultar documentación exacta de librerías (`streamlit`, `python-pptx`, `plotly`) sin alucinaciones de sintaxis. Si lo instalas, déjalo en modo **lazy loading** (por defecto en Antigravity) y desactívalo al terminar. |
| **Canva / Google Drive MCP** *(opcional)* | **Solo si diseñas en Canva/Slides** | Si vas a generar el `.pptx` y `.docx` localmente con Python (`python-pptx` y `python-docx`), **no necesitas ningún MCP externo**. |

> **Conclusión MCP:** Para este proyecto universitario, **0 MCPs obligatorios**. Tu combinación óptima en calidad y ahorro de tokens es: **Antigravity nativo + `gh` CLI + las 5 Skills en `.agents/skills/`**. Si algún día agregas un MCP, mantén el *lazy loading* activo y usa `disabledTools` para ocultar herramientas que no uses (ver [Antigravity MCP Docs](https://antigravity.google/docs/mcp/)).

---

## 5. Estrategia Práctica para Consumir Menos Tokens de los Mejores Modelos

1. **Una conversación nueva por entregable (no mezcles todo en un solo chat):**
   - Chat 1: Limpieza del repo y notebooks (`/ds-repo-cleanup`).
   - Chat 2: Dashboard en Streamlit (`/streamlit-dashboard`).
   - Chat 3: Gestión en GitHub con `gh` (`/github-pm-cli`).
   - Chat 4: Informe EP5 (`/ep5-informe-duoc`).
   - Chat 5: Presentación EP6 y guion (`/ep6-presentacion-duoc`).
   - *Por qué:* Al iniciar un chat limpio para cada fase, el modelo no arrastra 50.000 tokens de historial de fases anteriores. Si una sesión se alarga, usa `/compact`.
2. **Divide los modelos por tipo de tarea (enrutamiento inteligente):**
   - **Modelos rápidos / económicos:** crear carpetas, `.gitignore`, actualizar `README.md`, ejecutar comandos `gh issue create`, formatear tablas Markdown.
   - **Modelos Frontier (los mejores) / modo `/plan`:** diseñar el dashboard, corregir arquitectura de pipelines, redactar el informe ejecutivo de 5–8 páginas y estructurar el storytelling + defensa de EP6.
3. **Nunca cargues archivos pesados al contexto:**
   - Jamás adjuntes `train.csv` ni pidas al agente "lee `modelo_matematicas.ipynb` completo".
   - Los notebooks con gráficos embebidos pesan entre **800 KB y 1,2 MB** de texto base64; leer uno solo puede quemar decenas de miles de tokens inútiles. Usa la regla 1 de `.agents/rules/proyecto-scy1102.md` para inspeccionarlos con Python filtrando imágenes.
4. **Usa el modo *Planning* (`/plan`) antes de ejecutar código grande:**
   - Pide primero un plan corto (5–8 viñetas). Aprobar o corregir un plan de 200 tokens evita que el agente escriba 3.000 tokens de código equivocado que luego debas rehacer.
5. **Pasa archivos por ruta, no pegando texto en el chat:**
   - Guarda estos 4 `.md` en `docs/contexto/` y dile a Antigravity *"Lee solo la sección 5 de `docs/contexto/02_requisitos_y_rubricas_EP5_EP6.md`"*. Así evitas pegar megabloques repetidos en cada mensaje.
