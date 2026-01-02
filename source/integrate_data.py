"""
Modulo para la integración de los diferentes datasets
Autores: Jordi Guillem y Xairo Campos
"""

import pandas as pd


def merge_datasets(df_main, df_extra):
    """
    Integra el dataset principal con el dataset extra
    usando la columna post_id como clave.

    Además:
    - Elimina la columna original 'upvote_ratio'
    - Inserta 'upvote_ratio_new' en la misma posición
      donde estaba 'upvote_ratio'

    Parameters
    ----------
    df_main : pandas.DataFrame
        Dataset original.
    df_extra : pandas.DataFrame
        Dataset extra con la columna upvote_ratio_new.

    Returns
    -------
    pandas.DataFrame
        Dataset integrado y con la nueva columna colocada
        en la posición correcta.
    """

    # ---------------------------------------------------------
    # 1. Merge por post_id
    # ---------------------------------------------------------
    df = pd.merge(df_main, df_extra, on="post_id", how="left")

    # ---------------------------------------------------------
    # 2. Guardar la posición original de upvote_ratio
    # ---------------------------------------------------------
    if "upvote_ratio" in df.columns:
        original_pos = df.columns.get_loc("upvote_ratio")
    else:
        original_pos = None

    # ---------------------------------------------------------
    # 3. Eliminar la columna antigua
    # ---------------------------------------------------------
    df = df.drop(columns=["upvote_ratio"], errors="ignore")

    # ---------------------------------------------------------
    # 4. Insertar la nueva columna en la misma posición
    # ---------------------------------------------------------
    if original_pos is not None and "upvote_ratio_new" in df.columns:
        cols = list(df.columns)
        # Sacamos la columna nueva de donde esté
        cols.insert(original_pos, cols.pop(cols.index("upvote_ratio_new")))
        df = df[cols]

    print("[OK] Integración completada: upvote_ratio_new colocado en la posición original")

    return df