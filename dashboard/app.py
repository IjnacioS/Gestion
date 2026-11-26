# Dashboard de Acompañamiento Académico — Caso 1 (Rendimiento en Matemáticas) SCY1102
# Ejecutar desde la raíz del repo:  streamlit run dashboard/app.py
# No carga train.csv: usa solo el modelo serializado y archivos JSON ligeros.

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

NOMBRES_ES = {
    "Age": "Edad",
    "Grade": "Grado escolar",
    "SES_Quartile": "Cuartil socioeconómico",
    "StudyHours": "Tiempo de estudio",
    "AttendanceRate": "Tasa de asistencia",
    "InternetAccess": "Acceso a internet",
    "ParentSupport": "Apoyo parental",
    "Extracurricular": "Participación extracurricular",
    "ParentalEducation": "Educación de los padres",
}
NOMBRES_MODELOS = {
    "linea_base_promedio": "Línea base (promedio)",
    "regresion_lineal": "Regresión lineal",
    "gradient_boosting": "Gradient Boosting",
}
VARIABLES_RELEVANTES = {"AttendanceRate", "StudyHours"}

st.set_page_config(page_title="Acompañamiento Académico | Matemáticas", layout="wide")

st.markdown(
    f"""
<style>
html, body, [class*="css"] {{ font-family: "Inter", "Segoe UI", "Helvetica Neue", Arial, sans-serif; }}
.block-container {{ padding-top: 2rem; max-width: 1280px; }}
h1, h2, h3 {{ color: {TEXTO}; letter-spacing: -0.01em; }}
h1 {{ font-weight: 700; font-size: 1.9rem !important; }}
h3 {{ font-weight: 600; font-size: 1.15rem !important; }}

/* Tarjetas KPI */
[data-testid="stMetric"] {{
    background: #FFFFFF;
    border: 1px solid {BORDE};
    border-top: 3px solid {AZUL};
    border-radius: 6px;
    padding: 14px 18px;
}}
[data-testid="stMetricLabel"] p {{
    font-size: 0.72rem !important; font-weight: 600; text-transform: uppercase;
    letter-spacing: 0.06em; color: {TEXTO_SUAVE};
}}
[data-testid="stMetricValue"] {{ font-size: 1.75rem; font-weight: 700; color: {AZUL}; }}

/* Pestañas */
.stTabs [data-baseweb="tab-list"] {{ gap: 4px; border-bottom: 1px solid {BORDE}; }}
.stTabs [data-baseweb="tab"] {{ font-weight: 600; color: {TEXTO_SUAVE}; padding: 8px 18px; }}
.stTabs [aria-selected="true"] {{ color: {AZUL}; }}

/* Bloques narrativos */
.eyebrow {{ font-size: 0.72rem; font-weight: 700; letter-spacing: 0.08em; text-transform: uppercase; color: {AZUL}; margin-bottom: 2px; }}
.contexto {{ background: {FONDO_2}; border: 1px solid {BORDE}; border-radius: 6px; padding: 10px 14px;
             color: {TEXTO_SUAVE}; font-size: 0.92rem; margin: 4px 0 18px 0; }}
.contexto b {{ color: {TEXTO}; }}
.alerta {{ border-left: 4px solid; border-radius: 4px; padding: 12px 16px; margin: 8px 0; font-size: 0.95rem; }}
.alerta .titulo {{ font-weight: 700; display: block; margin-bottom: 2px; }}
.nota {{ color: {TEXTO_SUAVE}; font-size: 0.82rem; }}
</style>
""",
    unsafe_allow_html=True,
)


# ---------------------------------------------------------------- Utilidades de presentación
def contexto(texto: str):
    st.markdown(f'<div class="contexto">{texto}</div>', unsafe_allow_html=True)


def titular(eyebrow: str, texto: str):
    st.markdown(f'<div class="eyebrow">{eyebrow}</div>', unsafe_allow_html=True)
    st.subheader(texto)


def alerta(tipo: str, titulo: str, detalle: str = ""):
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
    st.error(f"No se encontró un artefacto del modelo: {e}")
    st.stop()

