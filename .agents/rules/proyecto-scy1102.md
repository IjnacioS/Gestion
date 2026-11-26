# Reglas del Proyecto SCY1102 — Caso 1 (Rendimiento en Matemáticas)

1. **Protección de tokens (CRÍTICO):**
   - NUNCA leas archivos CSV dentro de `data/raw/` (`train.csv` tiene 8M+ filas). Usa scripts Python cortos que solo lean `nrows=5` o estadísticas agregadas.
   - NUNCA leas archivos `.ipynb` completos en crudo (contienen imágenes base64 pesadas). Para inspeccionar un notebook, ejecuta un script Python que imprima solo código y texto sin el campo `image/png`.
2. **Herramienta de gestión:** Usa siempre GitHub CLI (`gh`) por terminal para crear/consultar milestones, issues y proyectos. No instales MCPs redundantes.
3. **Idioma y rigor:** Todos los entregables, gráficos, comentarios de código y reportes deben estar en español. Nunca inventes métricas; usa únicamente salidas reales ejecutadas del modelo (`Gradient Boosting`, RMSE Test 5.694, MAE 4.550, R² 0.673).
4. **Ética y fuga de datos:** Mantén excluidas `TestScore_Reading`, `TestScore_Science`, `GPA` (fuga de datos) y `Gender`, `Race` (atributos sensibles).