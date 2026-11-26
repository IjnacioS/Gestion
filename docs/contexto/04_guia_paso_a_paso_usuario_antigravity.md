# Guía Paso a Paso para Ti — Cómo Usar Estos `.md` con Antigravity

Esta es tu hoja de ruta personal. Sigue estas **6 fases en orden exacto** para que Google Antigravity transforme tu repositorio actual en un proyecto completo, ordenado y listo para sacar nota máxima en **EP5** y **EP6**, gastando el mínimo de tokens.

---

## Fase 0: Preparación en tu PC (5 minutos, sin gastar tokens)

Antes de abrir un chat en Antigravity, deja tu carpeta local ordenada así:

1. Abre tu repositorio clonado (`Gestion`) en tu computador.
2. Verifica que tus tres archivos CSV descargados de Kaggle (`train.csv`, `validation.csv`, `test.csv`) estén en `data/raw/` (si no existe la carpeta, créala).
3. Crea la carpeta `docs/contexto/` y copia dentro **estos 4 archivos `.md`**:
   - `docs/contexto/01_resumen_materia_SCY1102_EA3.md`
   - `docs/contexto/02_requisitos_y_rubricas_EP5_EP6.md`
   - `docs/contexto/03_antigravity_skills_mcp_y_tokens.md`
   - `docs/contexto/04_guia_paso_a_paso_usuario_antigravity.md`
4. Abre la terminal en la raíz del proyecto y confirma que GitHub CLI está listo:
   ```bash
   gh auth status
   git status
   ```
5. Crea las carpetas `.agents/rules/` y `.agents/skills/` y copia dentro los archivos definidos en `03_antigravity_skills_mcp_y_tokens.md` (o pídele a Antigravity en un chat rápido con un modelo económico que los cree por ti con el prompt de abajo).

**Prompt opcional de setup (usar modelo rápido/económico):**
> Lee `docs/contexto/03_antigravity_skills_mcp_y_tokens.md` secciones 2 y 3. Crea automáticamente el archivo `.agents/rules/proyecto-scy1102.md` y las 5 carpetas con sus `SKILL.md` dentro de `.agents/skills/`. No modifiques ningún otro archivo todavía.

---

## Fase 1: Limpiar el Repositorio y Cerrar el EDA/Modelado

**Abre una conversación NUEVA en Antigravity** (modelo estándar o rápido) y pega:

> Usa la skill `/ds-repo-cleanup`. Lee la sección 5 de `docs/contexto/02_requisitos_y_rubricas_EP5_EP6.md` y reorganiza el repositorio:
> 1. Crea `.gitignore` para no subir `data/raw/*.csv` ni archivos temporales.
> 2. Consolida los notebooks en `notebooks/01_EDA_matematicas.ipynb` (completando las conclusiones reales de la celda 34) y `notebooks/02_Modelado_y_automatizacion.ipynb` (basado en `modelo_matematicas.ipynb`), moviendo el duplicado `Modelado_matematicas_y_automatizacion.ipynb` a `archive/`.
> 3. Mueve `automatizacion_matematicas.py` a `src/` y el modelo `.joblib` + `metadatos.json` a `models/`, ajustando las rutas y probando el script con `entradas/nuevos_estudiantes.csv`.
> 4. Guarda un archivo ligero `models/resumen_metricas.json` con las métricas de validación/test e importancia de variables para que lo use el dashboard.
> 5. Actualiza `README.md` y haz un commit limpio con `git`.

**Qué debes verificar tú al terminar:**
- Que `python src/automatizacion_matematicas.py --entrada ...` corre y genera el CSV de predicciones en `salidas/`.
- Que `git status` **no** intenta subir `data/raw/train.csv` (pesa cientos de MB).

---

## Fase 2: Construir el Dashboard Interactivo (Entregable Funcional Estrella)

**Abre una conversación NUEVA en Antigravity** (usa tu mejor modelo en modo `/plan` primero) y pega:

> Usa la skill `/streamlit-dashboard`. Construye `dashboard/app.py` leyendo `models/modelo_matematicas.joblib`, `models/metadatos.json` y `models/resumen_metricas.json` (sin cargar `train.csv`).
> Incluye las 3 pestañas (Vista Ejecutiva, Simulador Individual de Estudiante con alerta de apoyo, y Vista Técnica + carga de CSV en lote con monitoreo de drift).
> Antes de escribir código, muéstrame un plan breve de 6 líneas. Al terminar, pruébalo localmente y dime el comando para abrirlo en mi navegador.

**Qué debes hacer tú al terminar:**
1. Ejecuta `streamlit run dashboard/app.py` en tu terminal.
2. Prueba el simulador cambiando la asistencia (`AttendanceRate`) y las horas de estudio (`StudyHours`) para ver cómo cambia el puntaje predicho y la alerta.
3. Saca **3 capturas de pantalla limpias** (una por pestaña) y guárdalas en `docs/evidencias/` (`dashboard_ejecutivo.png`, `dashboard_simulador.png`, `dashboard_tecnico.png`). Las usará el informe EP5 y la presentación EP6.

---

## Fase 3: Montar el Monitoreo y Control en GitHub (50% de EP5 / 30% de EP6)

**Abre una conversación NUEVA en Antigravity** (modelo rápido, aquí ahorras muchos tokens) y pega:

