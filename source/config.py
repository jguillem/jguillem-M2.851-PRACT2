# ---------------------------------------------------------
# Configuración global del proyecto
# ---------------------------------------------------------

# Carpeta donde se encuentran los datos originales
RAW_DATA_DIR = "data/raw/"

# Carpeta donde se guardarán los resultados finales
OUTPUT_DATA_DIR = "output/"

# Nombre de los datasets originales
ORIGINAL_DATASET = "reddit_datascience_dataset.csv"
EXTRA_DATASET = "reddit_datascience_extradata.csv"

# Rutas completas (útiles para load_data.py)
ORIGINAL_DATASET_PATH = RAW_DATA_DIR + ORIGINAL_DATASET
EXTRA_DATASET_PATH = RAW_DATA_DIR + EXTRA_DATASET

# Nombre del archivo final procesado
CLEAN_OUTPUT_FILENAME = "reddit_datascience_clean.csv"