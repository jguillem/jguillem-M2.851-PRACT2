# Reddit Scraper - r/datascience

**Autores:** Jordi Guillem y Xairo Campos  
**Asignatura:** M2.851 - Tipología y ciclo de vida de los datos  
**Práctica:** 2 - Data Cleaning  
**Universidad:** UOC  
**Fecha:** Diciembre 2025

---

## Descripción

Proyecto para la realización de la limpieza del dataset obtenido en la practiva 1 de la asignatura.

El dataset contiene los últimos posts del subreddit datascience que tiene como descripción "A space for data science professionals to engage in discussions and debates on the subject of data science." Su análisis puede ser importante por tratarse de un foro conocido y abierto sobre ciencia de datos y podría permitir identificar temas relevantes del área. 

---

## Estructura del proyecto

```
M2.851-PRACT2/
├── data
│   ├── processed
│   ├── raw
│   │   ├── reddit_datascience_dataset.csv      # Dataset principal
│   │   ├── reddit_datascience_extradata.csv    # Dataset con datos de upvote y permalink
├── output
│   ├── reddit_datascience_clean.csv            # Dataset con la vase de limpieza aplicada
├── source
│   ├── analyze_dataset.py                      # Script para analizar el dataset generado
│   ├── clean_after_integration.py              # Módulo para la imputación de datos faltantes y tipificación
│   ├── config.py                               # Configuración del pipeline de limpieza y análisis
│   ├── integrate_data.py                       # Modulo para la integración de los diferentes datasets
│   ├── load_data.py                            # Modulo para la carga de los diferentes datasets
│   ├── main.py                                 # Script principal
│   ├── select_columns.py                       # Modulo para la selección de los campos
│   ├── utils.py                                # Funciones auxiliares
├── .gitignore
├── M2.851_20251_Práctica2.pdf                  # Enunciado de la práctica
├── README.md                                   # Este archivo
├── requirements.txt                            # Dependencias del proyecto

```

## Instalación

### Requisitos previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### Definición del entorno virutal e Instalar dependencias

```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Esto instalará las librerías:

- pandas
- numpy

## Uso

### 1. Ejecutar el pipeline de integración, limpieza y análisis

Para ejecutar el script principal de integración, limpieza y análisis 

```bash
cd source
python main.py
```

Saldrá por el prompt de comandos los diferentes pasos del pipeline del proyecto:

1. Cargando datasets
2. Limpieza básica del dataset original
3. Integrando datasets
RESUMEN TRAS INTEGRACIÓN Y FILTRADO
4. Limpieza avanzada
5. Selección de columnas finales
6. Guardando dataset limpio

### 2. Analizar el dataset generado

Una vez generado el dataset:

```bash
cd source
python analyze_dataset.py
```

Este script mostrará:
- Total de posts extraídos
- Estadísticas de karma y comentarios
- Distribución de sentimientos
- Tipos de contenido
- Autores más activos
- Flairs más comunes
- Top posts con más engagement

---

## Configuración


### Parámetros principales:

- **`OUTPUT_FILE`**: Ruta del archivo CSV de salida
- **`ORIGINAL_DATASET`**: Nombre del archivo csv del dataset principal 
- **`EXTRA_DATASET`**: Nombre del archivo csv del dataset con datos adicionales
- **`CLEAN_OUTPUT_FILENAME`**: Nombre del archivo csv de los datos limpios del pipeline
---

## Resumen de las consideraciones de limpieza

| Campo              | Imputación                                   | Resumen                                           |
|--------------------|-----------------------------------------------|---------------------------------------------------|
| title              | "untitled"                                    | Título desconocido o vacío                        |
| author             | "unknown"                                     | Autor no disponible                               |
| karma              | Media redondeada                              | Mantiene distribución original                    |
| upvote_ratio_new   | Media redondeada                              | Evita sesgos por valores faltantes                |
| num_comments       | 0                                             | Sin comentarios registrados                       |
| flair              | "no flair"                                    | Publicación sin etiqueta                          |
| content_type       | "text" si hay contenido, si no "unknown"      | Inferido a partir de text_content                 |
| text_content       | "no content"                                  | No hay texto disponible                           |
| media_url          | "no media url"                                | No contiene medios                                |
| external_url       | "no external url"                             | No enlaza a recursos externos                     |
| posted_time        | 1970-01-01                                    | Fecha técnica para evitar NaT                     |
| posted_hour        | -1                                            | Hora desconocida                                  |
| sentiment          | "neutral"                                     | Valor por defecto                                 |
| sentiment_score    | 0                                             | Sentimiento neutral                               |
| sentiment_positive | 0                                             | Normalización posterior                           |
| sentiment_negative | 0                                             | Normalización posterior                           |
| sentiment_neutral  | 1                                             | Normalización posterior                           |
| scraped_at         | 1970-01-01                                    | Fecha técnica si falta                            |
| post_id            | "no post id"                                  | Identificador ausente                             |
| permalink          | URL generada                                  | https://old.reddit.com/r/datascience/<post_id_sin_prefijo> |)

---

## Tecnologías utilizadas

- **Pandas**: Procesamiento y análisis de datos
- **Python 3**: Lenguaje de programación

---


## Contacto

**Jordi Guillem** | **Xairo Campos**  
Universidad Oberta de Catalunya (UOC)  
M2.851 - Tipología y ciclo de vida de los datos  
Práctica 2 - Data Cleaning
Diciembre 2025
