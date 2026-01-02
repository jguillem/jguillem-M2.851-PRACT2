"""
Modulo para la carga de los diferentes datasets
Autores: Jordi Guillem y Xairo Campos
"""

import pandas as pd
from config import Config   


def load_original_dataset():
    """
    Carga el dataset principal desde data/raw/.

    Returns
    -------
    pandas.DataFrame
        DataFrame con los datos originales.
    """
    try:
        df = pd.read_csv(
            Config.ORIGINAL_DATASET_PATH,
            dtype={"post_id": "string"}
        )
        print(f"[OK] Dataset original cargado desde: {Config.ORIGINAL_DATASET_PATH}")
        return df
    except FileNotFoundError:
        print(f"[ERROR] No se encontró el archivo: {Config.ORIGINAL_DATASET_PATH}")
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
        df = pd.read_csv(
            Config.EXTRA_DATASET_PATH,
            dtype={"post_id": "string"}
        )
        print(f"[OK] Dataset extra cargado desde: {Config.EXTRA_DATASET_PATH}")
        return df
    except FileNotFoundError:
        print(f"[ERROR] No se encontró el archivo: {Config.EXTRA_DATASET_PATH}")
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