VARIABLES = meta["variables"]
RMSE_VAL = float(meta["rmse_validacion"])
UMBRAL = float(meta["umbral_apoyo"])
GB_TEST = resumen["metricas_test"]["gradient_boosting"]
LIN_TEST = resumen["metricas_test"]["regresion_lineal"]
DIST = resumen["dataset"]["distribucion_math"]
IMP = resumen["importancia_permutacion_rmse"]
CORR = resumen["correlaciones_bivariadas"]


def predecir(df: pd.DataFrame) -> np.ndarray:
    X = df[VARIABLES].copy()
    X["ParentalEducation"] = X["ParentalEducation"].astype(object)
    return np.clip(modelo.predict(X), 0, 100)


# ---------------------------------------------------------------- Encabezado
st.markdown('<div class="eyebrow">SCY1102 · Caso 1 Educación · Rendimiento en matemáticas</div>', unsafe_allow_html=True)
st.title("La asistencia, no el origen familiar, anticipa quién necesitará apoyo en matemáticas")
st.markdown(
    f'<p class="nota">Modelo Gradient Boosting entrenado sobre 8 millones de registros y evaluado en 500.000 estudiantes no vistos. '
    f'Las predicciones son estimaciones con margen de error de ±{RMSE_VAL:.1f} puntos; orientan la priorización, no etiquetan al estudiante.</p>',
    unsafe_allow_html=True,
)

tab_ejec, tab_sim, tab_tec = st.tabs(["Vista Ejecutiva", "Simulador Individual", "Vista Técnica y Monitoreo"])

