# Sistema de Alerta Temprana en Matemáticas — Caso 1 SCY1102
# Ejecutar desde la raíz del repo:  streamlit run dashboard/app.py
# No carga train.csv: usa solo el modelo serializado y archivos JSON ligeros.
#
# Audiencias:
#   - Pestañas 1 a 3: equipo directivo y docentes del colegio (lenguaje simple, sin siglas técnicas).
#   - Pestaña 4: equipo técnico y comisión evaluadora (métricas y monitoreo detallados).

import json
import warnings
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

warnings.filterwarnings("ignore", category=UserWarning)

ROOT = Path(__file__).resolve().parent.parent
MODELS = ROOT / "models"
ENTRADAS = ROOT / "entradas"

# Paleta corporativa
AZUL = "#0F2C59"
VERDE = "#047857"
AMBAR = "#B45309"
ROJO = "#B91C1C"
GRIS = "#94A3B8"
GRIS_CLARO = "#CBD5E1"
TEXTO = "#0F172A"
TEXTO_SUAVE = "#475569"
BORDE = "#E2E8F0"
FONDO_2 = "#F8FAFC"

# Nombres comprensibles para el colegio
NOMBRES_ES = {
    "Age": "Edad",
    "Grade": "Curso",
    "SES_Quartile": "Nivel socioeconómico",
    "StudyHours": "Tiempo de estudio",
    "AttendanceRate": "Asistencia a clases",
    "InternetAccess": "Internet en casa",
    "ParentSupport": "Apoyo de la familia",
    "Extracurricular": "Actividades extraprogramáticas",
    "ParentalEducation": "Escolaridad de los padres",
}
NIVEL_INFLUENCIA = {"AttendanceRate": "Influencia alta", "StudyHours": "Influencia baja"}
EDUCACION_PADRES = {
    "<HS": "Enseñanza media incompleta",
    "HS": "Enseñanza media completa",
    "SomeCollege": "Estudios superiores incompletos",
    "Bachelors+": "Título universitario o superior",
}
NIVEL_SES = {1: "Bajo", 2: "Medio-bajo", 3: "Medio-alto", 4: "Alto"}
# Niveles de estudio relativos al resto de estudiantes (percentiles de la muestra de entradas/)
NIVEL_ESTUDIO = {"Muy bajo": 0.40, "Bajo": 0.76, "Promedio": 0.99, "Alto": 1.22, "Muy alto": 1.60}
NOMBRES_MODELOS = {
    "linea_base_promedio": "Línea base (promedio)",
    "regresion_lineal": "Regresión lineal",
    "gradient_boosting": "Gradient Boosting",
}
COLUMNAS_ID = ["Nombre", "nombre", "Estudiante", "estudiante", "ID", "id", "StudentID", "RUT", "rut"]

st.set_page_config(page_title="Alerta Temprana en Matemáticas", layout="wide")