> Usa la skill `/github-pm-cli`. Usando `gh` CLI en mi repositorio actual:
> 1. Crea las etiquetas y los 4 Milestones CRISP-DM definidos en la skill.
> 2. Crea entre 10 y 12 Issues reales que cubran todo el ciclo (EDA, limpieza, modelado, automatización, dashboard, informe EP5, presentación EP6), cerrando los que ya completamos con referencia a los archivos creados y dejando abiertos solo los pendientes de EP5/EP6.
> 3. Crea 3 Issues etiquetados como `desviacion` + `accion-correctiva` con las desviaciones reales del proyecto (tamaño de 8M de filas, consolidación de 3 notebooks duplicados y ausencia de variable de bienestar emocional).
> 4. Genera `docs/reporte_estado_avance.md` con estado semáforo, tabla Planificado vs. Ejecutado, % de avance por hito y enlaces reales a los issues de GitHub.

**Qué debes hacer tú al terminar:**
1. Entra a tu repositorio en `github.com` -> pestaña **Projects** -> crea un tablero Kanban simple (*Board*) y vincula los issues creados (o revisa la pestaña **Issues / Milestones**).
2. Toma **2 capturas de pantalla** (vista de Milestones con % de avance + tablero Kanban/Issues) y guárdalas en `docs/evidencias/` (`github_milestones.png`, `github_kanban.png`).

---

## Fase 4: Generar el Informe Escrito EP5 (5 a 8 Páginas)

**Abre una conversación NUEVA en Antigravity** (usa tu mejor modelo) y pega:

> Usa la skill `/ep5-informe-duoc`. Lee:
> - `docs/contexto/02_requisitos_y_rubricas_EP5_EP6.md` (sección 2)
> - `docs/reporte_estado_avance.md`
> - `models/resumen_metricas.json`
> Redacta y genera con Python (`python-docx`) el informe `docs/entregables/Informe_EP5_Caso1_Matematicas.docx` incrustando las imágenes reales que están en `docs/evidencias/` y los enlaces reales a mi repositorio y tablero de GitHub.
> Requisitos estrictos: extensión exacta entre **5 y 8 páginas**, incluir apartados **1.1 Implementación técnica** y **1.2 Monitoreo y control**, y dejar `[Nombre Integrante]` solo donde falten los nombres de mi equipo.

**Qué debes revisar tú antes de entregar EP5:**
- Abre el `.docx` en Word o Google Docs, reemplaza los nombres de tu equipo y fecha de entrega.
- Verifica visualmente que tenga **entre 5 y 8 páginas exactas** y que todos los enlaces a GitHub abran correctamente (recuerda dejar el repositorio **público** o agregar al docente como colaborador).
- Exporta a PDF si la plataforma de Duoc UC pide PDF.

---

## Fase 5: Generar la Presentación Ejecutiva EP6 (10 Minutos) y Guion de Defensa

**Abre una conversación NUEVA en Antigravity** (usa tu mejor modelo) y pega:

> Usa la skill `/ep6-presentacion-duoc`. Lee:
> - `docs/contexto/01_resumen_materia_SCY1102_EA3.md` (secciones 4 y 5)
> - `docs/contexto/02_requisitos_y_rubricas_EP5_EP6.md` (sección 3)
> - `docs/reporte_estado_avance.md` y `models/resumen_metricas.json`
> Genera con `python-pptx` la presentación ejecutiva `docs/entregables/Presentacion_EP6_Caso1_Matematicas.pptx` (11 láminas, estilo limpio y moderno, incrustando las capturas de `docs/evidencias/`).
> Además, genera `docs/entregables/Guion_Defensa_EP6.md` con el reparto exacto para 10 minutos y las respuestas a 10 preguntas difíciles del jurado (Cliente, Gerente de Informática y Gerente General).

**Qué debes hacer tú al terminar:**
- Abre el `.pptx` en PowerPoint o impórtalo a Canva si prefieres pulir detalles visuales.
- Practica la exposición con cronómetro (meta: **9 minutos**, dejando 1 minuto de margen).
- Estudia `Guion_Defensa_EP6.md` — recuerda que **el 30% de EP6 es individual** respondiendo preguntas con dominio técnico y de gestión.

---

## Checklist Final Pre-Entrega (Cruce Directo con Rúbricas EP5 y EP6)

Marca cada punto antes de subir los archivos:

- [ ] **Repositorio limpio y accesible:** `README.md` actualizado, `.gitignore` activo, sin archivos duplicados ni textos `[completar]`.
- [ ] **Evidencia técnica completa (50% EP5):** Notebooks limpios (`01_EDA`, `02_Modelado`), script CLI funcionando (`src/automatizacion_matematicas.py`) y Dashboard Streamlit operativo (`dashboard/app.py`).
- [ ] **Evidencia de gestión sistemática (50% EP5 / 30% EP6):** Milestones y Issues en GitHub, tablero Kanban con capturas, tabla Planificado vs. Ejecutado, reporte de estado de avance con semáforo y al menos 3 desviaciones + acciones correctivas.
- [ ] **Informe EP5 formal:** Entre 5 y 8 páginas exactas, apartados 1.1 y 1.2 completos, capturas legibles y enlaces verificados.
- [ ] **Presentación EP6 (40% + 30% + 30%):** 10–12 láminas claras (sin muros de texto), balance técnico/ejecutivo, defensa en 10 minutos ensayada y respuestas dominadas sobre:
  - Por qué regresión continua y no clasificación arbitraria.
  - Por qué se excluyeron `GPA`, `Reading`, `Science` (fuga de datos) y `Gender`, `Race` (ética).
  - Por qué ganó `Gradient Boosting` (RMSE 5,694 vs. 9,952 baseline, mejora 42,7%, sin sobreajuste).
  - Por qué `AttendanceRate` explica casi todo y por qué la falta de bienestar emocional es una limitación documentada.
  - Cómo se detecta el *drift* en la automatización (umbral +20% RMSE) y cómo se controlaron las desviaciones del proyecto.
