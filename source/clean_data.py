"""
clean_data.py
---------------------------------------
Funciones de limpieza del dataset:
- Eliminación de duplicados
- Normalización de tipos
- Limpieza de columnas clave
- Manejo básico de valores nulos
"""

import pandas as pd


def clean_basic(df):
    """
    Realiza una limpieza básica del dataset:
    - Elimina duplicados
    - Limpia espacios en columnas string
    - Normaliza tipos de datos comunes

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset original cargado desde raw/

    Returns
    -------
    pandas.DataFrame
        Dataset limpio y preparado para integración
    """

    df = df.copy()

    # -----------------------------------------
    # 1. Eliminar duplicados
    # -----------------------------------------
    before = len(df)
    df = df.drop_duplicates()
    after = len(df)
    print(f"[OK] Duplicados eliminados: {before - after}")

    # -----------------------------------------
    # 2. Limpiar espacios en columnas string
    # -----------------------------------------
    str_cols = df.select_dtypes(include=["object"]).columns
    for col in str_cols:
        df[col] = df[col].astype(str).str.strip()

    print("[OK] Espacios en columnas string limpiados")

    # -----------------------------------------
    # 3. Convertir fechas si existen
    # -----------------------------------------
    if "posted_time" in df.columns:
        df["posted_time"] = pd.to_datetime(df["posted_time"], errors="coerce")
        print("[OK] Columna 'posted_time' convertida a datetime")

    # -----------------------------------------
    # 4. Manejo básico de valores nulos
    # -----------------------------------------
    nulls = df.isna().sum().sum()
    print(f"[INFO] Valores nulos totales: {nulls}")

    return df