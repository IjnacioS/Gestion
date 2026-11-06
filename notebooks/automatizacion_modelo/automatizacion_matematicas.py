# Automatización: predice el puntaje de matemáticas para un CSV de estudiantes.
# Uso:  python automatizacion_matematicas.py --entrada entradas/nuevos.csv

import argparse, json, sys
from datetime import datetime
from pathlib import Path
import numpy as np
import pandas as pd
import joblib

CARPETA = Path(__file__).parent

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--entrada", required=True, help="CSV con los estudiantes")
    parser.add_argument("--salida", default=str(CARPETA / "salidas"), help="Carpeta de resultados")
    args = parser.parse_args()

    modelo = joblib.load(CARPETA / "modelo_matematicas.joblib")
    meta = json.loads((CARPETA / "metadatos.json").read_text(encoding="utf-8"))
    variables = meta["variables"]

    datos = pd.read_csv(args.entrada)
    faltan = [c for c in variables if c not in datos.columns]
    if faltan:
        print("ERROR: faltan columnas en el CSV:", faltan)
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

    Path(args.salida).mkdir(parents=True, exist_ok=True)
    nombre = "predicciones_" + datetime.now().strftime("%Y%m%d_%H%M%S") + ".csv"
    ruta = Path(args.salida) / nombre
    resultado.to_csv(ruta, index=False)
    print(f"{len(resultado)} estudiantes procesados. Resultado: {ruta}")
    print(f"Estudiantes marcados para apoyo (predicho < {meta['umbral_apoyo']:.1f}): {int(resultado['requiere_apoyo'].sum())}")

    # Monitoreo: solo si el archivo trae el puntaje real
    if "TestScore_Math" in datos.columns:
        real = datos["TestScore_Math"].astype(float)
        ok = real.notna()
        rmse = float(np.sqrt(np.mean((pred[ok.values] - real[ok]) ** 2)))
        print(f"Monitoreo: RMSE en estos datos = {rmse:.2f} (referencia en validación = {meta['rmse_validacion']:.2f})")
        if rmse > 1.2 * meta["rmse_validacion"]:
            print("ALERTA: el error subió más de 20%. Conviene reentrenar el modelo.")
        else:
            print("Monitoreo OK: el modelo mantiene su desempeño.")

    with open(CARPETA / "registro.log", "a", encoding="utf-8") as f:
        f.write(f"{datetime.now().isoformat()} | {args.entrada} | {len(resultado)} filas\n")

if __name__ == "__main__":
    main()