# ================================================================ 1. VISTA EJECUTIVA
with tab_ejec:
    contexto(
        "<b>Decisión que habilita:</b> dónde concentrar los recursos de tutoría. "
        "El modelo identifica qué factores anticipan el puntaje y fija un umbral objetivo para priorizar estudiantes."
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Puntaje promedio histórico", f"{DIST['media']:.2f} pts", help="Media de TestScore_Math (8M+ registros)")
    c2.metric("Variación explicada (R²)", f"{GB_TEST['r2']:.3f}", help="Proporción de la variación del puntaje explicada por el modelo en Test")
    c3.metric("Error promedio (MAE)", f"{GB_TEST['mae']:.2f} pts",
              f"-{GB_TEST['reduccion_error_vs_base_pct']}% vs. línea base", delta_color="inverse")
    c4.metric("Umbral de apoyo académico", f"{UMBRAL:.2f} pts", help=resumen["criterio_umbral"])

    st.write("")
    col_g, col_t = st.columns([3, 2], gap="large")

    with col_g:
        titular("Factores del desempeño",
                "La asistencia explica la mayor parte del desempeño; los factores categóricos apenas mueven el promedio")
        imp = pd.DataFrame({"var": list(IMP.keys()), "valor": [round(v, 3) + 0.0 for v in IMP.values()]})
        imp["nombre"] = imp["var"].map(NOMBRES_ES)
        imp["color"] = np.where(imp["var"].isin(VARIABLES_RELEVANTES), AZUL, GRIS)
        imp = imp.sort_values("valor")
        fig = go.Figure(go.Bar(
            x=imp["valor"], y=imp["nombre"], orientation="h",
            marker_color=imp["color"], texttemplate="+%{x:.2f} pts", textposition="outside",
            cliponaxis=False, hovertemplate="%{y}: +%{x:.3f} pts<extra></extra>",
        ))
        estilo_fig(fig, 380)
        fig.update_xaxes(title="Aumento del error (RMSE, puntos) al desordenar la variable",
                         range=[0, imp["valor"].max() * 1.18])
        fig.update_layout(margin=dict(l=10, r=40, t=10, b=10))
        st.plotly_chart(fig, width="stretch")
        st.markdown('<p class="nota">Importancia por permutación sobre el conjunto de prueba. '
                    'En azul, las dos variables con efecto medible; en gris, las que no cambian el error del modelo.</p>',
                    unsafe_allow_html=True)

    with col_t:
        titular("Implicancias", "Qué hacer con estos hallazgos")
        st.markdown(
            f"""
1. **Monitorear la asistencia como señal temprana.** Al omitirla, el error del modelo sube {IMP['AttendanceRate']:.2f} pts (correlación r = {CORR['AttendanceRate']:.3f}).
2. **Reforzar hábitos de estudio** como palanca secundaria (r = {CORR['StudyHours']:.3f}).
3. **No segmentar por origen familiar.** Educación parental, internet y actividades extracurriculares cambian el promedio en 0,04 pts o menos.
4. **Priorizar tutorías** para quienes tengan un puntaje estimado bajo **{UMBRAL:.2f} pts** (percentil 25).
5. **Confianza operativa:** el {GB_TEST['pct_dentro_10_pts']:.1f}% de las predicciones queda a ±10 pts del puntaje real.
"""
        )
        alerta("info", "Limitaciones",
               "El dataset no mide el bienestar emocional y la correlación no implica causalidad. "
               "Se excluyeron Gender y Race (ética) y TestScore_Reading, TestScore_Science y GPA (fuga de información).")

# ================================================================ 2. SIMULADOR INDIVIDUAL
with tab_sim:
    contexto(
        "<b>Decisión que habilita:</b> si un estudiante concreto debe entrar al programa de apoyo. "
        "Ajusta su perfil y observa cómo cambia el puntaje estimado y el nivel de alerta."
    )
    titular("Simulador de estudiante", "La asistencia es la palanca que más mueve el puntaje estimado de un estudiante")

    col_in, col_out = st.columns([3, 2], gap="large")
    with col_in:
        a, b = st.columns(2)
        with a:
            asistencia = st.slider("Tasa de asistencia (%)", 50.0, 100.0, 90.0, 0.5) / 100
            estudio = st.slider("Tiempo de estudio (unidad del dataset)", 0.0, 3.0, 1.0, 0.05,
                                help="Unidad pendiente de confirmar con el diccionario de datos.")
            edad = st.slider("Edad", 14, 18, 16)
            grado = st.slider("Grado escolar", 9, 12, 11)
            ses = st.select_slider("Cuartil socioeconómico", options=[1, 2, 3, 4], value=3)
        with b:
            educ = st.selectbox("Educación de los padres", ["<HS", "HS", "SomeCollege", "Bachelors+"], index=2)
            internet = st.radio("Acceso a internet", ["Sí", "No"], horizontal=True)
            apoyo = st.radio("Apoyo parental", ["Sí", "No"], index=1, horizontal=True)
            extra = st.radio("Participación extracurricular", ["Sí", "No"], horizontal=True)

    estudiante = pd.DataFrame([{
        "Age": edad, "Grade": grado, "SES_Quartile": ses, "StudyHours": estudio,
        "AttendanceRate": asistencia, "InternetAccess": int(internet == "Sí"),
        "ParentSupport": int(apoyo == "Sí"), "Extracurricular": int(extra == "Sí"),
        "ParentalEducation": educ,
    }])
    pred = float(predecir(estudiante)[0])
    lo, hi = max(0.0, pred - RMSE_VAL), min(100.0, pred + RMSE_VAL)

    if pred < UMBRAL:
        estado, color_estado = "apoyo", ROJO
    elif lo < UMBRAL:
        estado, color_estado = "vigilancia", AMBAR
    else:
        estado, color_estado = "ok", VERDE

    with col_out:
        gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=pred,
            number={"suffix": " pts", "valueformat": ".1f", "font": {"color": color_estado, "size": 44}},
            gauge={
                "axis": {"range": [0, 100], "tickcolor": GRIS},
                "bar": {"color": color_estado, "thickness": 0.3},
                "bgcolor": "#FFFFFF", "borderwidth": 0,
                "steps": [{"range": [0, UMBRAL], "color": "#FEE2E2"}, {"range": [UMBRAL, 100], "color": "#F1F5F9"}],
                "threshold": {"line": {"color": ROJO, "width": 3}, "value": UMBRAL},
            },
            title={"text": "Puntaje estimado en matemáticas", "font": {"size": 15, "color": TEXTO_SUAVE}},
        ))
        estilo_fig(gauge, 280)
        gauge.update_layout(margin=dict(l=20, r=20, t=50, b=10))
        st.plotly_chart(gauge, width="stretch")
        st.markdown(f"**Rango probable:** {lo:.1f} a {hi:.1f} pts (±{RMSE_VAL:.2f}, RMSE de validación)")
        if estado == "apoyo":
            alerta("apoyo", "Requiere apoyo académico",
                   f"El puntaje estimado está bajo el umbral de {UMBRAL:.2f} pts. Se recomienda derivar a tutoría.")
        elif estado == "vigilancia":
            alerta("vigilancia", "Zona de vigilancia",
                   "El puntaje estimado supera el umbral, pero el rango probable incluye valores bajo él. Conviene hacer seguimiento.")
        else:
            alerta("ok", "Sin alerta",
                   "El puntaje estimado y su rango probable están sobre el umbral de apoyo.")

