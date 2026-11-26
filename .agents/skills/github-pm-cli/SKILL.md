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
