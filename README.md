# Predicción del Rendimiento Académico en Matemáticas

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)
![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.2%2B-F7931E?logo=scikitlearn&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2.0%2B-150458?logo=pandas&logoColor=white)
![Status](https://img.shields.io/badge/Estado-Completado-success)

## Contexto del Proyecto (Caso 1: Educación)

En una institución de educación secundaria, el equipo de gestión académica ha identificado una creciente preocupación por los bajos resultados obtenidos en las evaluaciones de matemáticas. Las autoridades buscan comprender los factores que influyen en el desempeño estudiantil —tales como características sociodemográficas, hábitos de estudio, bienestar emocional, antecedentes familiares y acceso a recursos educativos— con el objetivo de contar con insumos basados en datos que permitan diseñar estrategias más eficaces de acompañamiento académico.

Este repositorio contiene la etapa de **modelado predictivo (Machine Learning)** que da continuidad al Análisis Exploratorio de Datos (EDA) realizado previamente sobre este caso.

---

## Objetivo Técnico

Desarrollar, evaluar y automatizar un modelo de **regresión supervisada** capaz de predecir el puntaje continuo en matemáticas (`TestScore_Math`, en una escala de 0 a 100) a partir de 20 variables explicativas del perfil del estudiante.

> **Nota metodológica:** Se abordó como un problema de regresión continua (y no de clasificación) para evitar imponer umbrales arbitrarios de rendimiento ("bajo / medio / alto") sin un criterio institucional previo.

---

## Estructura del Repositorio

```text
ML_Matematicas/
│
├── data/
│   └── raw/                  # Archivos de datos (train.csv, validation.csv, test.csv)
├── models/                   # Modelos entrenados serializados (.joblib) y artefactos de automatización
├── notebooks/
│   └── ml_matematicas.ipynb  # Notebook principal con el flujo completo de 8 pasos
├── .gitignore                # Exclusión de archivos pesados, entornos virtuales y caché[cite: 1]
├── README.md                 # Documentación del proyecto[cite: 1]
└── requirements.txt          # Dependencias y librerías necesarias[cite: 1, 2]
