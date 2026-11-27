# Guion de Defensa Ejecutiva y Banco de Preguntas — EP6 (SCY1102)

**Proyecto:** Caso 1 — Sistema de Alerta Temprana para el Rendimiento Académico en Matemáticas  
**Asignatura:** SCY1102 Gestión de Proyectos de Datos (Duoc UC)  
**Docente:** Michael Palomino B.  
**Duración Total:** 10 minutos exactos + ronda de preguntas  
**Equipo Expositor:** Ignacio Sobarzo · Diego Yañez · Felipe Espinoza  
**Presentación:** `docs/entregables/Presentacion_EP6_Caso1_Matematicas.pptx` (10 láminas limpias y directas)

---

## 1. Reparto Exacto para 10 Minutos (Lámina por Lámina)

| Lámina | Tiempo | Acumulado | Expositor | Qué decir (en simple y directo) |
| :---: | :---: | :---: | :--- | :--- |
| **1. Portada** | 0:25 | 0:25 | Ignacio Sobarzo | Saludar al profe Michael Palomino B. y al jurado. Presentar al equipo y el objetivo: anticipar qué estudiantes necesitan tutoría en matemáticas antes de que termine el semestre. |
| **2. Problema y Actores** | 0:55 | 1:20 | Ignacio Sobarzo | Explicar que hoy las malas notas se ven muy tarde. Mostrar que la solución ayuda a **Dirección, UTP, Docentes, Orientación y TI**, priorizando al 25% con mayor riesgo (puntaje bajo 68 puntos). |
| **3. Requerimientos (RF/RNF) y Flujo** | 1:00 | 2:20 | Ignacio Sobarzo | Mostrar que cumplimos todo el plan de EP3: **RF1–RF2** (solo 9 datos previos), **RF3** (meta ≥ 10%, logramos **43% menos error**), **RF4** (nota continua + 3 niveles de alerta), **RNF1** (datos anónimos Ley 19.628), **RNF2** (brecha de solo 0,03 pts) y **RNF5** (`.gitignore`). Recorrer brevemente el flujo CRISP-DM. |
| **4. Datos, Ética y Variables** | 1:00 | 3:20 | Diego Yañez | Explicar que la base tiene **10 millones de filas** (8M train, 1M val, 1M test) sin datos vacíos, y validamos una muestra de **500.000 estudiantes**. Destacar qué excluimos: notas finales (`GPA`, lectura, ciencias) por **fuga de datos**, y género/etnia por **ética**. Nombrar las 9 señales usadas. |
| **5. Resultados del Modelo** | 1:00 | 4:20 | Diego Yañez | Explicar el gráfico en fácil: **Gradient Boosting** ganó porque baja el error un **43%** frente al promedio simple, se equivoca en promedio solo **± 4,5 puntos**, acierta en **9 de cada 10 alumnos** dentro de ± 10 puntos y tiene una brecha de equidad de apenas **0,03 puntos**. |
| **6. Hallazgo y Automatización** | 1:00 | 5:20 | Diego Yañez | Contar el gran hallazgo: **la asistencia a clases es lo que más pesa** (si la quitamos, el error sube más de 6,6 pts), mientras el origen familiar casi no afecta. Explicar cómo el script automático procesa cursos completos en segundos y avisa a TI si el error sube más de **20%** (drift). |
| **7. Demo en Vivo (Dashboard)** | 1:30 | 6:50 | Diego Yañez | Mostrar el Dashboard en Streamlit en 3 pasos rápidos: (1) Resumen ejecutivo, (2) Simulador moviendo la asistencia para ver cómo cambia el semáforo de 3 niveles, y (3) Subir una nómina CSV de curso y descargar la lista priorizada. |
| **8. Seguimiento en GitHub** | 0:55 | 7:45 | Felipe Espinoza | Mostrar la tabla de las 4 etapas (Milestones M1 a M4) con todos los entregables listos y las capturas reales del tablero y los issues en GitHub. |
| **9. Avance y 3 Desviaciones** | 1:15 | 9:00 | Felipe Espinoza | Mostrar el semáforo global en **VERDE** (100% completado) y contar brevemente las 3 desviaciones reales que resolvimos: **#12** (muestra 500k de 8M por memoria), **#13** (unificar 3 notebooks duplicados en 2 limpios) y **#14** (falta de bienestar emocional, riesgo que ya habíamos previsto en EP3 y transparentamos en el sistema). |
| **10. Valor y Próximos Pasos** | 1:00 | **10:00** | Ignacio Sobarzo | Cerrar destacando el impacto: costo **$0 en licencias**, uso 100% formativo (nunca sancionador, correlación ≠ causalidad) y los 3 pasos para el colegio: conectar asistencia mensual, sumar encuesta breve de bienestar y hacer el piloto semestral con UTP. |

