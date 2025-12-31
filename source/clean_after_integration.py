"""
clean_after_integration.py
---------------------------------------
Limpieza avanzada después de integrar datasets:
- Tratamiento de valores faltantes
- Conversión de tipos
"""

import pandas as pd


def clean_dataset(df):
    """
    Limpieza avanzada del dataset integrado.
    """

    # ---------------------------------------------------------
    # 1. TRATAMIENTO DE VALORES FALTANTES
    # ---------------------------------------------------------

    # upvote_ratio_new: porcentaje (0-100)
    if "upvote_ratio_new" in df.columns:

        # valores válidos (no NaN)
        valid_values = df["upvote_ratio_new"].dropna()

        if len(valid_values) > 0:
            mean_ratio = round(valid_values.mean())
        else:
            # si toda la columna está vacía, usar 0 como valor seguro
            mean_ratio = 0

        # rellenar NaN
        df["upvote_ratio_new"] = df["upvote_ratio_new"].fillna(mean_ratio)

        # convertir a entero (ya sin NaN)
        df["upvote_ratio_new"] = df["upvote_ratio_new"].astype(int)

    else:
        print("[WARN] La columna 'upvote_ratio_new' no existe en este dataset.")

    # Columnas enteras
    int_columns = ["num_comments", "karma", "score"]
    for col in int_columns:
        if col in df.columns:
            df[col] = df[col].fillna(0).astype(int)

    # ---------------------------------------------------------
    # 2. CONVERSIÓN DE TIPOS
    # ---------------------------------------------------------

    # Convertir categorías
    categorical_cols = ["flair", "content_type"]
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].astype("category")

    # Convertir fechas
    if "created_utc" in df.columns:
        df["created_utc"] = pd.to_datetime(df["created_utc"], errors="coerce")

    # Convertir post_id a string
    if "post_id" in df.columns:
        df["post_id"] = df["post_id"].astype(str)

    return df