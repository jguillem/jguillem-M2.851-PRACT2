"""
Script principal para scrapear Reddit
Autores: Jordi Guillem y Xairo Campos
UOC - M2.851 - Tipología y ciclo de vida de los datos
Práctica 1 - Web Scraping
Noviembre 2025
"""

import os
import sys
import signal
from reddit_scraper import RedditScraper
from config import Config
from dotenv import load_dotenv



def signal_handler(signum, frame):
    # esto es para cuando presiones Ctrl+C que guarde antes de cerrar
    print("\n\n[!] Interrupción detectada. Guardando progreso...")
    if 'scraper' in globals():
        scraper.save_to_csv()
    print("[✓] Dataset guardado correctamente.")
    sys.exit(0)


def main():
    # aquí arranca todo
    signal.signal(signal.SIGINT, signal_handler)
    
    config = Config()
    
    print("=" * 80)
    print("REDDIT WEB SCRAPER - r/datascience")
    print("=" * 80)
    print(f"\n[i] Configuración:")
    print(f"    - Subreddit: {config.SUBREDDIT}")
    print(f"    - Max posts: {config.MAX_POSTS if config.MAX_POSTS else 'Ilimitado'}")
    print(f"    - Delay entre scrolls: {config.SCROLL_DELAY}s")
    print(f"    - Output: {config.OUTPUT_FILE}")
    print(f"\n[i] Presiona Ctrl+C en cualquier momento para detener y guardar.")
    print("=" * 80 + "\n")
    
    # carga del archivo .env con los datos de contraseña 
    load_dotenv()
    REDDIT_USER = os.getenv("REDDIT_USER")
    REDDIT_PASS = os.getenv("REDDIT_PASS")

    # crear el scraper
    global scraper
    scraper = RedditScraper(config, username=REDDIT_USER, password=REDDIT_PASS)
    
    try:
        # ejecutar el scraping
        scraper.scrape()
        
        # guardar cuando termine
        scraper.save_to_csv()
        
        print("\n" + "=" * 80)
        print("[✓] Scraping completado exitosamente")
        print(f"[✓] Dataset guardado en: {config.OUTPUT_FILE}")
        print("=" * 80)
        
    except Exception as e:
        print(f"\n[✗] Error durante el scraping: {str(e)}")
        print("[!] Intentando guardar el progreso...")
        scraper.save_to_csv()
        sys.exit(1)
    
    finally:
        # cerrar el navegador
        scraper.close()


if __name__ == "__main__":
    main()
