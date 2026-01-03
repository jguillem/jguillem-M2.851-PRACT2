"""
Script principal
Autores: Jordi Guillem y Xairo Campos
UOC - M2.851 - Tipología y ciclo de vida de los datos
Práctica 2 - Limpieza de datos
Diciembre 2025
""" 

import pandas as pd
from utils import clean_basic, ensure_directory, print_separator, summarize_dataframe
from config import Config  
from load_data import load_original_dataset, load_extra_dataset
from integrate_data import merge_datasets
from clean_after_integration import clean_dataset
from select_columns import select_final_columns
from outliers import detect_outliers_iqr, mark_outliers, plot_outliers


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

    coinciden = set(df_extra["post_id"]) & set(df_main["post_id"])
    print("Coincidencias:", len(coinciden))

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

    print("Filas después del merge:", df_merged.shape[0])
    print("Coincidencias en post_id:", df_merged["upvote_ratio_new"].notna().sum())

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
    # 4B. DETECCIÓN DE OUTLIERS (IQR)
    # ---------------------------------------------------------
    print_separator("4B. Detección de outliers (IQR)")

    outliers = detect_outliers_iqr(df_clean)
    print("\nCantidad de outliers por atributo:")
    for col, info in outliers.items():
        print(f" - {col}: {len(info['outliers'])}")



    # Añadir columnas marcando outliers
    df_clean = mark_outliers(df_clean)

    # Mostrar plots por pantalla
    plot_outliers(df_clean)


    # ---------------------------------------------------------
    # 5. SELECCIÓN DE COLUMNAS FINALES
    # ---------------------------------------------------------
    print_separator("5. Selección de columnas finales")

    df_final = select_final_columns(df_clean)
    print(f"Dataset final: {df_final.shape}")

    # ---------------------------------------------------------
    # 6. GUARDADO DEL RESULTADO
    # ---------------------------------------------------------
    print_separator("6. Guardando dataset limpio")

    ensure_directory(Config.OUTPUT_DATA_DIR)

    output_path = Config.CLEAN_OUTPUT_PATH
    df_final.to_csv(output_path, index=False)

    print(f"Archivo guardado en: {output_path}")
    print_separator("PIPELINE COMPLETADO")

    print("Duplicados en df_main:", df_main["post_id"].duplicated().sum())
    print("Duplicados en df_extra:", df_extra["post_id"].duplicated().sum())
    print("Duplicados en df_final:", df_final["post_id"].duplicated().sum())





if __name__ == "__main__":
    main()