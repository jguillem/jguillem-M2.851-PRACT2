# Reddit Scraper - r/datascience

**Autores:** Jordi Guillem y Xairo Campos  
**Asignatura:** M2.851 - Tipología y ciclo de vida de los datos  
**Práctica:** 2 - Data Cleaning  
**Universidad:** UOC  
**Fecha:** Diciembre 2025

---

## Descripción

Proyecto completo de análisis de datos sobre posts del subreddit r/datascience. El proyecto incluye:

1. **Práctica 1:** Web scraping de posts del subreddit
2. **Práctica 2:** Limpieza, integración y preparación de datos
3. **Análisis avanzado:** Modelado supervisado, no supervisado y contraste de hipótesis

El dataset contiene posts del subreddit r/datascience: "A space for data science professionals to engage in discussions and debates on the subject of data science." El análisis identifica patrones de engagement, características de posts exitosos y clusters temáticos. 

---

## Estructura del proyecto

```
M2.851-PRACT2/
├── data
│   ├── processed
│   ├── raw
│   │   ├── reddit_datascience_dataset.csv      # Dataset principal (960 posts)
│   │   ├── reddit_datascience_extradata.csv    # Dataset con datos de upvote y permalink
├── output
│   ├── reddit_datascience_clean.csv            # Dataset limpio y procesado (960 posts × 24 vars)
├── source
│   ├── analyze_dataset.py                      # Script para analizar el dataset generado
│   ├── clean_after_integration.py              # Módulo para la imputación de datos faltantes y tipificación
│   ├── config.py                               # Configuración del pipeline de limpieza y análisis
│   ├── integrate_data.py                       # Módulo para la integración de los diferentes datasets
│   ├── load_data.py                            # Módulo para la carga de los diferentes datasets
│   ├── main.py                                 # Script principal de limpieza
│   ├── outliers.py                             # Detección y marcado de outliers (IQR)
│   ├── select_columns.py                       # Módulo para la selección de los campos
│   ├── utils.py                                # Funciones auxiliares
├── analisis_reddit_datascience.ipynb           # 📊 NOTEBOOK DE ANÁLISIS COMPLETO
├── .gitignore
├── M2.851_20251_Práctica2.pdf                  # Enunciado de la práctica
├── memoria.txt                                 # Enlace a Google Drive con documentación adicional
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

- **pandas**: Manipulación y análisis de datos
- **numpy**: Computación numérica
- **matplotlib**: Visualización de datos (gráficos)
- **seaborn**: Visualización estadística avanzada
- **scikit-learn**: Machine learning (Random Forest, K-Means, PCA, métricas)
- **scipy**: Tests estadísticos (Shapiro-Wilk, Levene, t-test, Mann-Whitney)

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

### 3. Ejecutar el notebook de análisis completo

El archivo **`analisis_reddit_datascience.ipynb`** contiene el análisis completo del proyecto:

**Contenido del notebook:**

1. **Descripción del Dataset:** Contexto, variables y motivación del estudio
2. **Integración y Selección:** Resumen del proceso de preparación de datos
3. **Limpieza de Datos:** Verificación de imputación, tipificación y gestión de outliers
4. **Análisis de Datos:**
   - **Modelo Supervisado (Random Forest):** Clasificación de posts de alto engagement
   - **Modelo No Supervisado (K-Means):** Clustering de posts por características
   - **Contraste de Hipótesis:** Test estadístico sobre sentimiento vs engagement
5. **Visualizaciones:** Gráficos de distribuciones, correlaciones, ROC, clusters, etc.
6. **Conclusiones:** Interpretación de resultados y resolución del problema

**Para ejecutar el notebook:**

```bash
# Instalar Jupyter si no lo tienes
pip install jupyter

# Lanzar Jupyter Notebook
jupyter notebook analisis_reddit_datascience.ipynb
```

O abrir directamente el archivo `.ipynb` en **VS Code** con la extensión de Jupyter instalada.

**Características destacadas del análisis:**
- ✅ Modelos de machine learning supervisado y no supervisado
- ✅ Verificación de supuestos estadísticos (normalidad, homocedasticidad)
- ✅ Visualizaciones profesionales con matplotlib y seaborn
- ✅ Interpretaciones detalladas de cada resultado
- ✅ Código ejecutable y reproducible

**Resultados principales obtenidos:**

📊 **Modelo Supervisado (Random Forest):**
- Accuracy: 91.67%
- ROC-AUC: 0.9816
- Top predictor: número de comentarios (44.28% importancia)
- Segundo predictor: upvote ratio (39.20% importancia)

🔍 **Modelo No Supervisado (K-Means):**
- 4 clusters identificados
- Cluster 0: Posts de bajo engagement controversial (138 posts)
- Cluster 1: Posts estándar positivos (507 posts)
- Cluster 2: Posts con sentimiento negativo/neutral (287 posts)
- Cluster 3: Posts virales (28 posts, karma promedio: 1429.71)

📈 **Contraste de Hipótesis (Mann-Whitney U):**
- p-value: 0.017779 (< 0.05)
- Decisión: Se rechaza H₀
- Conclusión: Existe diferencia estadísticamente significativa en el karma entre posts positivos y no-positivos
- Tamaño del efecto: -0.1636 (efecto pequeño)

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

- **Python 3.8+**: Lenguaje de programación
- **Pandas**: Procesamiento y análisis de datos
- **NumPy**: Computación numérica
- **Matplotlib & Seaborn**: Visualización de datos
- **Scikit-learn**: Machine learning (Random Forest, K-Means, métricas)
- **SciPy**: Tests estadísticos (Shapiro-Wilk, Levene, t-test, Mann-Whitney)
- **Jupyter Notebook**: Análisis interactivo y documentación

---


## Contacto

**Jordi Guillem** | **Xairo Campos**  
Universidad Oberta de Catalunya (UOC)  
M2.851 - Tipología y ciclo de vida de los datos  
Práctica 2 - Data Cleaning
Diciembre 2025
