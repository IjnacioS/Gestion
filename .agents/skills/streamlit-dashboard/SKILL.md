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
