# Guion de Defensa Ejecutiva y Banco de Preguntas Críticas — EP6 (SCY1102)

**Proyecto:** Caso 1 — Sistema de Alerta Temprana para el Rendimiento Académico en Matemáticas  
**Asignatura:** SCY1102 Gestión de Proyectos de Datos (Duoc UC)  
**Docente:** Michael Palomino B.  
**Duración Total Exacta:** 10 minutos (600 segundos) + Ronda de preguntas del jurado  
**Equipo Expositor:** Ignacio Sobarzo · Diego Yañez · Felipe Espinoza  
**Presentación Asociada:** `docs/entregables/Presentacion_EP6_Caso1_Matematicas.pptx` (11 láminas)

---

## 1. Reparto Exacto para 10 Minutos (Cronograma por Lámina)

| Lámina | Tiempo | Acumulado | Expositor | Mensaje Clave y Conexión con el Plan EP3 |
| :---: | :---: | :---: | :--- | :--- |
| **1. Portada** | 0:25 | 0:25 | Ignacio Sobarzo | Saludo al docente Michael Palomino B. y al jurado; presentación del equipo y propósito: transformar datos escolares en apoyo preventivo en matemáticas. |
| **2. Contexto y Actores EP3** | 0:50 | 1:15 | Ignacio Sobarzo | Explicar el problema de detectar tarde los bajos resultados y cómo la solución sirve a los 5 actores definidos en EP3: **Dirección (Sponsor), UTP (Contraparte), Docentes de matemáticas, Orientación y TI**. |
| **3. Requerimientos RF/RNF** | 0:55 | 2:10 | Ignacio Sobarzo | Demostrar el cumplimiento del Plan EP3: **RF3** (meta $\ge 10\%$ superada con **43% menos error**), **RF4** (puntaje continuo + 3 niveles de alerta), **RNF1** (Ley 19.628), **RNF2** (brecha de solo 0,03 pts $\le 10$ pts) y **RNF5** (`.gitignore`). |
| **4. Técnica 1: Datos y Ética** | 0:55 | 3:05 | Diego Yañez | Explicar la base de 10 millones de registros sin datos faltantes y las dos exclusiones clave: notas finales (`GPA`, lectura, ciencias) por fuga de información y género/etnia por equidad. |
| **5. Técnica 2: Resultados** | 1:00 | 4:05 | Diego Yañez | Explicar con números claros que **Gradient Boosting** reduce el error un **43%**, se equivoca en promedio solo **$\pm 4,5$ puntos**, acierta en **9 de cada 10 estudiantes ($\pm 10$ pts)** y mantiene **0,03 puntos** de brecha por educación parental. |
| **6. Técnica 3: Factores y CLI** | 1:00 | 5:05 | Diego Yañez | Destacar que la **asistencia a clases** es la señal determinante, cómo opera el script por lotes (E5) con los **3 niveles de recomendación (RF4)** y la alerta automática a TI si el error sube más de **20%**. |
| **7. Demo: Dashboard (E6)** | 1:20 | 6:25 | Diego Yañez | Mostrar las capturas reales del Dashboard Streamlit y guiar los 3 pasos de la demo en vivo: (1) Vista UTP/Dirección, (2) Simulador individual con 3 niveles de alerta y (3) Nómina CSV de curso completo. |
| **8. Gestión 1: EP3 ↔ GitHub** | 0:50 | 7:15 | Felipe Espinoza | Mostrar la tabla de trazabilidad que une los **4 Milestones de GitHub (M1–M4)** con los **Hitos H1–H6** y **Entregables E1–E7** de EP3, respaldada por las capturas reales del repositorio. |
| **9. Gestión 2: Semáforo** | 0:50 | 8:05 | Felipe Espinoza | Presentar el semáforo global en **VERDE**: 100% de los entregables E1 a E7 construidos, 14 issues documentados y las 3 desviaciones resueltas a tiempo. |
| **10. Gestión 3: Desviaciones y R4** | 1:05 | 9:10 | Felipe Espinoza | Explicar las 3 desviaciones reales (#12 muestra 500k de 8M, #13 consolidación de 3 notebooks en 2) y destacar cómo el **Issue #14 activó el Riesgo R4 anticipado en EP3** (falta de bienestar emocional), junto con la mitigación de R2, R3 y R7. |
| **11. Valor y Próximos Pasos** | 0:50 | **10:00** | Ignacio Sobarzo | Cierre ejecutivo: valor para Dirección, UTP, Docentes, Orientación y TI; rigor ético (asociación $\ne$ causalidad) y los 3 pasos para el piloto semestral. |

---

## 2. Banco de 10 Preguntas Difíciles del Jurado y Respuestas Modelo

### A. Perspectiva del Cliente / UTP y Orientación (4 Preguntas)

#### 1. En el Plan de EP3 el requerimiento RF4 hablaba de clasificar el rendimiento, pero ustedes entregaron un puntaje continuo de 0 a 100 con 3 niveles de alerta. ¿Por qué hicieron ese ajuste?
**Respuesta:** Fue una decisión técnica y pedagógica acordada para proteger la validez del sistema para **UTP**. El dataset original no traía categorías oficiales ("bajo/medio/alto"), por lo que inventar cortes arbitrarios durante el entrenamiento habría distorsionado la información. En cambio, predecimos el puntaje exacto de 0 a 100 y en el simulador lo traducimos en **3 niveles de acción claros para UTP y Orientación** usando el percentil 25 (68 puntos) y el margen de error: **Incorporar a tutoría** (bajo 68 pts), **Hacer seguimiento** (sobre 68 pts pero dentro del margen de riesgo) y **Sin apoyo por ahora**.

#### 2. El caso menciona "bienestar emocional", pero su sistema no lo mide. ¿Cómo justifican esa ausencia ante Orientación?
**Respuesta:** Esa brecha la anticipamos desde la planificación en EP3 como nuestro **Riesgo R4** y, al confirmarla en la exploración de datos, la registramos formalmente en GitHub como la **Desviación #14**. En lugar de inventar una variable falsa, aplicamos el plan de mitigación de R4: dejamos una advertencia explícita en el Dashboard ("Lo que esta herramienta no hace") para que Orientación sepa que el modelo evalúa hábitos escolares observables, y propusimos incorporar una encuesta breve semestral de bienestar estudiantil en la siguiente iteración.

#### 3. ¿Cómo garantizan que el sistema cumple los requerimientos de privacidad (RNF1) y equidad (RNF2) comprometidos en EP3?
**Respuesta:** Para **RNF1 (Ley 19.628)** trabajamos únicamente con registros anonimizados sin RUT ni datos sensibles en el modelo, y mediante **RNF5** bloqueamos en `.gitignore` cualquier subida de datos crudos a GitHub. Para **RNF2 (equidad $\le 10$ puntos de brecha)** excluimos género y etnia del entrenamiento y comprobamos empíricamente que la diferencia promedio entre grupos de distinta escolaridad parental es de apenas **0,03 puntos**, muy por debajo del máximo de 10 puntos exigido en EP3.

#### 4. Si la asistencia es lo que más pesa, ¿basta con exigir asistencia obligatoria para que suban las notas de matemáticas?
**Respuesta:** No, y así mitigamos explícitamente los **Riesgos R3 (mal uso punitivo) y R7 (confundir correlación con causalidad)** de nuestro plan EP3. Una caída en la asistencia es la mejor **señal de alerta temprana** (correlación de 0,815), pero suele ser síntoma de problemas familiares, de salud o desmotivación. El sistema no busca sancionar la inasistencia, sino avisarle a tiempo a UTP y Orientación para que apoyen al estudiante antes de la prueba.

---

### B. Perspectiva del Gerente de Informática / TI (3 Preguntas)

#### 5. ¿Por qué descartaron las notas de lectura, ciencias y el promedio general (`GPA`) si tenían altísima relación con matemáticas?
**Respuesta:** Para cumplir con **RF1/RF2** y evitar la **fuga de información (*data leakage*)**. Esas calificaciones se obtienen al final del mismo período que la prueba de matemáticas. Si las usáramos, el modelo parecería casi perfecto en el papel, pero no serviría como alerta temprana a mitad de semestre porque TI y UTP aún no tendrían esas notas finales disponibles.

#### 6. ¿Qué tan superior fue el modelo elegido frente a la meta RF3 de EP3 y por qué eligieron Gradient Boosting sobre Regresión Lineal?
**Respuesta:** En EP3 comprometimos en **RF3** mejorar al menos un **10%** respecto a la línea base (que tenía un error RMSE de 9,95 puntos). Nuestro modelo **Gradient Boosting** redujo el error en un **42,7% (~43%)**, bajando el RMSE a **5,69 puntos** y el error habitual (MAE) a **$\pm 4,5$ puntos**, acertando en **9 de cada 10 estudiantes** dentro de $\pm 10$ puntos. Elegimos Gradient Boosting porque logró el menor error en los 500.000 casos de prueba sin ningún sobreajuste (solo 0,4% de diferencia entre entrenamiento y validación), manteniendo la Regresión Lineal como respaldo comparativo en la pestaña técnica.

#### 7. ¿Cómo validaron el muestreo de 500.000 filas (Desviación #12) y cómo sabe TI cuándo debe reentrenar el modelo en producción?
**Respuesta:** Frente a los 8 millones de filas de entrenamiento (Issue #12), trazamos la **curva de aprendizaje** y comprobamos que a partir de 200.000 registros el error ya se estabiliza por completo; usar 500.000 filas mantuvo intacta la precisión y redujo en más de 90% el tiempo de cómputo. Para producción, tanto el script por lotes (E5) como el Dashboard (E6) incluyen monitoreo automático de **estabilidad (*drift*)**: cuando se cargan los puntajes reales del semestre, si el error RMSE sube más de un **20%** respecto a la referencia, el sistema emite una alerta roja para que TI reentrene el modelo.

---

### C. Perspectiva del Gerente General / Dirección — Sponsor (3 Preguntas)

#### 8. ¿Cómo se conectan los 4 Milestones de su repositorio GitHub con los Hitos H1–H6 y Entregables E1–E7 que aprobaron en el Plan de EP3?
**Respuesta:** Mantuvimos trazabilidad uno a uno: el **Milestone M1** cerró los hitos **H1 y H2** (entregables **E1** de alcance y **E2** de análisis exploratorio); **M2** cerró **H3 y H4** (**E3** flujo de preparación y **E4** modelo predictivo); **M3** cerró **H5** (**E5** script de automatización y **E6** Dashboard interactivo); y **M4** consolida el hito **H6** con el entregable **E7** (Informe EP5 y esta Defensa EP6), completando el 100% de los productos comprometidos.

#### 9. Tuvieron 3 desviaciones registradas en GitHub. ¿Qué demuestra que su control de proyecto fue efectivo y no improvisado?
**Respuesta:** Primero, que cada desviación tuvo una acción correctiva medible y cerrada en GitHub (#12 muestreo validado, #13 unificación de 3 notebooks duplicados en 2 oficiales con respaldo en `archive/`, y #14 falta de variable emocional). Y segundo, que la **Desviación #14** estaba prevista desde EP3 como el **Riesgo R4**, lo que demuestra que nuestra matriz de riesgos no fue un trámite documental, sino una herramienta viva que guio las decisiones del equipo durante toda la ejecución.

#### 10. Como Dirección del colegio (Sponsor), ¿qué inversión necesitamos para poner esto en marcha el próximo semestre y cuál es el beneficio concreto?
**Respuesta:** El costo de licencias es **cero**, porque toda la solución (E3 a E6) funciona sobre tecnologías abiertas en Python y Streamlit que TI puede alojar en infraestructura actual del colegio. Solo requerimos tres acuerdos operativos: (1) que TI exporte mensualmente la planilla de asistencia del libro de clases al script automático; (2) que UTP utilice la nómina de alerta para asignar los cupos de tutoría al 25% prioritario (bajo 68 puntos); y (3) que Orientación incorpore la encuesta breve de bienestar emocional (mitigación final de R4).
