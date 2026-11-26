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

st.set_page_config(page_title="Acompañamiento Académico — Matemáticas", page_icon="📘", layout="wide")


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


def predecir(df: pd.DataFrame) -> np.ndarray:
    X = df[VARIABLES].copy()
    X["ParentalEducation"] = X["ParentalEducation"].astype(object)
    return np.clip(modelo.predict(X), 0, 100)


# ---------------------------------------------------------------- Encabezado
st.title("📘 Dashboard de Acompañamiento Académico en Matemáticas")
st.caption(
    "SCY1102 — Caso 1: Educación · Modelo: Gradient Boosting (HistGradientBoostingRegressor) · "
    "Las predicciones son estimaciones con margen de error, no etiquetas sobre el estudiante."
)

tab_ejec, tab_sim, tab_tec = st.tabs(
    ["📊 Vista Ejecutiva", "🧑‍🎓 Simulador Individual", "🛠️ Vista Técnica y Monitoreo (Lote)"]
)

# ================================================================ 1. VISTA EJECUTIVA
with tab_ejec:
    gb_test = resumen["metricas_test"]["gradient_boosting"]
    dist = resumen["dataset"]["distribucion_math"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Puntaje promedio histórico", f"{dist['media']:.2f} pts", help="Media de TestScore_Math (8M+ registros)")
    c2.metric("R² en Test", f"{gb_test['r2']:.3f}", help="Proporción de la variación explicada por el modelo")
    c3.metric("Error promedio (MAE)", f"{gb_test['mae']:.2f} pts", f"-{gb_test['reduccion_error_vs_base_pct']}% vs. línea base", delta_color="inverse")
    c4.metric("Umbral de apoyo académico", f"{UMBRAL:.2f} pts", help=resumen["criterio_umbral"])

    st.divider()
    col_g, col_t = st.columns([3, 2])

    with col_g:
        st.subheader("Factores más influyentes en el puntaje")
        imp = pd.Series(resumen["importancia_permutacion_rmse"]).rename(index=NOMBRES_ES).sort_values()
        fig = px.bar(
            x=imp.values, y=imp.index, orientation="h",
            labels={"x": "Aumento del error (RMSE, puntos) al desordenar la variable", "y": ""},
            color=imp.values, color_continuous_scale="Blues",
        )
        fig.update_layout(coloraxis_showscale=False, height=380, margin=dict(l=10, r=10, t=10, b=10))
        st.plotly_chart(fig, width="stretch")
        st.caption("Importancia por permutación sobre el conjunto de prueba. Mayor valor = el modelo depende más de esa variable.")

    with col_t:
        st.subheader("Conclusiones accionables")
        st.markdown(
            f"""
- **La asistencia es el factor dominante** (+{resumen['importancia_permutacion_rmse']['AttendanceRate']:.2f} pts de error al omitirla; correlación r = {resumen['correlaciones_bivariadas']['AttendanceRate']:.3f}).
- **El tiempo de estudio** aporta en menor medida (r = {resumen['correlaciones_bivariadas']['StudyHours']:.3f}).
- **Educación parental, internet y actividades extracurriculares** casi no cambian el promedio (diferencias ≤ 0,04 pts).
- **Prioridad de tutorías:** estudiantes con puntaje estimado bajo **{UMBRAL:.2f} pts** (percentil 25).
- **{gb_test['pct_dentro_10_pts']:.1f}%** de las predicciones queda a ±10 pts del puntaje real.
"""
        )
        st.info(
            "**Limitaciones:** el dataset no incluye una medida directa de bienestar emocional; "
            "correlación no implica causalidad. Se excluyeron Gender y Race (ética) y "
            "TestScore_Reading, TestScore_Science y GPA (fuga de información)."
        )

# ================================================================ 2. SIMULADOR INDIVIDUAL
with tab_sim:
    st.subheader("Simulador de estudiante")
    st.write("Ajusta el perfil del estudiante y el modelo estimará su puntaje en matemáticas en tiempo real.")

    col_in, col_out = st.columns([3, 2])
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

    with col_out:
        gauge = go.Figure(go.Indicator(
            mode="gauge+number", value=pred, number={"suffix": " pts", "valueformat": ".1f"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#1f4e79"},
                "steps": [{"range": [0, UMBRAL], "color": "#f8d7da"}, {"range": [UMBRAL, 100], "color": "#d4edda"}],
                "threshold": {"line": {"color": "red", "width": 3}, "value": UMBRAL},
            },
            title={"text": "Puntaje estimado en matemáticas"},
        ))
        gauge.update_layout(height=280, margin=dict(l=20, r=20, t=50, b=10))
        st.plotly_chart(gauge, width="stretch")
        st.write(f"**Rango probable:** {lo:.1f} – {hi:.1f} pts (± {RMSE_VAL:.2f}, RMSE de validación)")
        if pred < UMBRAL:
            st.error(f"🚨 **Requiere Apoyo Académico** — puntaje estimado bajo el umbral de {UMBRAL:.2f} pts.")
        elif lo < UMBRAL:
            st.warning("⚠️ **Zona de vigilancia** — el rango probable incluye valores bajo el umbral de apoyo.")
        else:
            st.success("✅ **Sin alerta** — el puntaje estimado supera el umbral de apoyo.")

# ================================================================ 3. VISTA TÉCNICA Y LOTE
with tab_tec:
    st.subheader("Comparación de modelos")
    conjunto = st.radio("Conjunto", ["Test", "Validación"], horizontal=True)
    clave = "metricas_test" if conjunto == "Test" else "metricas_validacion"
    filas = []
    for k, v in resumen[clave].items():
        filas.append({
            "Modelo": NOMBRES_MODELOS.get(k, k), "MAE": v["mae"], "RMSE": v["rmse"], "R²": v["r2"],
            "% ±5 pts": v["pct_dentro_5_pts"], "% ±10 pts": v["pct_dentro_10_pts"],
        })
    tabla = pd.DataFrame(filas)
    cg, ct = st.columns([2, 3])
    with cg:
        fig_m = px.bar(tabla, x="Modelo", y="RMSE", text="RMSE", color="Modelo",
                       color_discrete_sequence=["#adb5bd", "#6c9bd2", "#1f4e79"])
        fig_m.update_traces(texttemplate="%{text:.3f}", textposition="outside")
        fig_m.update_layout(showlegend=False, height=330, yaxis_title="RMSE (puntos)", margin=dict(t=20))
        st.plotly_chart(fig_m, width="stretch")
    with ct:
        st.dataframe(tabla.style.format({"MAE": "{:.3f}", "RMSE": "{:.3f}", "R²": "{:.3f}",
                                         "% ±5 pts": "{:.1f}", "% ±10 pts": "{:.1f}"}),
                     hide_index=True, width="stretch")
        gb = resumen["metricas_test"]["gradient_boosting"]
        st.caption(
            f"Gradient Boosting: brecha train/validación {gb['brecha_train_val_pct']}%, sesgo medio {gb['sesgo_medio']} pts "
            f"→ sin sobreajuste. Variables usadas: {', '.join(VARIABLES)}."
        )

    st.divider()
    st.subheader("Predicción por lotes (CSV) y monitoreo de drift")
    st.write(
        f"Columnas requeridas: `{'`, `'.join(VARIABLES)}`. "
        "Si el archivo incluye `TestScore_Math`, se calcula el error real para detectar *drift*."
    )

    archivo = st.file_uploader("Sube un CSV de estudiantes", type="csv")
    ejemplos = sorted(p.name for p in ENTRADAS.glob("*.csv")) if ENTRADAS.exists() else []
    ejemplo = st.selectbox("…o usa un archivo de ejemplo de `entradas/`", ["(ninguno)"] + ejemplos)

    datos = None
    if archivo is not None:
        datos = pd.read_csv(archivo)
    elif ejemplo != "(ninguno)":
        datos = pd.read_csv(ENTRADAS / ejemplo)

    if datos is not None:
        faltan = [c for c in VARIABLES if c not in datos.columns]
        if faltan:
            st.error(f"Faltan columnas en el CSV: {faltan}")
        else:
            p = predecir(datos)
            res = datos.copy()
            res["puntaje_predicho"] = p.round(1)
            res["rango_min"] = np.clip(p - RMSE_VAL, 0, 100).round(1)
            res["rango_max"] = np.clip(p + RMSE_VAL, 0, 100).round(1)
            res["requiere_apoyo"] = p < UMBRAL

            k1, k2, k3 = st.columns(3)
            k1.metric("Estudiantes procesados", f"{len(res):,}".replace(",", "."))
            k2.metric("Requieren apoyo", int(res["requiere_apoyo"].sum()))
            k3.metric("% con alerta", f"{100 * res['requiere_apoyo'].mean():.1f}%")

            if "TestScore_Math" in res.columns:
                real = res["TestScore_Math"].astype(float)
                ok = real.notna().values
                rmse_obs = float(np.sqrt(np.mean((p[ok] - real[ok]) ** 2)))
                mae_obs = float(np.mean(np.abs(p[ok] - real[ok])))
                variacion = 100 * (rmse_obs / RMSE_VAL - 1)
                d1, d2, d3 = st.columns(3)
                d1.metric("RMSE observado", f"{rmse_obs:.2f}", f"{variacion:+.1f}% vs. validación", delta_color="inverse")
                d2.metric("MAE observado", f"{mae_obs:.2f}")
                d3.metric("RMSE de referencia", f"{RMSE_VAL:.2f}")
                if rmse_obs > 1.2 * RMSE_VAL:
                    st.error("🚨 ALERTA DE DRIFT: el error subió más de 20%. Se recomienda reentrenar el modelo.")
                else:
                    st.success("✅ Monitoreo OK: el modelo mantiene su desempeño (error dentro de +20%).")
                fig_s = px.scatter(res.sample(min(len(res), 2000), random_state=0), x="TestScore_Math",
                                   y="puntaje_predicho", opacity=0.4,
                                   labels={"TestScore_Math": "Puntaje real", "puntaje_predicho": "Puntaje predicho"})
                fig_s.add_shape(type="line", x0=0, y0=0, x1=100, y1=100, line=dict(dash="dash", color="red"))
                fig_s.update_layout(height=350)
                st.plotly_chart(fig_s, width="stretch")
            else:
                st.info("El archivo no incluye `TestScore_Math`: no se puede calcular el monitoreo de drift.")

            fig_h = px.histogram(res, x="puntaje_predicho", nbins=30, labels={"puntaje_predicho": "Puntaje predicho"})
            fig_h.add_vline(x=UMBRAL, line_dash="dash", line_color="red", annotation_text="Umbral de apoyo")
            fig_h.update_layout(height=300)
            st.plotly_chart(fig_h, width="stretch")

            st.dataframe(res.head(200), width="stretch")
            st.download_button("⬇️ Descargar predicciones (CSV)", res.to_csv(index=False).encode("utf-8"),
                               file_name="predicciones_lote.csv", mime="text/csv")
