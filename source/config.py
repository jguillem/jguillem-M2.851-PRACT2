"""
Configuración del pipeline de limpieza y análisis
Autores: Jordi Guillem y Xairo Campos
"""

import os

class Config:

    # ========== BASE DEL PROYECTO ==========

    # Carpeta raíz del proyecto (un nivel por encima de /source)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # ========== DIRECTORIOS DE DATOS ==========

    RAW_DATA_DIR = os.path.join(BASE_DIR, "data", "raw")
    OUTPUT_DATA_DIR = os.path.join(BASE_DIR, "output")

    # ========== ARCHIVOS ORIGINALES ==========

    ORIGINAL_DATASET = "reddit_datascience_dataset.csv"
    EXTRA_DATASET = "reddit_datascience_extradata.csv"

    ORIGINAL_DATASET_PATH = os.path.join(RAW_DATA_DIR, ORIGINAL_DATASET)
    EXTRA_DATASET_PATH = os.path.join(RAW_DATA_DIR, EXTRA_DATASET)

    # ========== ARCHIVO FINAL ==========

    CLEAN_OUTPUT_FILENAME = "reddit_datascience_clean.csv"
    CLEAN_OUTPUT_PATH = os.path.join(OUTPUT_DATA_DIR, CLEAN_OUTPUT_FILENAME)