st.markdown(
    f"""
<style>
html, body, [class*="css"] {{ font-family: "Inter", "Segoe UI", "Helvetica Neue", Arial, sans-serif; }}
.block-container {{ padding-top: 2rem; max-width: 1280px; }}
h1, h2, h3 {{ color: {TEXTO}; letter-spacing: -0.01em; }}
h1 {{ font-weight: 700; font-size: 1.9rem !important; }}
h3 {{ font-weight: 600; font-size: 1.15rem !important; }}
[data-testid="stMetric"] {{
    background: #FFFFFF; border: 1px solid {BORDE}; border-top: 3px solid {AZUL};
    border-radius: 6px; padding: 14px 18px;
}}
[data-testid="stMetricLabel"] p {{
    font-size: 0.72rem !important; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.06em; color: {TEXTO_SUAVE};
}}
[data-testid="stMetricValue"] {{ font-size: 1.75rem; font-weight: 700; color: {AZUL}; }}
.stTabs [data-baseweb="tab-list"] {{ gap: 4px; border-bottom: 1px solid {BORDE}; }}
.stTabs [data-baseweb="tab"] {{ font-weight: 600; color: {TEXTO_SUAVE}; padding: 8px 18px; }}
.stTabs [aria-selected="true"] {{ color: {AZUL}; }}
.eyebrow {{ font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: {AZUL}; margin-bottom: 2px; }}
.contexto {{ background: {FONDO_2}; border: 1px solid {BORDE}; border-radius: 6px; padding: 10px 14px;
             color: {TEXTO_SUAVE}; font-size: 0.95rem; margin: 4px 0 18px 0; }}
.contexto b {{ color: {TEXTO}; }}
.alerta {{ border-left: 4px solid; border-radius: 4px; padding: 12px 16px; margin: 8px 0; font-size: 0.95rem; }}
.alerta .titulo {{ font-weight: 700; display: block; margin-bottom: 2px; }}
.nota {{ color: {TEXTO_SUAVE}; font-size: 0.85rem; }}
.cifra {{ font-size: 2.6rem; font-weight: 700; line-height: 1.1; }}
</style>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------- Utilidades
def num(x, d=1):
    """Formato numérico chileno: 1.234,5"""
    return f"{x:,.{d}f}".replace(",", "X").replace(".", ",").replace("X", ".")


def contexto(texto):
    st.markdown(f'<div class="contexto">{texto}</div>', unsafe_allow_html=True)


def titular(eyebrow, texto):
    st.markdown(f'<div class="eyebrow">{eyebrow}</div>', unsafe_allow_html=True)
    st.subheader(texto)


def nota(texto):
    st.markdown(f'<p class="nota">{texto}</p>', unsafe_allow_html=True)


def alerta(tipo, titulo, detalle=""):
    colores = {"ok": (VERDE, "#ECFDF5"), "vigilancia": (AMBAR, "#FFFBEB"),
               "apoyo": (ROJO, "#FEF2F2"), "info": (AZUL, "#EFF6FF")}
    borde, fondo = colores[tipo]
    st.markdown(
        f'<div class="alerta" style="border-color:{borde}; background:{fondo}; color:{TEXTO};">'
        f'<span class="titulo" style="color:{borde};">{titulo}</span>{detalle}</div>',
        unsafe_allow_html=True,
    )


def estilo_fig(fig, height):
    fig.update_layout(
        height=height, plot_bgcolor="#FFFFFF", paper_bgcolor="#FFFFFF",
        font=dict(family="Inter, Segoe UI, Arial, sans-serif", color=TEXTO, size=13),
        margin=dict(l=10, r=10, t=20, b=10),
    )
    fig.update_xaxes(gridcolor=BORDE, zerolinecolor=BORDE)
    fig.update_yaxes(gridcolor=BORDE, zerolinecolor=BORDE)
    return fig


def grafico_importancia(etiquetas_simples: bool):
    imp = pd.DataFrame({"var": list(IMP.keys()), "valor": [round(v, 3) + 0.0 for v in IMP.values()]})
    imp["nombre"] = imp["var"].map(NOMBRES_ES)
    imp["color"] = np.where(imp["var"].isin(NIVEL_INFLUENCIA), AZUL, GRIS)
    if etiquetas_simples:
        imp["texto"] = imp["var"].map(NIVEL_INFLUENCIA).fillna("Sin influencia medible")
    else:
        imp["texto"] = imp["valor"].map(lambda v: f"+{v:.2f} pts")
    imp = imp.sort_values("valor")
    fig = go.Figure(go.Bar(
        x=imp["valor"], y=imp["nombre"], orientation="h", marker_color=imp["color"],
        text=imp["texto"], textposition="outside", cliponaxis=False,
        hovertemplate="%{y}: +%{x:.3f} pts<extra></extra>",
    ))
    estilo_fig(fig, 380)
    fig.update_xaxes(range=[0, imp["valor"].max() * (1.35 if etiquetas_simples else 1.18)],
                     showticklabels=not etiquetas_simples,
                     title=None if etiquetas_simples else "Aumento del error (RMSE, puntos) al desordenar la variable")
    fig.update_layout(margin=dict(l=10, r=40, t=10, b=10))
    return fig


# ---------------------------------------------------------------- Carga de artefactos
@st.cache_resource
def cargar_modelo():
    return joblib.load(MODELS / "modelo_matematicas.joblib")


@st.cache_data
def cargar_json(nombre):
    return json.loads((MODELS / nombre).read_text(encoding="utf-8"))


try:
    modelo = cargar_modelo()
    meta = cargar_json("metadatos.json")
    resumen = cargar_json("resumen_metricas.json")
except FileNotFoundError as e:
    st.error(f"No se encontró un archivo del sistema: {e}")
    st.stop()

VARIABLES = meta["variables"]
RMSE_VAL = float(meta["rmse_validacion"])
UMBRAL = float(meta["umbral_apoyo"])
GB_TEST = resumen["metricas_test"]["gradient_boosting"]
LIN_TEST = resumen["metricas_test"]["regresion_lineal"]
DIST = resumen["dataset"]["distribucion_math"]
IMP = resumen["importancia_permutacion_rmse"]
CORR = resumen["correlaciones_bivariadas"]


def predecir(df):
    X = df[VARIABLES].copy()
    X["ParentalEducation"] = X["ParentalEducation"].astype(object)
    return np.clip(modelo.predict(X), 0, 100)


def recomendacion(p):
    if p < UMBRAL:
        return "Incorporar a tutoría"
    if p - RMSE_VAL < UMBRAL:
        return "Hacer seguimiento"
    return "Sin apoyo por ahora"


# ---------------------------------------------------------------- Encabezado
st.markdown('<div class="eyebrow">Sistema de alerta temprana · Matemáticas</div>', unsafe_allow_html=True)
st.title("La asistencia a clases es la señal más clara de quién necesitará apoyo en matemáticas")
nota(
    "Esta herramienta estima el puntaje que obtendría un estudiante en la prueba de matemáticas (escala de 0 a 100) "
    "a partir de datos que el colegio ya conoce, para identificar a tiempo a quienes podrían necesitar apoyo. "
    "Es una orientación: no reemplaza el criterio de profesores y equipo directivo."
)

tab_res, tab_est, tab_curso, tab_tec = st.tabs(
    ["Resumen para el colegio", "Evaluar a un estudiante", "Revisar un curso completo", "Detalle técnico"]
)

# ================================================================ 1. RESUMEN PARA EL COLEGIO
with tab_res:
    contexto(
        "<b>Para qué sirve esta vista:</b> decidir en qué concentrar los esfuerzos de apoyo académico. "
        "Resume qué factores pesan más en el resultado de matemáticas y qué tan confiable es la estimación."
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Puntaje promedio de los estudiantes", f"{num(DIST['media'], 0)} de 100")
    c2.metric("Margen de error habitual", f"± {num(GB_TEST['mae'], 1)} puntos",
              help="En promedio, la estimación se aleja en esta cantidad de puntos del resultado real.")
    c3.metric("Estimaciones acertadas", f"{round(GB_TEST['pct_dentro_10_pts'] / 10)} de cada 10",
              help="Proporción de estudiantes cuya estimación quedó a menos de 10 puntos de su resultado real.")
    c4.metric("Se sugiere apoyo bajo", f"{num(UMBRAL, 0)} puntos",
              help="Corresponde al 25% de estudiantes con los puntajes más bajos.")

    st.write("")
    col_g, col_t = st.columns([3, 2], gap="large")
    with col_g:
        titular("Qué influye en el resultado",
                "La asistencia es lo que más pesa; el origen familiar casi no cambia el puntaje")
        st.plotly_chart(grafico_importancia(etiquetas_simples=True), width="stretch")
        nota("La barra indica cuánto pierde precisión la estimación cuando no se conoce ese dato. "
             "En azul, los factores que sí influyen; en gris, los que no muestran efecto.")

    with col_t:
        titular("Qué significa para el colegio", "Cuatro conclusiones para la gestión")
        st.markdown(
            f"""
1. **Vigilar la asistencia como señal de alerta temprana.** Es, por lejos, el dato que mejor anticipa el resultado.
2. **Fomentar hábitos de estudio**, que tienen un efecto menor, pero positivo.
3. **No clasificar a los estudiantes por su origen.** La escolaridad de los padres, tener internet o participar en actividades extraprogramáticas cambian el promedio en menos de 0,1 puntos.
4. **Priorizar tutorías** para quienes tengan un puntaje estimado bajo **{num(UMBRAL, 0)} puntos**.
"""
        )
        alerta("info", "Lo que esta herramienta no hace",
               "No mide el estado emocional del estudiante ni explica las causas de su resultado: muestra asociaciones. "
               "Tampoco usa género ni etnia, para no generar decisiones discriminatorias.")

# ================================================================ 2. EVALUAR A UN ESTUDIANTE
with tab_est:
    contexto(
        "<b>Para qué sirve esta vista:</b> decidir si un estudiante en particular debería recibir apoyo. "
        "Completa sus datos y la herramienta estima su puntaje y entrega una recomendación."
    )
    titular("Evaluación individual", "Una baja asistencia basta para que un estudiante quede en zona de apoyo")

    col_in, col_out = st.columns([3, 2], gap="large")
    with col_in:
        a, b = st.columns(2)
        with a:
            asistencia = st.slider("Asistencia a clases (%)", 50, 100, 90) / 100
            nivel_estudio = st.select_slider("Tiempo de estudio, comparado con sus compañeros",
                                             options=list(NIVEL_ESTUDIO), value="Promedio")
            edad = st.slider("Edad (años)", 14, 18, 16)
            curso = st.select_slider("Curso", options=[9, 10, 11, 12], value=11,
                                     format_func=lambda g: f"{g - 8}° medio")
            ses = st.select_slider("Nivel socioeconómico de la familia", options=[1, 2, 3, 4], value=3,
                                   format_func=lambda q: NIVEL_SES[q])
        with b:
            educ = st.selectbox("Escolaridad de los padres", list(EDUCACION_PADRES), index=2,
                                format_func=lambda k: EDUCACION_PADRES[k])
            internet = st.radio("Tiene internet en casa", ["Sí", "No"], horizontal=True)
            apoyo = st.radio("Recibe apoyo de su familia en los estudios", ["Sí", "No"], index=1, horizontal=True)
            extra = st.radio("Participa en actividades extraprogramáticas", ["Sí", "No"], horizontal=True)

    base = {
        "Age": edad, "Grade": curso, "SES_Quartile": ses, "StudyHours": NIVEL_ESTUDIO[nivel_estudio],
        "AttendanceRate": asistencia, "InternetAccess": int(internet == "Sí"),
        "ParentSupport": int(apoyo == "Sí"), "Extracurricular": int(extra == "Sí"),
        "ParentalEducation": educ,
    }
    pred = float(predecir(pd.DataFrame([base]))[0])
    lo, hi = max(0.0, pred - RMSE_VAL), min(100.0, pred + RMSE_VAL)
    rec = recomendacion(pred)
    color_estado = {"Incorporar a tutoría": ROJO, "Hacer seguimiento": AMBAR, "Sin apoyo por ahora": VERDE}[rec]

    with col_out:
        st.markdown(
            f'<div class="eyebrow">Puntaje estimado en matemáticas</div>'
            f'<div class="cifra" style="color:{color_estado};">{num(pred, 0)} <span style="font-size:1.1rem; color:{TEXTO_SUAVE};">de 100</span></div>'
            f'<p class="nota">Lo más probable es que obtenga entre <b>{num(lo, 0)}</b> y <b>{num(hi, 0)}</b> puntos.</p>',
            unsafe_allow_html=True,
        )
        barra = go.Figure()
        barra.add_trace(go.Bar(x=[100], y=[""], orientation="h", marker_color="#F1F5F9", hoverinfo="skip"))
        barra.add_trace(go.Bar(x=[pred], y=[""], orientation="h", marker_color=color_estado, hoverinfo="skip", width=0.5))
        barra.add_vline(x=UMBRAL, line_color=ROJO, line_dash="dash",
                        annotation_text=f"Apoyo bajo {num(UMBRAL, 0)}", annotation_font_color=ROJO)
        estilo_fig(barra, 110)
        barra.update_layout(barmode="overlay", showlegend=False, margin=dict(l=0, r=0, t=30, b=0))
        barra.update_xaxes(range=[0, 100], showgrid=False)
        st.plotly_chart(barra, width="stretch")

        if rec == "Incorporar a tutoría":
            alerta("apoyo", "Recomendación: incorporar a tutoría",
                   f"Su puntaje estimado está bajo los {num(UMBRAL, 0)} puntos sugeridos para recibir apoyo.")
        elif rec == "Hacer seguimiento":
            alerta("vigilancia", "Recomendación: hacer seguimiento",
                   "Su puntaje estimado está cerca del límite; con el margen de error, podría quedar bajo él.")
        else:
            alerta("ok", "Recomendación: sin apoyo por ahora",
                   "Su puntaje estimado está por sobre el nivel que sugiere apoyo, incluso considerando el margen de error.")

        # Escenario de mejora: qué pasaría con mayor asistencia
        if asistencia < 0.95:
            pred_95 = float(predecir(pd.DataFrame([{**base, "AttendanceRate": 0.95}]))[0])
            if pred_95 - pred >= 1:
                nota(f"<b>Escenario:</b> si su asistencia subiera a 95%, su puntaje estimado pasaría de "
                     f"{num(pred, 0)} a {num(pred_95, 0)} puntos. Es una estimación, no una garantía.")

# ================================================================ 3. REVISAR UN CURSO COMPLETO
with tab_curso:
    contexto(
        "<b>Para qué sirve esta vista:</b> obtener en un solo paso la lista de estudiantes de un curso o nivel "
        "que conviene incorporar a tutoría o seguir de cerca, y descargarla."
    )

    cu, ce = st.columns(2)
    with cu:
        archivo = st.file_uploader("Sube la planilla del curso (formato CSV)", type="csv")
    with ce:
        ejemplos = sorted(p.name for p in ENTRADAS.glob("*.csv")) if ENTRADAS.exists() else []
        ejemplo = st.selectbox("O prueba con una planilla de ejemplo", ["(ninguna)"] + ejemplos)
        if (ENTRADAS / "nuevos_estudiantes.csv").exists():
            st.download_button("Descargar planilla modelo", (ENTRADAS / "nuevos_estudiantes.csv").read_bytes(),
                               file_name="planilla_modelo.csv", mime="text/csv")

    with st.expander("Qué columnas debe tener la planilla"):
        st.markdown(
            "| Columna | Contenido |\n| :--- | :--- |\n"
            "| Age | Edad en años |\n| Grade | Curso (9 = 1° medio … 12 = 4° medio) |\n"
            "| SES_Quartile | Nivel socioeconómico del 1 (bajo) al 4 (alto) |\n"
            "| StudyHours | Tiempo de estudio (misma escala del registro original) |\n"
            "| AttendanceRate | Asistencia como proporción (0,90 = 90%) |\n"
            "| InternetAccess | Internet en casa (1 = sí, 0 = no) |\n"
            "| ParentSupport | Apoyo familiar (1 = sí, 0 = no) |\n"
            "| Extracurricular | Actividades extraprogramáticas (1 = sí, 0 = no) |\n"
            "| ParentalEducation | <HS, HS, SomeCollege o Bachelors+ |\n"
            "| TestScore_Math | Opcional: puntaje real, para comprobar si el sistema sigue acertando |\n"
            "| Nombre o ID | Opcional: para identificar a cada estudiante en el resultado |"
        )

    datos = None
    if archivo is not None:
        datos = pd.read_csv(archivo)
    elif ejemplo != "(ninguna)":
        datos = pd.read_csv(ENTRADAS / ejemplo)

    if datos is not None:
        faltan = [c for c in VARIABLES if c not in datos.columns]
        if faltan:
            alerta("apoyo", "La planilla no tiene el formato esperado",
                   f"Faltan estas columnas: {', '.join(faltan)}. Revisa la planilla modelo.")
        else:
            p = predecir(datos)
            col_id = next((c for c in COLUMNAS_ID if c in datos.columns), None)
            tabla = pd.DataFrame({
                "Estudiante": datos[col_id].astype(str) if col_id else [f"Fila {i + 1}" for i in range(len(datos))],
                "Asistencia": (datos["AttendanceRate"] * 100).round(0).astype(int).astype(str) + "%",
                "Puntaje estimado": p.round(0).astype(int),
                "Rango probable": [f"{max(0, round(x - RMSE_VAL))} a {min(100, round(x + RMSE_VAL))}" for x in p],
                "Recomendación": [recomendacion(x) for x in p],
            })
            n = len(tabla)
            conteo = tabla["Recomendación"].value_counts()
            n_tut, n_seg = int(conteo.get("Incorporar a tutoría", 0)), int(conteo.get("Hacer seguimiento", 0))
            n_ok = n - n_tut - n_seg

            st.subheader(f"{n_tut} de {num(n, 0)} estudiantes ({num(100 * n_tut / n, 0)}%) deberían incorporarse a tutoría "
                         f"y {n_seg} requieren seguimiento")
            k1, k2, k3 = st.columns(3)
            k1.metric("Incorporar a tutoría", n_tut)
            k2.metric("Hacer seguimiento", n_seg)
            k3.metric("Sin apoyo por ahora", n_ok)

            fig_r = go.Figure(go.Bar(
                x=[n_tut, n_seg, n_ok], y=["Incorporar a tutoría", "Hacer seguimiento", "Sin apoyo por ahora"],
                orientation="h", marker_color=[ROJO, AMBAR, VERDE],
                text=[n_tut, n_seg, n_ok], textposition="outside", cliponaxis=False,
            ))
            estilo_fig(fig_r, 200)
            fig_r.update_xaxes(showticklabels=False, showgrid=False, range=[0, max(n_tut, n_seg, n_ok) * 1.15])
            fig_r.update_yaxes(autorange="reversed")
            st.plotly_chart(fig_r, width="stretch")

            solo_prioridad = st.checkbox("Mostrar solo estudiantes que requieren tutoría o seguimiento", value=True)
            orden = {"Incorporar a tutoría": 0, "Hacer seguimiento": 1, "Sin apoyo por ahora": 2}
            vista = tabla.assign(_o=tabla["Recomendación"].map(orden)).sort_values(["_o", "Puntaje estimado"]).drop(columns="_o")
            if solo_prioridad:
                vista = vista[vista["Recomendación"] != "Sin apoyo por ahora"]

            def color_rec(v):
                c = {"Incorporar a tutoría": ROJO, "Hacer seguimiento": AMBAR, "Sin apoyo por ahora": VERDE}.get(v, TEXTO)
                return f"color: {c}; font-weight: 600"

            st.dataframe(vista.style.map(color_rec, subset=["Recomendación"]), hide_index=True, width="stretch")
            st.download_button("Descargar lista de estudiantes (CSV)",
                               vista.to_csv(index=False).encode("utf-8-sig"),
                               file_name="lista_apoyo_matematicas.csv", mime="text/csv")

            # Comprobación de confiabilidad (solo si hay puntaje real)
            if "TestScore_Math" in datos.columns:
                real = datos["TestScore_Math"].astype(float)
                ok = real.notna().values
                rmse_obs = float(np.sqrt(np.mean((p[ok] - real[ok]) ** 2)))
                mae_obs = float(np.mean(np.abs(p[ok] - real[ok])))
                st.write("")
                titular("¿El sistema sigue acertando?", "Comparación con los puntajes reales de esta planilla")
                if rmse_obs > 1.2 * RMSE_VAL:
                    alerta("apoyo", "Las estimaciones se están alejando de los resultados reales",
                           f"En este grupo la estimación se equivocó en promedio {num(mae_obs)} puntos, más de lo esperado "
                           f"(cerca de {num(GB_TEST['mae'])}). Recomendamos avisar al equipo técnico para actualizar el sistema.")
                else:
                    alerta("ok", "El sistema sigue siendo confiable",
                           f"En este grupo la estimación se equivocó en promedio {num(mae_obs)} puntos, "
                           f"similar a lo esperado (cerca de {num(GB_TEST['mae'])}).")
                with st.expander("Detalle técnico del monitoreo"):
                    variacion = 100 * (rmse_obs / RMSE_VAL - 1)
                    d1, d2, d3 = st.columns(3)
                    d1.metric("RMSE observado", f"{rmse_obs:.2f}", f"{variacion:+.1f}% vs. validación", delta_color="inverse")
                    d2.metric("MAE observado", f"{mae_obs:.2f}")
                    d3.metric("RMSE de referencia", f"{RMSE_VAL:.2f}")
                    nota("Regla de drift: alerta si el RMSE observado supera en más de 20% al RMSE de validación.")
            else:
                nota("Si la planilla incluye el puntaje real (TestScore_Math), aquí se mostrará si el sistema sigue acertando.")

# ================================================================ 4. DETALLE TÉCNICO
with tab_tec:
    contexto(
        "<b>Para el equipo técnico y la comisión evaluadora:</b> respaldo cuantitativo de la herramienta, "
        "comparación de modelos y criterios de monitoreo."
    )
    mejora_vs_lineal = 100 * (1 - GB_TEST["rmse"] / LIN_TEST["rmse"])
    titular("Comparación de modelos",
            f"Gradient Boosting reduce el error {GB_TEST['reduccion_error_vs_base_pct']:.1f}% frente a la línea base, "
            f"aunque apenas supera a la regresión lineal")
    conjunto = st.radio("Conjunto de evaluación", ["Test", "Validación"], horizontal=True)
    clave = "metricas_test" if conjunto == "Test" else "metricas_validacion"
    comp = pd.DataFrame([{
        "Modelo": NOMBRES_MODELOS.get(k, k), "MAE": v["mae"], "RMSE": v["rmse"], "R²": v["r2"],
        "% ±5 pts": v["pct_dentro_5_pts"], "% ±10 pts": v["pct_dentro_10_pts"],
    } for k, v in resumen[clave].items()])

    cg, ct = st.columns([2, 3], gap="large")
    with cg:
        fig_m = go.Figure(go.Bar(
            x=comp["Modelo"], y=comp["RMSE"], marker_color=[GRIS_CLARO, GRIS, AZUL],
            texttemplate="%{y:.3f}", textposition="outside", cliponaxis=False,
        ))
        estilo_fig(fig_m, 330)
        fig_m.update_yaxes(title="RMSE (puntos)", range=[0, comp["RMSE"].max() * 1.15])
        st.plotly_chart(fig_m, width="stretch")
    with ct:
        st.dataframe(comp.style.format({"MAE": "{:.3f}", "RMSE": "{:.3f}", "R²": "{:.3f}",
                                        "% ±5 pts": "{:.1f}", "% ±10 pts": "{:.1f}"}),
                     hide_index=True, width="stretch")
        nota(f"La ventaja de Gradient Boosting sobre la regresión lineal es de {mejora_vs_lineal:.2f}% en RMSE: "
             f"la relación entre variables y puntaje es casi lineal. Brecha train/validación {GB_TEST['brecha_train_val_pct']}% "
             f"y sesgo medio {GB_TEST['sesgo_medio']} pts, sin sobreajuste. Variables: {', '.join(VARIABLES)}.")

    st.divider()
    titular("Importancia por permutación",
            "La asistencia explica la mayor parte del desempeño; los factores categóricos apenas mueven el promedio")
    st.plotly_chart(grafico_importancia(etiquetas_simples=False), width="stretch")
    nota(f"Correlación con el puntaje: asistencia r = {CORR['AttendanceRate']:.3f}; tiempo de estudio r = {CORR['StudyHours']:.3f}. "
         "Excluidas por fuga de información: TestScore_Reading, TestScore_Science, GPA. Excluidas por ética: Gender, Race.")

    with st.expander("Glosario: cómo se tradujeron las métricas para el colegio"):
        st.markdown(
            f"""
| Métrica técnica | Valor (Test) | Cómo se presenta al colegio |
| :--- | :---: | :--- |
| MAE | {GB_TEST['mae']:.3f} | "Margen de error habitual: ± {num(GB_TEST['mae'])} puntos" |
| % dentro de ±10 pts | {GB_TEST['pct_dentro_10_pts']:.1f}% | "{round(GB_TEST['pct_dentro_10_pts'] / 10)} de cada 10 estimaciones acertadas" |
| RMSE validación | {RMSE_VAL:.3f} | "Rango probable" del puntaje (estimación ± RMSE) |
| Umbral P25 | {UMBRAL:.2f} | "Se sugiere apoyo bajo {num(UMBRAL, 0)} puntos" |
| Drift (RMSE > +20%) | — | "¿El sistema sigue acertando?" |
| Importancia por permutación | — | Influencia alta / baja / sin influencia medible |
| R² | {GB_TEST['r2']:.3f} | Se omite en la vista del colegio (concepto poco intuitivo) |
"""
        )
