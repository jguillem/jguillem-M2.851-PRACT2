"""
Módulo para la detección y visualización de valores extremos (outliers)
mediante el criterio del boxplot (IQR).
Autores: Jordi Guillem y Xairo Campos
"""

import pandas as pd
import matplotlib.pyplot as plt

# Variables numéricas del dataset donde tiene sentido buscar outliers
NUMERIC_OUTLIER_COLS = [
    "karma",
    "upvote_ratio_new",
    "num_comments",
    "sentiment_score"
]


# ============================================================
# 1. DETECCIÓN DE OUTLIERS (IQR)
# ============================================================

def detect_outliers_iqr(df):
    """
    Detecta outliers usando el criterio IQR (boxplot).
    Devuelve un diccionario con los outliers por variable.
    """

    outliers_dict = {}

    for col in NUMERIC_OUTLIER_COLS:
        if col not in df.columns:
            continue

        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        outliers = df[(df[col] < lower) | (df[col] > upper)][col]

        outliers_dict[col] = {
            "lower_bound": lower,
            "upper_bound": upper,
            "outliers": outliers
        }

    return outliers_dict


# ============================================================
# 2. MARCAR OUTLIERS EN EL DATAFRAME
# ============================================================

def mark_outliers(df):
    """
    Añade columnas booleanas indicando si cada fila es outlier
    según el criterio IQR.
    """

    df = df.copy()

    for col in NUMERIC_OUTLIER_COLS:
        if col not in df.columns:
            continue

        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1

        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        df[f"{col}_is_outlier"] = (df[col] < lower) | (df[col] > upper)

    return df


# ============================================================
# 3. PLOTS DE OUTLIERS (BOXPLOT)
# ============================================================

def plot_outliers(df, save=False, folder="plots_outliers"):
    """
    Genera un boxplot por cada variable numérica relevante.
    Si save=True, guarda las imágenes en una carpeta.
    """

    import os
    if save:
        os.makedirs(folder, exist_ok=True)

    for col in NUMERIC_OUTLIER_COLS:
        if col not in df.columns:
            continue

        q1 = df[col].quantile(0.25)
        q3 = df[col].quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr

        plt.figure(figsize=(6, 4))
        plt.boxplot(df[col].dropna(), vert=True)
        plt.title(f"Boxplot de {col}")
        plt.axhline(lower, color="red", linestyle="--", label="Límite inferior")
        plt.axhline(upper, color="red", linestyle="--", label="Límite superior")
        plt.legend()

        if save:
            plt.savefig(f"{folder}/{col}_boxplot.png", dpi=120)

        plt.show()