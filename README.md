# Reddit Scraper - r/datascience

**Autores:** Jordi Guillem y Xairo Campos  
**Asignatura:** M2.851 - Tipología y ciclo de vida de los datos  
**Práctica:** 2 - Data Cleaning  
**Universidad:** UOC  
**Fecha:** Octubre 2025

---

## Descripción

Proyecto para la realización de la limpieza del dataset obtenido en la practiva 1 de la asignatura.


---

## Estructura del proyecto

```
M2.851-PRACT1/
├── dataset/
│   ├── old_reddit_datascience_dataset.csv    # Dataset generado por el scraper
|        
│
├── source/
│   ├── analyze_dataset.py                # Script para analizar el dataset generado
├── .git/                                 # Control de versiones
├── .gitignore                            # Archivos ignorados por git
├── M2.851_20251_Practica2.pdf            # Enunciado de la práctica
├── README.md                             # Este archivo
└── requirements.txt                      # Dependencias del proyecto
```

---

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

Esto instalará:

---

## Uso

### 1. Ejecutar el scraper

Copiar el archivo .env.example del proyecto y renombrar a .env indicando las credenciales.
Funciona con usuario nativo de reddit

Desde el directorio raíz del proyecto:

```bash
cd source
python main.py
```

El analizador:
1. Abrirá el dataset

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

---

## Datos extraídos

Cada fila del CSV representa un post con los siguientes campos:

### Metadatos básicos:
- **`post_id`**: ID único del post en Reddit
- **`title`**: Título del post
- **`author`**: Nombre de usuario del autor
- **`subreddit`**: Subreddit de origen (siempre "datascience" en este caso)

### Engagement:
- **`karma`**: Puntos del post (upvotes - downvotes)
- **`upvote_ratio`**: Ratio de upvotes (0-1)
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
- Reddit puede cambiar su estructura HTML en cualquier momento
- Compatibilidad parcial con reddit moderno

---

## Contacto

**Jordi Guillem** | **Xairo Campos**  
Universidad Oberta de Catalunya (UOC)  
M2.851 - Tipología y ciclo de vida de los datos  
Práctica 1 - Web Scraping  
Octubre 2025
