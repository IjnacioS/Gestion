# Automatización: predice el puntaje de matemáticas para un CSV de estudiantes.
# Uso:  python src/automatizacion_matematicas.py --entrada entradas/nuevos_estudiantes.csv

import argparse, json, sys, warnings
from datetime import datetime
from pathlib import Path
import numpy as np
import pandas as pd
import joblib

warnings.filterwarnings("ignore", category=UserWarning)

ROOT_DIR = Path(__file__).resolve().parent.parent

def main():
    parser = argparse.ArgumentParser(description="Predicción automatizada de rendimiento en matemáticas (SCY1102)")
    parser.add_argument("--entrada", required=True, help="Ruta al archivo CSV con los datos de los estudiantes")
    parser.add_argument("--salida", default=str(ROOT_DIR / "salidas"), help="Carpeta de destino para los resultados")
    parser.add_argument("--modelo", default=str(ROOT_DIR / "models" / "modelo_matematicas.joblib"), help="Ruta al modelo entrenado")
    parser.add_argument("--metadatos", default=str(ROOT_DIR / "models" / "metadatos.json"), help="Ruta al archivo de metadatos")
    parser.add_argument("--log", default=str(ROOT_DIR / "registro.log"), help="Ruta al archivo de log")
    args = parser.parse_args()

    ruta_modelo = Path(args.modelo)
    ruta_meta = Path(args.metadatos)

    if not ruta_modelo.exists():
        print(f"ERROR: No se encuentra el modelo en {ruta_modelo}")
        sys.exit(1)
    if not ruta_meta.exists():
        print(f"ERROR: No se encuentran los metadatos en {ruta_meta}")
        sys.exit(1)

    modelo = joblib.load(ruta_modelo)
    meta = json.loads(ruta_meta.read_text(encoding="utf-8"))
    variables = meta["variables"]

    ruta_entrada = Path(args.entrada)
    if not ruta_entrada.exists():
        print(f"ERROR: No se encuentra el archivo de entrada: {ruta_entrada}")
        sys.exit(1)

    datos = pd.read_csv(ruta_entrada)
    faltan = [c for c in variables if c not in datos.columns]
    if faltan:
        print("ERROR: faltan columnas requeridas en el CSV:", faltan)
        sys.exit(1)

    X = datos[variables].copy()
    X["ParentalEducation"] = X["ParentalEducation"].astype(object)
    if X.isnull().any().any():
        print("AVISO: hay valores faltantes; el modelo los rellena con los valores aprendidos en entrenamiento.")

    pred = np.clip(modelo.predict(X), 0, 100)
    resultado = datos.copy()
    resultado["puntaje_predicho"] = pred.round(1)
    resultado["rango_min"] = np.clip(pred - meta["rmse_validacion"], 0, 100).round(1)
    resultado["rango_max"] = np.clip(pred + meta["rmse_validacion"], 0, 100).round(1)
    resultado["requiere_apoyo"] = pred < meta["umbral_apoyo"]

    carpeta_salida = Path(args.salida)
    carpeta_salida.mkdir(parents=True, exist_ok=True)
    nombre = "predicciones_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv"
    ruta_guardado = carpeta_salida / nombre
    resultado.to_csv(ruta_guardado, index=False)
    print(f"{len(resultado)} estudiantes procesados exitosamente. Resultado guardado en: {ruta_guardado}")
    print(f"Estudiantes con requerimiento de apoyo académico (predicho < {meta['umbral_apoyo']:.2f} pts): {int(resultado['requiere_apoyo'].sum())}")

    # Monitoreo de drift: solo si el archivo trae el puntaje real
    if "TestScore_Math" in datos.columns:
        real = datos["TestScore_Math"].astype(float)
        ok = real.notna()
        rmse = float(np.sqrt(np.mean((pred[ok.values] - real[ok]) ** 2)))
        print(f"Monitoreo de desempeño: RMSE observado = {rmse:.2f} (referencia validación = {meta['rmse_validacion']:.2f})")
        if rmse > 1.2 * meta["rmse_validacion"]:
            print("ALERTA: El error subió más del 20% respecto a validación. Se recomienda reentrenar o recalibrar el modelo.")
        else:
            print("Monitoreo OK: El desempeño del modelo se mantiene dentro del rango esperado.")

    try:
        ruta_log = Path(args.log)
        ruta_log.parent.mkdir(parents=True, exist_ok=True)
        with open(ruta_log, "a", encoding="utf-8") as f:
            f.write(f"{datetime.now().isoformat()} | {args.entrada} | {len(resultado)} filas | apoyo: {int(resultado['requiere_apoyo'].sum())}\n")
    except Exception as e:
        print(f"Aviso: no se pudo escribir en el log ({e})")

if __name__ == "__main__":
    main()
