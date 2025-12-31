"""
utils.py
---------------------------------------
Funciones auxiliares utilizadas en distintos
módulos del proyecto. Incluye validaciones,
comprobaciones y utilidades generales.
"""

import os


def check_columns(df, required_columns):
    """
    Verifica que un DataFrame contiene todas las columnas necesarias.

    Parameters
    ----------
    df : pandas.DataFrame
        DataFrame a comprobar.
    required_columns : list
        Lista de nombres de columnas obligatorias.

    Returns
    -------
    bool
        True si todas las columnas están presentes, False en caso contrario.
    """

    missing = [col for col in required_columns if col not in df.columns]

    if missing:
        print(f"[ERROR] Faltan columnas obligatorias: {missing}")
        return False

    print("[OK] Todas las columnas requeridas están presentes")
    return True


def ensure_directory(path):
    """
    Crea un directorio si no existe.

    Parameters
    ----------
    path : str
        Ruta del directorio.
    """

    if not os.path.exists(path):
        os.makedirs(path)
        print(f"[OK] Directorio creado: {path}")
    else:
        print(f"[INFO] Directorio ya existente: {path}")


def print_separator(text=None):
    """
    Imprime una línea separadora. Si se proporciona texto,
    lo muestra entre dos líneas para mayor claridad.
    """
    print("\n" + "-" * 60)
    if text:
        print(text)
        print("-" * 60)
    else:
        print("-" * 60)


# ---------------------------------------------------------
# NUEVA FUNCIÓN: RESUMEN DEL DATASET
# ---------------------------------------------------------

def summarize_dataframe(df, title="RESUMEN DEL DATASET"):
    """
    Muestra un resumen completo del DataFrame:
    - Tipos de datos
    - Información general
    - Estadísticos descriptivos numéricos
    - Estadísticos descriptivos categóricos (si existen)
    - Rangos de valores numéricos
    """

    print_separator(title)

    print("\nTipos de datos:")
    print(df.dtypes)

    print("\nInformación general:")
    df.info()

    print("\nEstadísticos descriptivos (numéricos):")
    print(df.describe())

    print("\nEstadísticos descriptivos (categóricos):")
    categorical_cols = df.select_dtypes(include='category').columns
    if len(categorical_cols) > 0:
        print(df.describe(include='category'))
    else:
        print("[INFO] No hay columnas categóricas en este dataset.")

    print("\nRangos de valores por variable numérica:")
    for col in df.select_dtypes(include=["int64", "float64"]):
        print(f"{col}: min={df[col].min()}, max={df[col].max()}")