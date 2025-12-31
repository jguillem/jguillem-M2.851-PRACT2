"""
load_data.py
---------------------------------------
Módulo encargado de cargar los datasets
originales desde la carpeta raw/.

Utiliza las rutas definidas en config.py
para mantener el código limpio y centralizado.
"""

import pandas as pd
from config import (
    ORIGINAL_DATASET_PATH,
    EXTRA_DATASET_PATH
)


def load_original_dataset():
    """
    Carga el dataset principal desde data/raw/.

    Returns
    -------
    pandas.DataFrame
        DataFrame con los datos originales.
    """
    try:
        df = pd.read_csv(ORIGINAL_DATASET_PATH)
        print(f"[OK] Dataset original cargado desde: {ORIGINAL_DATASET_PATH}")
        return df
    except FileNotFoundError:
        print(f"[ERROR] No se encontró el archivo: {ORIGINAL_DATASET_PATH}")
        raise


def load_extra_dataset():
    """
    Carga el dataset adicional (por ejemplo, upvote_ratio_new)
    desde data/raw/.

    Returns
    -------
    pandas.DataFrame
        DataFrame con los datos adicionales.
    """
    try:
        df = pd.read_csv(EXTRA_DATASET_PATH)
        print(f"[OK] Dataset extra cargado desde: {EXTRA_DATASET_PATH}")
        return df
    except FileNotFoundError:
        print(f"[ERROR] No se encontró el archivo: {EXTRA_DATASET_PATH}")
        raise


def load_all():
    """
    Carga ambos datasets y los devuelve juntos.

    Returns
    -------
    tuple(DataFrame, DataFrame)
        (dataset_original, dataset_extra)
    """
    df_original = load_original_dataset()
    df_extra = load_extra_dataset()
    return df_original, df_extra