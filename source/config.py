"""
Configuración del scraper
Autores: Jordi Guillem y Xairo Campos
"""


class Config:
    # aquí va toda la config del scraper
    
    # ========== CONFIG DEL SITIO ==========
    
    SUBREDDIT = "datascience"
    # usamos old.reddit porque es más fácil de scrapear
    USE_OLD_REDDIT = True
    BASE_URL = f"https://{'old' if USE_OLD_REDDIT else 'www'}.reddit.com/r/{SUBREDDIT}/"
    
    
    # ========== CONFIG DEL SCRAPING ==========
    
    # cuántos posts queremos? None = todos los que haya
    MAX_POSTS = None  
    
    # tiempo entre scrolls (segundos) para no saturar el servidor
    SCROLL_DELAY = 2
    
    # tiempo max de espera para que cargue algo
    TIMEOUT = 2
    
    # después de cuántos scrolls sin nuevos posts paramos
    MAX_SCROLLS_WITHOUT_NEW_POSTS = 2
    
    # pausas random para parecer humano
    MIN_ACTION_DELAY = 1.5  
    MAX_ACTION_DELAY = 3
    
    
    # ========== CONFIG DEL NAVEGADOR ==========
    
    # user agent para identificarnos
    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36 "
        "WebScraperBot/1.0 (Educational Purpose; UOC University)"
    )
    
    # modo sin ventana
    HEADLESS = False  # poner True para ejecución sin ventana
    
    
    # ========== SALIDA DE DATOS ==========
    
    # donde guardamos el csv (ruta absoluta para evitar errores)
    import os
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    OUTPUT_FILE = os.path.join(BASE_DIR, "dataset", f"{'old_' if USE_OLD_REDDIT else ''}reddit_datascience_dataset.csv")
    
    CSV_ENCODING = "utf-8"
    CSV_DELIMITER = ","
    
    
    # ========== ANÁLISIS DE SENTIMIENTO ==========
    
    # reddit es en inglés
    SENTIMENT_LANGUAGE = "en"
    
    
    # ========== LOGS ==========
    
    # mostrar info extra mientras corre
    VERBOSE = True
    
    # cada cuántos posts mostramos progreso
    PROGRESS_REPORT_FREQUENCY = 10
