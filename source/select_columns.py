"""
Modulo para la selección de los campos
Autores: Jordi Guillem y Xairo Campos
"""

def select_final_columns(df):
    """
    Selecciona las columnas finales del dataset.

    Parameters
    ----------
    df : pandas.DataFrame
        Dataset integrado.

    Returns
    -------
    pandas.DataFrame
        Dataset con las columnas seleccionadas.
    """

    # Columnas que quieres eliminar
    columns_to_drop = [
        "upvote_ratio",   # columna original con datos identicos al karma y que no aportan valor
        "subreddit"       # columna que indica el nombre del subreddit. Como estamos trabajando con solamente un subreddit, tampoco aporta valor.
    ]

    # Eliminar solo si existen (evita errores)
    df = df.drop(columns=[c for c in columns_to_drop if c in df.columns])

    print("[OK] Columnas eliminadas:", columns_to_drop)

    return df