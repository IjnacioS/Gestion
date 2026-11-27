# Guion Detallado de Defensa Ejecutiva (Libreto Completo) — EP6 (SCY1102)

**Proyecto:** Caso 1 — Sistema de Alerta Temprana para el Rendimiento Académico en Matemáticas  
**Asignatura:** SCY1102 Gestión de Proyectos de Datos (Duoc UC)  
**Docente:** Michael Palomino B.  
**Equipo Expositor:** Ignacio Sobarzo · Diego Yañez · Felipe Espinoza  
**Duración Total:** 10 minutos exactos (calibrado a ~130 palabras por minuto)  
**Presentación:** `docs/entregables/Presentacion_EP6_Caso1_Matematicas.pptx` (10 láminas)

---

## 1. Resumen de Tiempos y Reparto

| Lámina | Tiempo | Acumulado | Expositor | Foco Principal |
| :---: | :---: | :---: | :--- | :--- |
| **1. Portada** | 0:25 | 0:25 | Ignacio Sobarzo | Saludo, presentación del equipo y propósito |
| **2. Problema y Actores** | 0:55 | 1:20 | Ignacio Sobarzo | Problema del colegio, 5 actores y corte 68 pts |
| **3. Requerimientos y CRISP-DM** | 1:00 | 2:20 | Ignacio Sobarzo | Cumplimiento RF/RNF y arquitectura general |
| **4. Datos, Ética y Variables** | 1:00 | 3:20 | Diego Yañez | 10M filas vs 500k, fuga de datos, ética y 9 variables |
| **5. Resultados del Modelo** | 1:00 | 4:20 | Diego Yañez | Gradient Boosting, 43% menos error, ±4,5 pts, equidad |
| **6. Hallazgo y Automatización** | 1:00 | 5:20 | Diego Yañez | Peso de la asistencia, script por lotes y alerta drift |
| **7. Demo en Vivo (Dashboard)** | 1:30 | 6:50 | Diego Yañez | Recorrido real por Streamlit (Resumen, Simulador, CSV) |
| **8. Seguimiento en GitHub** | 0:55 | 7:45 | Felipe Espinoza | 4 Milestones, entregables construidos y tablero real |
| **9. Avance y 3 Desviaciones** | 1:15 | 9:00 | Felipe Espinoza | Semáforo VERDE y las 3 desviaciones resueltas (#12, #13, #14) |
| **10. Valor y Próximos Pasos** | 1:00 | **10:00** | Ignacio Sobarzo | Beneficio, costo $0, ética y cierre ejecutivo |

---

## 2. Libreto Completo Diapositiva por Diapositiva

### Lámina 1: Portada (0:25) — Ignacio Sobarzo
* **Qué hacer en pantalla:** Mantener la portada visible, mirar al docente y al jurado con postura relajada y segura.
* **Qué decir:**
  > "Buenas tardes profesor Michael Palomino y estimados integrantes del jurado. Somos **Ignacio Sobarzo, Diego Yañez y Felipe Espinoza**, y hoy les presentamos nuestro proyecto final del **Caso 1 de Educación**: un **Sistema de Alerta Temprana para el Rendimiento Académico en Matemáticas**. Nuestro objetivo es simple y concreto: aprovechar los datos que un colegio ya registra mes a mes para detectar a tiempo qué estudiantes necesitan apoyo antes de que termine el semestre."

---

### Lámina 2: Problema Educativo y Actores Involucrados (0:55) — Ignacio Sobarzo
* **Qué señalar en pantalla:** Primero la tarjeta roja (Problema), luego la tarjeta azul (Actores) y finalmente los 4 KPIs de abajo (en especial **< 68 pts**).
* **Qué decir:**
  > "Partamos por el problema real del colegio. Hoy, los bajos resultados en matemáticas suelen detectarse recién al cierre del semestre, cuando ya es tarde para nivelar al estudiante.
  >
  > Para cambiar ese enfoque reactivo por uno preventivo, diseñamos una solución pensada para los cinco actores clave definidos en nuestro plan de EP3: **Dirección**, que aprueba las políticas de apoyo; **UTP**, que asigna los cupos de tutoría; los **docentes de matemáticas y Orientación**, que acompañan al alumno y su familia; y el área de **TI**, encargada de operar el sistema mensualmente.
  >
  > Como ven en las cifras de abajo, trabajamos sobre una base de **10 millones de registros de estudiantes** sin datos vacíos, donde el promedio es **75 puntos de 100**. Definimos un corte operativo en **68 puntos**, que corresponde exactamente al **25% de alumnos con mayor prioridad**, y los ordenamos en un **semáforo de 3 niveles** para facilitar la toma de decisiones."

---

### Lámina 3: Requerimientos (RF / RNF) y Arquitectura CRISP-DM (1:00) — Ignacio Sobarzo
* **Qué señalar en pantalla:** Tarjeta izquierda (RF), tarjeta derecha (RNF) y luego recorrer con la mano el diagrama de izquierda a derecha (de Datos a Script/Dashboard).
* **Qué decir:**
  > "En esta lámina mostramos cómo cumplimos uno a uno los requerimientos comprometidos en la planificación.
  >
  > En los **Requerimientos Funcionales**: para **RF1 y RF2**, usamos solo 9 señales que el colegio conoce antes de la prueba final, sin fuga de información. En **RF3**, nuestra meta era mejorar al menos un 10% frente al promedio simple, y logramos un **43% menos error**, cuadruplicando el objetivo. Y en **RF4**, hicimos un ajuste justificado: en vez de inventar categorías arbitrarias, el modelo predice la nota continua de 0 a 100 y el simulador la traduce en 3 niveles claros de alerta.
  >
  > En los **Requerimientos No Funcionales**, cumplimos la **Ley 19.628 (RNF1)** con datos 100% anónimos; garantizamos **equidad (RNF2)** eliminando género y etnia, logrando una brecha real de solo **0,03 puntos** frente al límite de 10 puntos; y protegimos los datos crudos con `.gitignore` (**RNF5**).
  >
  > Abajo ven toda la arquitectura bajo **CRISP-DM**, desde los archivos CSV protegidos hasta el script automático y el Dashboard web. Ahora le doy el pase a **Diego**, quien explicará el detalle técnico."

---

### Lámina 4: Datos, Prevención de Fuga y Ética (1:00) — Diego Yañez
* **Qué señalar en pantalla:** Recorrer las 3 columnas de izquierda a derecha (Base de datos → Qué excluimos → Las 9 variables).
* **Qué decir:**
  > "Gracias Ignacio. Para construir el modelo auditamos la base completa de **10 millones de filas** —dividida en 8 millones de entrenamiento, 1 millón de validación y 1 millón de prueba— y verificamos que tiene **cero nulos y cero duplicados**. Como 8 millones de filas saturaban la memoria local, validamos mediante curva de aprendizaje una muestra representativa de **500.000 estudiantes** que mantiene exactamente la misma precisión.
  >
  > Aquí tomamos dos decisiones técnicas muy importantes que ven en la columna central. Primero, excluimos el promedio general (`GPA`), lectura y ciencias para evitar **fuga de datos**, ya que esas notas se conocen al final del semestre y harían trampa al predecir. Segundo, excluimos **género y etnia** por ética y equidad, y no usamos RUT ni nombres.
  >
  > Así nos quedamos con las **9 señales limpias** de la derecha: asistencia, horas de estudio, actividades extra, apoyo familiar, escolaridad de los padres, internet en casa, curso, edad y nivel socioeconómico; todos datos que el colegio ya tiene desde el primer mes."

---

### Lámina 5: Desempeño del Modelo Gradient Boosting (1:00) — Diego Yañez
* **Qué señalar en pantalla:** El gráfico izquierdo (comparación de RMSE), luego el gráfico derecho (importancia de variables) y finalmente las 4 tarjetas KPI de abajo.
* **Qué decir:**
  > "Con esas 9 variables comparamos tres alternativas: una línea base que siempre predice el promedio de 75 puntos, una Regresión Lineal y un modelo **Gradient Boosting**.
  >
  > Como se aprecia en el gráfico izquierdo, **Gradient Boosting** fue el claro ganador, logrando el menor error en los 500.000 casos de prueba y sin ningún sobreajuste, con apenas un 0,4% de diferencia entre entrenamiento y validación.
  >
  > Llevado a números fáciles de entender para el colegio, en las tarjetas de abajo vemos cuatro logros clave: el modelo se equivoca en promedio solo **± 4,5 puntos** en una escala de 0 a 100; reduce el error en un **43%** frente a la línea base; acierta en **9 de cada 10 estudiantes** dentro de un margen de ± 10 puntos; y mantiene una **brecha de equidad de apenas 0,03 puntos** según escolaridad de los padres."

---

### Lámina 6: Hallazgos Clave y Operación Automática (1:00) — Diego Yañez
* **Qué señalar en pantalla:** Tarjeta izquierda (Asistencia) y luego tarjeta derecha (Script por lotes y alerta de 20%).
* **Qué decir:**
  > "Más allá de la precisión, el modelo nos dejó un hallazgo clave para UTP y Orientación: **la asistencia a clases es, por lejos, la señal que más anticipa el rendimiento**. Si le quitamos la asistencia al modelo, el error se dispara en más de 6,6 puntos. En cambio, variables como la escolaridad de los padres o el acceso a internet casi no alteran el resultado. Eso le permite al colegio actuar desde el primer mes apenas detecte inasistencias reiteradas.
  >
  > Para que esto no quede en un cuaderno de código, construimos un **script automático por lotes** pensado para TI. Procesa planillas CSV de cursos completos en segundos, entrega la nómina priorizada con los **3 niveles de alerta** y deja todo registrado en un log auditable. Además, incluye **monitoreo automático de drift**: cuando al final del semestre llegan las notas reales, si el error sube más de un **20%**, el sistema avisa automáticamente a TI para reentrenar el modelo."

---

### Lámina 7: Demo en Vivo — Dashboard Interactivo en Streamlit (1:30) — Diego Yañez
* **Qué hacer en pantalla:** Mostrar brevemente la captura de la lámina y luego **cambiar a la ventana del navegador con Streamlit abierto (`localhost:8501`)** para hacer la demo real en 3 pasos rápidos (~1 minuto en vivo).
  * *Tip previo:* Tener abierto `streamlit run dashboard/app.py` antes de empezar a exponer y tener a mano el archivo `data/demo_curso_ejemplo.csv` para subirlo en 2 segundos.
* **Qué decir:**
  > "Y para que Dirección, UTP y los profesores puedan usar esto sin tocar una sola línea de código, construimos este **Dashboard interactivo en Streamlit**. Les muestro en vivo sus tres funciones principales:
  >
  > 1. *(Mostrar pestaña Resumen Ejecutivo)* Aquí arriba Dirección y UTP ven de inmediato los indicadores de precisión del modelo y el corte de tutoría en **68 puntos**.
  > 2. *(Cambiar a pestaña Simulador de Estudiante)* En el simulador podemos evaluar un caso individual. Fíjense que si este alumno tiene buena asistencia queda en **Verde (Sin apoyo por ahora)**; pero si bajamos su asistencia hacia 65%–70%, el puntaje estimado cae bajo 68 puntos y se activa automáticamente la alerta roja de **Incorporar a tutoría**. Abajo además dejamos explícito el cuadro ético de *'Lo que esta herramienta no hace'*, recordando que no reemplaza el criterio docente ni mide bienestar emocional.
  > 3. *(Cambiar a pestaña Nómina CSV)* Finalmente, UTP o TI pueden arrastrar aquí la planilla CSV de un curso completo; el sistema procesa a todos los estudiantes en segundos, ordena de mayor a menor riesgo y permite descargar el archivo listo para asignar los cupos de tutoría.
  >
  > *(Volver a la presentación)* Con la solución técnica demostrada, le doy el pase a **Felipe** para revisar cómo gestionamos el proyecto."

---

### Lámina 8: Planificación vs. Ejecución en GitHub (0:55) — Felipe Espinoza
* **Qué señalar en pantalla:** La tabla de los 4 Milestones arriba y las dos capturas reales de GitHub abajo (Milestones a la izquierda, Issues a la derecha).
* **Qué decir:**
  > "Muchas gracias Diego. En paralelo al desarrollo técnico, gestionamos todo el proyecto de forma sistemática en **GitHub**, alineando las etapas de CRISP-DM con cuatro **Milestones** y **14 Issues** trazables.
  >
  > Como pueden ver en la tabla superior: el **Milestone 1** cerró el alcance y el análisis exploratorio con 4 de 4 issues completados; el **Milestone 2** cerró el modelado y la exportación de Gradient Boosting también al 100%; el **Milestone 3** cerró el script automático y el Dashboard en Streamlit; y el **Milestone 4** consolida el informe final y esta presentación que entregamos hoy.
  >
  > Abajo incluimos las capturas reales de nuestro repositorio público, donde se verifica cada hito, sus etiquetas y el cierre documentado de cada tarea del equipo."

---

### Lámina 9: Reporte de Avance (Semáforo) y 3 Desviaciones Resueltas (1:15) — Felipe Espinoza
* **Qué señalar en pantalla:** El semáforo **VERDE** arriba a la derecha, el gráfico de barras y luego cada una de las 3 tarjetas de desviaciones abajo (#12, #13, #14).
* **Qué decir:**
  > "Al cierre del proyecto nuestro **semáforo global está en VERDE**, con el 100% de los entregables construidos y sin atrasos en el cronograma.
  >
  > Pero gestionar bien no significa que no existan problemas, sino detectarlos y resolverlos a tiempo. Documentamos y cerramos **tres desviaciones reales** en GitHub:
  >
  > * **Primera, Issue #12:** El archivo original de 8 millones de filas saturaba la memoria de los computadores locales. Como acción correctiva validamos la muestra representativa de 500.000 estudiantes, reduciendo más de un 90% el tiempo de entrenamiento sin perder precisión.
  > * **Segunda, Issue #13:** El trabajo en paralelo generó 3 notebooks duplicados con versiones distintas. Los consolidamos en 2 cuadernos oficiales limpios (`01_EDA` y `02_Modelado`) y respaldamos los antiguos en una carpeta de archivo.
  > * **Tercera, Issue #14:** Confirmamos en los datos que no existía ninguna variable de bienestar emocional, un riesgo que ya habíamos anticipado en EP3. En lugar de inventar datos, transparentamos esa limitación en el Dashboard y en el Informe, y propusimos una encuesta breve para el próximo semestre.
  >
  > Ahora **Ignacio** cierra con el valor para el colegio y los próximos pasos."

---

### Lámina 10: Valor para el Colegio y Próximos Pasos (1:00) — Ignacio Sobarzo
* **Qué señalar en pantalla:** Tarjeta izquierda (Valor y Uso Ético) y tarjeta derecha (3 Próximos Pasos).
* **Qué decir:**
  > "Para cerrar, queremos resumir el valor concreto que entregamos al establecimiento.
  >
  > Hoy el colegio cuenta con una herramienta que permite priorizar al **25% de estudiantes con mayor riesgo** acertando en **9 de cada 10 casos**, con **costo cero en licencias** al estar construida sobre Python y Streamlit, y diseñada bajo un enfoque **100% formativo y ético**: el sistema apoya, nunca sanciona ni etiqueta, y siempre recuerda que **asociación no es causalidad**; detrás de una baja asistencia hay un estudiante que Orientación debe escuchar.
  >
  > Para llevar esto a producción el próximo semestre proponemos solo **tres pasos concretos**: primero, exportar mensualmente la asistencia desde el libro de clases digital al script automático; segundo, sumar junto a Orientación una encuesta breve de bienestar emocional; y tercero, ejecutar un piloto semestral con UTP para medir cuántos alumnos en alerta logran superar los 68 puntos tras recibir tutoría.
  >
  > Muchas gracias por su atención. Quedamos atentos a sus preguntas."

---

## 3. Banco de 10 Preguntas Difíciles del Jurado y Respuestas Modelo

### A. Perspectiva del Cliente (UTP, Dirección y Orientación)

1. **¿Por qué entregaron una nota de 0 a 100 con 3 alertas en vez de solo clasificar en "Bajo / Medio / Alto" (RF4)?**
   > **Respuesta:** Porque el dataset original traía puntajes numéricos continuos, no categorías oficiales. Inventar cortes arbitrarios para entrenar un clasificador habría distorsionado los datos y perdido información. Es mucho más preciso predecir la nota exacta (0–100) y luego traducirla en **3 niveles prácticos de acción para UTP**: *Incorporar a tutoría* (< 68 pts), *Hacer seguimiento* (zona límite) y *Sin apoyo por ahora*.

2. **El caso menciona bienestar emocional, pero el modelo no lo mide. ¿Cómo justifican esa ausencia ante Orientación?**
   > **Respuesta:** Esa brecha la anticipamos desde la planificación en EP3 como un riesgo y, al confirmarla en el EDA, la registramos formalmente en GitHub (**Issue #14**). En lugar de inventar una variable falsa, aplicamos nuestra mitigación: dejamos una advertencia explícita en el Dashboard (*"Lo que esta herramienta no hace"*) para que Orientación sepa ese límite y propusimos incorporar una encuesta breve semestral de bienestar en la siguiente etapa.

3. **¿Cómo garantizan privacidad (RNF1) y que el modelo no discrimina (RNF2)?**
   > **Respuesta:** Para **RNF1 (Ley 19.628)** trabajamos únicamente con registros anónimos sin RUT ni nombres, y mediante **RNF5** bloqueamos los CSV crudos con `.gitignore`. Para **RNF2 (equidad)** excluimos género y etnia del modelo y medimos que la diferencia promedio de error según escolaridad de los padres es de apenas **0,03 puntos**, muy por debajo del límite de 10 puntos fijado en EP3.

4. **Si la asistencia es lo que más pesa, ¿basta con obligar a los estudiantes a ir a clases para subir sus notas?**
   > **Respuesta:** No, porque **correlación no es causalidad**. Una baja asistencia es la mejor señal temprana de riesgo, pero suele ser síntoma de problemas de salud, familiares o de desmotivación. El sistema no busca sancionar la inasistencia, sino avisar a tiempo a UTP y Orientación para acompañar al estudiante.

---

### B. Perspectiva del Gerente de Informática (TI)

5. **¿Por qué descartaron las notas de lectura, ciencias y el promedio general (`GPA`) si tenían altísima relación con matemáticas?**
   > **Respuesta:** Para evitar **fuga de datos (*data leakage*)**. Esas calificaciones se obtienen al final del mismo semestre que matemáticas. Si las usáramos, el modelo parecería casi perfecto en el papel, pero sería inútil a mitad de año porque TI y UTP aún no tendrían esas notas finales disponibles.

6. **¿Por qué ganó Gradient Boosting y no Regresión Lineal?**
   > **Respuesta:** Porque **Gradient Boosting** logró el menor error en los 500.000 casos de prueba: redujo el error un **43%** frente a la línea base (cuadruplicando la meta de 10% en RF3), logró un error habitual de **± 4,5 puntos** (MAE), acertó en **9 de cada 10 casos** dentro de ± 10 puntos y demostró cero sobreajuste (solo 0,4% de diferencia entre entrenamiento y validación).

7. **¿Cómo validaron usar 500.000 filas de los 8 millones de entrenamiento y cómo sabe TI cuándo reentrenar en producción?**
   > **Respuesta:** Frente al problema de memoria local (**Issue #12**), trazamos la curva de aprendizaje y comprobamos que a partir de 200.000 filas el error ya se estabiliza por completo; usar 500.000 mantuvo intacta la precisión y redujo más de 90% el tiempo de cómputo. En producción, tanto el script como el Dashboard tienen monitoreo automático de **drift**: cuando llegan las notas reales, si el error RMSE sube más de **20%** respecto a la referencia, el sistema emite una alerta roja para que TI reentrene el modelo.

---

### C. Perspectiva del Gerente General / Dirección (Sponsor)

8. **¿Cómo aseguran que hubo control real del proyecto y no se armó todo a última hora?**
   > **Respuesta:** Todo está auditable en GitHub: estructuramos **4 Milestones** alineados a CRISP-DM con **14 Issues** trazables, commits ordenados, reportes de avance con semáforo en **VERDE** y 3 desviaciones reales registradas con su causa raíz y acción correctiva cerrada.

9. **Tuvieron 3 desviaciones en GitHub. ¿Eso significa que el proyecto se desordenó?**
   > **Respuesta:** Al contrario: en gestión de proyectos, registrar y cerrar desviaciones demuestra control efectivo. Cada una tuvo solución medible sin atrasar fechas: **#12** (muestra validada de 500k), **#13** (unificar 3 notebooks en 2 oficiales) y **#14** (transparentar la falta de bienestar emocional que ya estaba prevista como riesgo en EP3).

10. **¿Cuánto cuesta implementar esto en el colegio el próximo semestre?**
    > **Respuesta:** El costo de licencias es **cero pesos**, porque toda la solución corre en Python y Streamlit (software libre) sobre la infraestructura actual del colegio. Solo requiere coordinar la exportación mensual de asistencia desde el libro de clases y asignar los cupos de tutoría con UTP.
