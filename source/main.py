"""
main.py
---------------------------------------
Pipeline completo de procesamiento de datos:

1. Carga de datasets
2. Limpieza básica
3. Integración de datasets
4. Resumen del dataset integrado
5. Limpieza avanzada
6. Feature engineering
7. Selección de columnas finales
8. Guardado del dataset procesado
"""

import pandas as pd

from load_data import load_original_dataset, load_extra_dataset
from clean_data import clean_basic
from integrate_data import merge_datasets
from clean_after_integration import clean_dataset
from feature_engineering import apply_feature_engineering
from select_columns import select_final_columns
from utils import ensure_directory, print_separator, summarize_dataframe
from config import OUTPUT_DATA_DIR, CLEAN_OUTPUT_FILENAME


def main():
    print_separator("INICIANDO PIPELINE DE PROCESAMIENTO DE DATOS")

    # ---------------------------------------------------------
    # 1. CARGA DE DATOS
    # ---------------------------------------------------------
    print_separator("1. Cargando datasets")

    df_main = load_original_dataset()
    df_extra = load_extra_dataset()

    print(f"Dataset original: {df_main.shape}")
    print(f"Dataset extra: {df_extra.shape}")

    # ---------------------------------------------------------
    # 2. LIMPIEZA BÁSICA
    # ---------------------------------------------------------
    print_separator("2. Limpieza básica del dataset original")

    df_main = clean_basic(df_main)

    # ---------------------------------------------------------
    # 3. INTEGRACIÓN DE DATOS
    # ---------------------------------------------------------
    print_separator("3. Integrando datasets")

    df_merged = merge_datasets(df_main, df_extra)
    print(f"Dataset integrado: {df_merged.shape}")

    # Exclusión del subreddit y de otra variable
    if "subreddit" in df_merged.columns:
        df_merged = df_merged[df_merged["subreddit"] != "datascience"]

    df_merged = df_merged.drop(columns=["otra_variable"], errors="ignore")

    # ---------------------------------------------------------
    # RESUMEN DEL DATASET TRAS LA INTEGRACIÓN Y FILTRADO
    # ---------------------------------------------------------
    summarize_dataframe(df_merged, "RESUMEN TRAS INTEGRACIÓN Y FILTRADO")

    # ---------------------------------------------------------
    # 4. LIMPIEZA AVANZADA
    # ---------------------------------------------------------
    print_separator("4. Limpieza avanzada")

    df_clean = clean_dataset(df_merged)
    print(f"Dataset limpio: {df_clean.shape}")

    # ---------------------------------------------------------
    # 5. FEATURE ENGINEERING
    # ---------------------------------------------------------
    print_separator("5. Feature engineering")

    df_features = apply_feature_engineering(df_clean)
    print(f"Dataset con features: {df_features.shape}")

    # ---------------------------------------------------------
    # 6. SELECCIÓN DE COLUMNAS FINALES
    # ---------------------------------------------------------
    print_separator("6. Selección de columnas finales")

    df_final = select_final_columns(df_features)
    print(f"Dataset final: {df_final.shape}")

    # ---------------------------------------------------------
    # 7. GUARDADO DEL RESULTADO
    # ---------------------------------------------------------
    print_separator("7. Guardando dataset final")

    ensure_directory(OUTPUT_DATA_DIR)

    output_path = f"{OUTPUT_DATA_DIR}/{CLEAN_OUTPUT_FILENAME}"
    df_final.to_csv(output_path, index=False)

    print(f"Archivo guardado en: {output_path}")
    print_separator("PIPELINE COMPLETADO")


if __name__ == "__main__":
    main()