# ================================================================ 3. VISTA TÉCNICA Y LOTE
with tab_tec:
    contexto(
        "<b>Decisión que habilita:</b> si el modelo es confiable para operar y a quiénes intervenir en un curso o nivel completo. "
        "Compara modelos, procesa listados de estudiantes y verifica que el error no se haya degradado."
    )
    mejora_vs_lineal = 100 * (1 - GB_TEST["rmse"] / LIN_TEST["rmse"])
    titular("Comparación de modelos",
            f"Gradient Boosting reduce el error {GB_TEST['reduccion_error_vs_base_pct']:.1f}% frente a la línea base, "
            f"aunque apenas supera a la regresión lineal")
    conjunto = st.radio("Conjunto de evaluación", ["Test", "Validación"], horizontal=True)
    clave = "metricas_test" if conjunto == "Test" else "metricas_validacion"
    tabla = pd.DataFrame([{
        "Modelo": NOMBRES_MODELOS.get(k, k), "MAE": v["mae"], "RMSE": v["rmse"], "R²": v["r2"],
        "% ±5 pts": v["pct_dentro_5_pts"], "% ±10 pts": v["pct_dentro_10_pts"],
    } for k, v in resumen[clave].items()])

    cg, ct = st.columns([2, 3], gap="large")
    with cg:
        fig_m = go.Figure(go.Bar(
            x=tabla["Modelo"], y=tabla["RMSE"], marker_color=[GRIS_CLARO, GRIS, AZUL],
            texttemplate="%{y:.3f}", textposition="outside", cliponaxis=False,
        ))
        estilo_fig(fig_m, 330)
        fig_m.update_yaxes(title="RMSE (puntos)", range=[0, tabla["RMSE"].max() * 1.15])
        st.plotly_chart(fig_m, width="stretch")
    with ct:
        st.dataframe(tabla.style.format({"MAE": "{:.3f}", "RMSE": "{:.3f}", "R²": "{:.3f}",
                                         "% ±5 pts": "{:.1f}", "% ±10 pts": "{:.1f}"}),
                     hide_index=True, width="stretch")
        st.markdown(
            f'<p class="nota">La ventaja de Gradient Boosting sobre la regresión lineal es de {mejora_vs_lineal:.2f}% en RMSE: '
            f'la relación entre variables y puntaje es casi lineal. Brecha train/validación {GB_TEST["brecha_train_val_pct"]}% '
            f'y sesgo medio {GB_TEST["sesgo_medio"]} pts, sin sobreajuste. Variables usadas: {", ".join(VARIABLES)}.</p>',
            unsafe_allow_html=True,
        )

    st.divider()
    st.markdown('<div class="eyebrow">Predicción por lote y monitoreo</div>', unsafe_allow_html=True)
    st.markdown(
        f'<p class="nota">Columnas requeridas: {", ".join(VARIABLES)}. '
        "Si el archivo incluye TestScore_Math, se compara con el puntaje real para detectar drift.</p>",
        unsafe_allow_html=True,
    )

    cu, ce = st.columns(2)
    with cu:
        archivo = st.file_uploader("Sube un CSV de estudiantes", type="csv")
    with ce:
        ejemplos = sorted(p.name for p in ENTRADAS.glob("*.csv")) if ENTRADAS.exists() else []
        ejemplo = st.selectbox("O usa un archivo de ejemplo de entradas/", ["(ninguno)"] + ejemplos)

    datos = None
    if archivo is not None:
        datos = pd.read_csv(archivo)
    elif ejemplo != "(ninguno)":
        datos = pd.read_csv(ENTRADAS / ejemplo)

    if datos is not None:
        faltan = [c for c in VARIABLES if c not in datos.columns]
        if faltan:
            alerta("apoyo", "Archivo incompatible", f"Faltan columnas en el CSV: {', '.join(faltan)}")
        else:
            p = predecir(datos)
            res = datos.copy()
            res["puntaje_predicho"] = p.round(1)
            res["rango_min"] = np.clip(p - RMSE_VAL, 0, 100).round(1)
            res["rango_max"] = np.clip(p + RMSE_VAL, 0, 100).round(1)
            res["requiere_apoyo"] = p < UMBRAL
            n, n_apoyo = len(res), int(res["requiere_apoyo"].sum())
            pct_apoyo = 100 * n_apoyo / n if n else 0.0

            hay_real = "TestScore_Math" in res.columns
            rmse_obs = mae_obs = None
            if hay_real:
                real = res["TestScore_Math"].astype(float)
                ok = real.notna().values
                rmse_obs = float(np.sqrt(np.mean((p[ok] - real[ok]) ** 2)))
                mae_obs = float(np.mean(np.abs(p[ok] - real[ok])))
            drift = hay_real and rmse_obs > 1.2 * RMSE_VAL

            n_fmt = f"{n:,}".replace(",", ".")
            if not hay_real:
                cierre = "sin puntaje real no es posible verificar el error del modelo"
            elif drift:
                cierre = "el error del modelo se degradó y conviene reentrenarlo"
            else:
                cierre = "el modelo mantiene su precisión"
            st.subheader(f"{n_apoyo} de {n_fmt} estudiantes ({pct_apoyo:.1f}%) requieren apoyo; {cierre}")

            k1, k2, k3 = st.columns(3)
            k1.metric("Estudiantes procesados", n_fmt)
            k2.metric("Requieren apoyo", n_apoyo)
            k3.metric("Porcentaje con alerta", f"{pct_apoyo:.1f}%")

            if hay_real:
                variacion = 100 * (rmse_obs / RMSE_VAL - 1)
                d1, d2, d3 = st.columns(3)
                d1.metric("RMSE observado", f"{rmse_obs:.2f}", f"{variacion:+.1f}% vs. validación", delta_color="inverse")
                d2.metric("MAE observado", f"{mae_obs:.2f}")
                d3.metric("RMSE de referencia", f"{RMSE_VAL:.2f}")
                if drift:
                    alerta("apoyo", "Alerta de drift",
                           "El error subió más de 20% respecto a validación. Se recomienda reentrenar el modelo.")
                else:
                    alerta("ok", "Monitoreo OK",
                           "El error se mantiene dentro de +20% del valor de validación.")
            else:
                alerta("vigilancia", "Monitoreo no disponible",
                       "El archivo no incluye TestScore_Math, por lo que no se puede calcular el drift.")

            cols = st.columns(2 if hay_real else 1, gap="large")
            with cols[0]:
                fig_h = px.histogram(res, x="puntaje_predicho", nbins=30,
                                     labels={"puntaje_predicho": "Puntaje predicho"},
                                     color_discrete_sequence=[AZUL])
                fig_h.add_vline(x=UMBRAL, line_dash="dash", line_color=ROJO,
                                annotation_text=f"Umbral {UMBRAL:.1f}", annotation_font_color=ROJO)
                estilo_fig(fig_h, 320)
                fig_h.update_yaxes(title="Estudiantes")
                st.plotly_chart(fig_h, width="stretch")
            if hay_real:
                with cols[1]:
                    muestra = res.sample(min(n, 2000), random_state=0)
                    fig_s = px.scatter(muestra, x="TestScore_Math", y="puntaje_predicho", opacity=0.35,
                                       color_discrete_sequence=[AZUL],
                                       labels={"TestScore_Math": "Puntaje real", "puntaje_predicho": "Puntaje predicho"})
                    fig_s.add_shape(type="line", x0=0, y0=0, x1=100, y1=100, line=dict(dash="dash", color=GRIS))
                    estilo_fig(fig_s, 320)
                    st.plotly_chart(fig_s, width="stretch")

            st.dataframe(res.head(200), width="stretch")
            st.download_button("Descargar predicciones (CSV)", res.to_csv(index=False).encode("utf-8"),
                               file_name="predicciones_lote.csv", mime="text/csv")