---

## 2. Respuestas Rápidas a las 10 Preguntas Más Probables del Jurado

### A. Preguntas del Cliente (UTP, Dirección y Orientación)

1. **¿Por qué entregaron una nota de 0 a 100 con 3 alertas en vez de solo clasificar en "Bajo / Medio / Alto" (RF4)?**
   > Porque el dataset original traía notas numéricas, no etiquetas oficiales. Inventar categorías para entrenar distorsiona los datos. Es mejor predecir la nota exacta (0–100) y luego traducirla en **3 niveles de acción claros para UTP**: *Incorporar a tutoría* (< 68 pts), *Hacer seguimiento* (zona límite) y *Sin apoyo por ahora*.

2. **El caso menciona bienestar emocional, pero el modelo no lo tiene. ¿Por qué?**
   > Porque los archivos CSV entregados no traían esa columna. Ya lo habíamos anticipado como riesgo en la planificación (EP3) y lo registramos en GitHub (**Issue #14**). En vez de inventar datos, dejamos un aviso claro en el Dashboard para que Orientación sepa ese límite y propusimos agregar una encuesta breve el próximo semestre.

3. **¿Cómo cuidan la privacidad y que el modelo no discrimine?**
   > Cumplimos la **Ley 19.628 (RNF1)** usando solo datos anónimos sin RUT ni nombres, y bloqueamos los CSV con `.gitignore` (**RNF5**). Para equidad (**RNF2**), eliminamos género y etnia del modelo y comprobamos que la diferencia por nivel educativo de los padres es de apenas **0,03 puntos** (el límite permitido era 10 puntos).

4. **Si la asistencia es lo que más pesa, ¿basta con obligar a los niños a ir a clases para que suban las notas?**
   > No, porque **correlación no es causalidad**. La falta de asistencia es una excelente señal de alerta temprana, pero detrás suele haber problemas de salud, familia o desmotivación. El sistema sirve para que UTP y Orientación apoyen a tiempo, nunca para castigar.

---

### B. Preguntas del Gerente de Informática (TI)

5. **¿Por qué sacaron las notas de lectura, ciencias y el promedio (`GPA`) si ayudaban a predecir mejor?**
   > Por **fuga de datos (*data leakage*)**. Esas notas se conocen recién al terminar el semestre, al mismo tiempo que matemáticas. Si las dejábamos, el modelo haría trampa en el papel pero sería inútil a mitad de año.

6. **¿Por qué ganó Gradient Boosting y no Regresión Lineal?**
   > Porque **Gradient Boosting** logró el menor error en los 500.000 casos de prueba: bajó el error un **43%** frente al promedio simple (superando la meta de 10% en RF3), con un error habitual de **± 4,5 puntos** y sin sobreajuste (solo 0,4% de diferencia entre entrenamiento y validación).

7. **¿Por qué usaron 500.000 filas si la base tenía 8 millones de entrenamiento? ¿Y cómo detectan si el modelo se degrada?**
   > Con 8 millones de filas el computador se quedaba sin memoria (**Issue #12**). Probamos la curva de aprendizaje y vimos que desde 200.000 filas el error ya no mejora; con 500.000 logramos exactamente la misma precisión en un 90% menos de tiempo. Además, el script y el Dashboard revisan automáticamente si el error sube más de **20%** al llegar las notas reales (*drift*) y avisan a TI para reentrenar.

---

### C. Preguntas de Gestión y Dirección (Gerente General / Sponsor)

8. **¿Cómo controlaron el avance del proyecto durante la ejecución?**
   > Organizamos el repositorio en GitHub con **4 Milestones** alineados a CRISP-DM (Comprensión/EDA, Modelado, Automatización/Dashboard y Cierre) y **14 Issues** trazables, logrando cerrar el 100% de las entregas planificadas con semáforo en **VERDE**.

9. **Tuvieron 3 desviaciones en GitHub. ¿Eso significa que el proyecto se desordenó?**
   > Al contrario: demuestra control real. Cada problema se registró, se corrigió y se cerró sin atrasar las fechas: **#12** (muestra 500k validada), **#13** (ordenar 3 notebooks duplicados en 2 oficiales) y **#14** (transparentar la falta de bienestar emocional).

10. **¿Cuánto cuesta implementar esto en el colegio el próximo semestre?**
    > **Cero pesos en licencias**, porque corre en Python y Streamlit (software libre) sobre los servidores que el colegio ya tiene. Solo hace falta exportar la asistencia mensual desde el libro de clases y coordinar los cupos de tutoría con UTP.
