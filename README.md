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

- Carga de los datasets presentes en data/raw

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

- **`SUBREDDIT`**: Subreddit a scrapear (por defecto: "datascience")
- **`USE_OLD_REDDIT`**: True para usar old.reddit.com (recomendado)
- **`MAX_POSTS`**: Límite de posts a extraer
  - `None` = sin límite (extrae todo lo disponible)
  - Número entero = límite específico
- **`SCROLL_DELAY`**: Segundos entre cada scroll/navegación (por defecto: 2)
- **`HEADLESS`**: 
  - `False` = muestra el navegador (útil para ver el progreso)
  - `True` = ejecución sin ventana
- **`VERBOSE`**: Mostrar información detallada durante la ejecución
- **`OUTPUT_FILE`**: Ruta del archivo CSV de salida


- **`ORIGINAL_DATASET`**: Nombre del archivo csv del dataset principal 
- **`EXTRA_DATASET`**: Nombre del archivo csv del dataset con datos adicionales
- **`CLEAN_OUTPUT_FILENAME`**: Nombre del archivo csv de los datos limpios del pipeline

---

## Datos extraídos

Cada fila del CSV representa un post con los siguientes campos:

### Metadatos básicos:
- **`post_id`**: ID único del post en Reddit
- **`title`**: Título del post
- **`author`**: Nombre de usuario del autor
- **`subreddit`**: Subreddit de origen (siempre "datascience" en este caso)
- **`permalink`**: URL del post

### Engagement:
- **`karma`**: Puntos del post (upvotes - downvotes)
- **`upvote_ratio`**: Porcentaje de upvotes (0-100)
- **`num_comments`**: Número de comentarios

### Clasificación:
- **`flair`**: Etiqueta/categoría del post (si tiene)
- **`content_type`**: Tipo de contenido:
  - `text` - Post de texto
  - `image` - Contiene imagen
  - `video` - Contiene video
  - `link` - Link a sitio externo

### Contenido:
- **`text_content`**: Texto del post (primeros 500 caracteres)
- **`media_url`**: URL de imagen/video (si aplica)
- **`external_url`**: URL externa (si aplica)

### Temporal:
- **`posted_time`**: Fecha y hora de publicación
- **`posted_hour`**: Hora del día (0-23)
- **`scraped_at`**: Timestamp de cuando se extrajo

### Análisis de sentimiento (VADER):
- **`sentiment`**: Clasificación categórica
  - `positive` - Sentimiento positivo
  - `negative` - Sentimiento negativo
  - `neutral` - Sentimiento neutral
- **`sentiment_score`**: Score compuesto (-1 a 1)
- **`sentiment_positive`**: Score positivo (0-1)
- **`sentiment_negative`**: Score negativo (0-1)
- **`sentiment_neutral`**: Score neutral (0-1)

---

## Tecnologías utilizadas

- **Pandas**: Procesamiento y análisis de datos
- **Python 3**: Lenguaje de programación

---

## Consideraciones importantes

### Aspectos éticos y legales:

### Limitaciones:
- El ratio de upvotes no siempre está disponible en el listado
- Timestamps pueden estar en formato relativo ("2 hours ago")
---

## Contacto

**Jordi Guillem** | **Xairo Campos**  
Universidad Oberta de Catalunya (UOC)  
M2.851 - Tipología y ciclo de vida de los datos  
Práctica 2 - Data Cleaning
Diciembre 2025
