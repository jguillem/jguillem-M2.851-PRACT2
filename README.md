# Reddit Scraper - r/datascience

**Autores:** Jordi Guillem y Xairo Campos  
**Asignatura:** M2.851 - Tipología y ciclo de vida de los datos  
**Práctica:** 1 - Web Scraping  
**Universidad:** UOC  
**Fecha:** Octubre 2025

---

## Descripción

Proyecto de web scraping para extraer posts del subreddit r/datascience de Reddit. El scraper utiliza Selenium para navegar por las páginas, extrae metadatos completos de cada post y realiza análisis de sentimiento automático usando VADER.

El objetivo es generar un dataset estructurado con información sobre posts de data science, que incluye engagement (karma, comentarios), tipos de contenido, y análisis de sentimiento del título y texto.

---

## Estructura del proyecto

```
M2.851-PRACT1/
├── dataset/
│   ├── .gitkeep
│   ├── reddit_datascience_dataset.csv    # Dataset generado por el scraper
|   └── zenodo                            # Carpeta con el README de zenodo
|        
│
├── source/
│   ├── .gitkeep
│   ├── main.py                           # Script principal - ejecutar desde aquí
│   ├── config.py                         # Configuración del scraper
│   ├── reddit_scraper.py                 # Lógica principal del scraping
│   ├── post_extractor.py                 # Extrae datos individuales de cada post
│   ├── sentiment_analyzer.py             # Análisis de sentimiento con VADER
│   ├── analyze_dataset.py                # Script para analizar el dataset generado
│   └── __pycache__/                      # Archivos compilados de Python
│
├── .env.example                          # Ejemplo de configuración de las credenciales
├── .git/                                 # Control de versiones
├── .gitignore                            # Archivos ignorados por git
├── M2.851_20251_Practica1.pdf            # Enunciado de la práctica
├── README.md                             # Este archivo
└── requirements.txt                      # Dependencias del proyecto
```

---

## Instalación

### Requisitos previos
- Python 3.8 o superior
- Chrome o Chromium instalado
- pip (gestor de paquetes de Python)

### Definición del entorno virutal e Instalar dependencias

```bash
python -m venv env
source env/bin/activate
pip install -r requirements.txt
```

Esto instalará:
- **selenium** - Para automatización del navegador
- **webdriver-manager** - Gestión automática del driver de Chrome
- **vaderSentiment** - Análisis de sentimiento
- **pandas** - Procesamiento de datos
- **python-dateutil** - Manejo de fechas

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

El scraper:
1. Abrirá Chrome (o en modo headless si está configurado)
   1. Si el proceso de login funciona correctamente se verá la pantalla de login
2. Navegará a old.reddit.com/r/datascience
3. Extraerá posts página por página
4. Guardará el progreso automáticamente

**Para detener el scraper:** Presiona `Ctrl+C` y guardará automáticamente el progreso hasta ese momento.

### 2. Uso con login de usuario

Aunque la aplicación hace el scraping de datos públicos, es posible arrancarla con login de usuario para evitar detecciones
Solamente funciona con usuario nativo de la plataforma Reddit. No funciona con login de Google o Apple

Pasos:

 1. Renombrar el archivo .env.example a .env 
 2. Indicar usuario y contraseña de reddit
 3. Ejecutar el script principal main.py

REDDIT_USER=
REDDIT_PASS=


### 3. Analizar el dataset generado

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

Editar `source/config.py` para personalizar el comportamiento:

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

### Ejemplo de configuración para pruebas rápidas:

```python
MAX_POSTS = 50           # Solo 50 posts
HEADLESS = True          # Sin ventana
SCROLL_DELAY = 1         # Más rápido (¡cuidado con saturar el servidor!)
```

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

- **Selenium WebDriver**: Automatización del navegador web
- **Chrome/Chromium**: Navegador para el scraping
- **VADER Sentiment**: Análisis de sentimiento optimizado para redes sociales
- **Pandas**: Procesamiento y análisis de datos
- **Python 3**: Lenguaje de programación

---

## Consideraciones importantes

### Aspectos éticos y legales:
- [o] Uso de old.reddit.com que es más ligero y accesible
- [o] Delays entre peticiones para no saturar los servidores
- [o] User-Agent identificable con propósito educativo
- [!] Solo para uso académico/educativo
- [!] Respetar los términos de servicio de Reddit

### Técnicas anti-detección:
- User-Agent personalizado identificando propósito educativo
- Delays aleatorios entre acciones
- Scroll gradual para simular comportamiento humano
- Scripts JavaScript para ocultar flags de automatización
- Espera de carga completa de la página en la versión moderna

### Limitaciones:
- El ratio de upvotes no siempre está disponible en el listado
- Timestamps pueden estar en formato relativo ("2 hours ago")
- Reddit puede cambiar su estructura HTML en cualquier momento
- Compatibilidad parcial con reddit moderno

---

## Notas adicionales

- El scraper usa **old.reddit.com** por defecto porque:
  - Es más ligero y rápido
  - Estructura HTML más simple y estable
  - Menos JavaScript dinámico
  - Navegación por páginas más predecible

- **Interrupción segura**: Al presionar `Ctrl+C`, el scraper:
  1. Captura la señal de interrupción
  2. Guarda todos los datos extraídos hasta ese momento
  3. Cierra el navegador correctamente
  4. Termina sin perder datos

- **Duplicados**: El scraper mantiene un registro de IDs procesados para evitar duplicados en una misma ejecución

- **VADER Sentiment**: Especialmente diseñado para textos cortos de redes sociales, considera:
  - Emoticonos y emojis
  - Capitalización (MAYÚSCULAS = énfasis)
  - Signos de puntuación (!!!)
  - Palabras de argot

---

## Troubleshooting

### Extracción en Reddit Moderno
- Esta aplicación tiene compatibilidad limitada para el reddit moderno 
- Los posts se abren en pestañas pero la interrupción del programa con Crl + C genera algunos mensajes de error en modo VERBOSE
- Por defecto Reddit moderno detecta el idioma de instalación del navegador, aún que en el archivo .config se haya definido el inglés
- Si se cambia rápidamente la opción de autotraducción el idioma rápidamente en el icono superior derecho

### El navegador no se abre
- Verificar que Chrome/Chromium está instalado
- Probar con `HEADLESS = False` en config.py

### "Import selenium could not be resolved"
```bash
pip install -r requirements.txt
```

### El scraper no encuentra posts
- Reddit puede haber cambiado su estructura HTML
- Verificar que old.reddit.com está accesible
- Revisar los selectores en `post_extractor.py`

### Muy lento
- Reducir `SCROLL_DELAY` en config.py (¡con cuidado!)
- Usar `HEADLESS = True`

### El dataset está vacío
- Verificar que el scraper encontró posts durante la ejecución
- Revisar errores en la consola
- Comprobar permisos de escritura en la carpeta `dataset/`

---

## Contacto

**Jordi Guillem** | **Xairo Campos**  
Universidad Oberta de Catalunya (UOC)  
M2.851 - Tipología y ciclo de vida de los datos  
Práctica 1 - Web Scraping  
Octubre 2025
