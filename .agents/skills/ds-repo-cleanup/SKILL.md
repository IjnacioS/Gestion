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
