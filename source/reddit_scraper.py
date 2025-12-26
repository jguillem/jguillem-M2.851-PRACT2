"""
Scraper principal de Reddit con Selenium
Autores: Jordi Guillem y Xairo Campos
"""

import time
import random
import csv
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException, StaleElementReferenceException
from post_extractor import PostExtractor
from sentiment_analyzer import SentimentAnalyzer


class RedditScraper:
    
    def __init__(self, config, username=None, password=None):
        # aquí guardamos todo
        self.config = config
        self.data = []  # los posts extraídos van aquí
        self.processed_post_ids = set()  # para evitar duplicados
        self.username = username
        self.password = password
        
        # inicializar todo
        self.driver = self._initialize_driver()
        self.post_extractor = PostExtractor(self.driver, config)
        self.sentiment_analyzer = SentimentAnalyzer()

        if self.username and self.password:
            self.login(self.username, self.password)
        else:
            if self.config.VERBOSE:
                print("[!] No se detectaron credenciales. Ejecutando sin login")
        
        print("[✓] Scraper inicializado correctamente")
    
    def login(self, username, password):
        # ir directamente a la pantalla de login
        self.driver.get("https://old.reddit.com/login")

        # se espera a que cargue el formulario
        WebDriverWait(self.driver, self.config.TIMEOUT).until(
            EC.presence_of_element_located((By.ID, "login-username"))
        )

        # rellenar usuario y contraseña
        self.driver.find_element(By.ID, "login-username").send_keys(username)
        self.driver.find_element(By.ID, "login-password").send_keys(password)
        login_button = WebDriverWait(self.driver, self.config.TIMEOUT).until(
            EC.element_to_be_clickable((By.XPATH, "//button[.//span[contains(text(), 'Iniciar sesión')]]"))
            )
        login_button.click()

        try:
            WebDriverWait(self.driver, self.config.TIMEOUT).until(
                EC.presence_of_element_located((By.CLASS_NAME, "user"))
                )
            self.logged_in = True
            if self.config.VERBOSE:
                print("[✓] Login exitoso como:", username)
        except:
            self.logged_in = False
            print("[!] Login fallido o no detectado. Continuando sin sesión.")
         

    def _initialize_driver(self):
        # configurar Chrome para que no detecten que es un bot
        print("[*] Inicializando navegador Chrome...")
        
        options = Options()
        
        # user-agent realista
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36')
        
        # modo headless si queremos
        if self.config.HEADLESS:
            options.add_argument('--headless=new')
        
        # cosas para evitar detección
        options.add_argument("--lang=en-US")
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-notifications')
        options.add_argument('--disable-popup-blocking')
        options.add_argument('--start-maximized')
        options.add_argument('--disable-web-security')
        options.add_argument('--disable-features=IsolateOrigins,site-per-process')
        
        # preferencias extra
        prefs = {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.default_content_setting_values.notifications": 2
        }
        options.add_experimental_option("prefs", prefs)
        
        # más trucos anti-detección
        options.add_experimental_option("excludeSwitches", ["enable-automation", "enable-logging"])
        options.add_experimental_option('useAutomationExtension', False)
        
        driver = webdriver.Chrome(options=options)
        
        # scripts para que no detecten selenium
        driver.execute_cdp_cmd('Network.setUserAgentOverride', {
            "userAgent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36'
        })
        
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        driver.execute_script("Object.defineProperty(navigator, 'plugins', {get: () => [1, 2, 3, 4, 5]})")
        driver.execute_script("Object.defineProperty(navigator, 'languages', {get: () => ['en-US', 'en']})")
        
        return driver
    
    
    def _random_delay(self, min_delay=None, max_delay=None):
        # pausa random para simular humano
        if min_delay is None:
            min_delay = self.config.MIN_ACTION_DELAY
        if max_delay is None:
            max_delay = self.config.MAX_ACTION_DELAY
            
        delay = random.uniform(min_delay, max_delay)
        time.sleep(delay)
    
    
    def _scroll_down(self):
        # hacer scroll gradual, como si fuera una persona
        current_position = self.driver.execute_script("return window.pageYOffset;")
        target_position = self.driver.execute_script("return document.body.scrollHeight;")
        
        # scroll en pedazos
        scroll_increment = (target_position - current_position) / 5
        for i in range(5):
            new_position = current_position + (scroll_increment * (i + 1))
            self.driver.execute_script(f"window.scrollTo(0, {new_position});")
            time.sleep(0.2)
        
        # esperar a que cargue más contenido
        time.sleep(self.config.SCROLL_DELAY)
    
    
    def _accept_cookies_if_present(self):
        # intentar aceptar cookies si sale el banner
        try:
            cookie_selectors = [
                "button[aria-label='Accept']",
                "button[id*='accept']",
                "button[class*='accept']",
                "button:contains('Accept')",
                "button:contains('I Accept')"
            ]
            
            for selector in cookie_selectors:
                try:
                    cookie_button = WebDriverWait(self.driver, 2).until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, selector))
                    )
                    cookie_button.click()
                    print("[✓] Banner de cookies aceptado")
                    time.sleep(1)
                    return
                except:
                    continue
                    
        except Exception as e:
            pass  # no pasa nada si no hay cookies
    
    
    def _get_visible_posts(self):
        # conseguir todos los posts que se ven en la página ahora
        try:
            # reddit usa diferentes estructuras según versión
            selectors = [
                "shreddit-post",
                "article",
                "div[id^='t3_']",  # old reddit
                "div.Post",
                "div.thing",
                "[data-testid='post-container']",
            ]
            
            for selector in selectors:
                try:
                    posts = self.driver.find_elements(By.CSS_SELECTOR, selector)

                    # evita posts patrocinados, anuncios y avisos
                    posts = [
                        post for post in posts
                        if not any(keyword in post.get_attribute("outerHTML").lower()
                                for keyword in ["patrocinado", "automoderator"])
                    ]                    

                    if posts and len(posts) > 0:
                        if self.config.VERBOSE:
                            print(f"[i] Usando selector: {selector} ({len(posts)} posts encontrados)")
                        return posts
                except:
                    continue
            
            # si nada funciona, probar xpath
            try:
                posts = self.driver.find_elements(By.XPATH, "//shreddit-post | //div[contains(@class, 'Post')] | //div[@id[starts-with(., 't3_')]]")

                # evita posts patrocinados, anuncios y avisos
                posts = [
                        post for post in posts
                        if not any(keyword in post.get_attribute("outerHTML").lower()
                                for keyword in ["patrocinado", "automoderator"])
                ]

                if posts and len(posts) > 0:
                    if self.config.VERBOSE:
                        print(f"[i] Usando XPath ({len(posts)} posts encontrados)")
                    return posts
            except:
                pass
            
            return []
            
        except Exception as e:
            print(f"[!] Error al obtener posts visibles: {str(e)}")
            return []
    
    
    def _click_next_page(self):
        # hacer clic en "next" para ir a la siguiente página
        try:
            # buscar el botón next con xpath (es más confiable)
            try:
                next_button = self.driver.find_element(By.XPATH, "//span[@class='next-button']/a | //span[@class='nextprev']/a[contains(text(), 'next')]")
                if next_button and next_button.is_displayed():
                    href = next_button.get_attribute('href')
                    if href:
                        if self.config.VERBOSE:
                            print(f"[i] Navegando a la siguiente página...")
                        
                        self.driver.get(href)
                        time.sleep(self.config.SCROLL_DELAY + 1)
                        return True
            except:
                pass
            
            # si no funciona xpath, probar con css
            next_selectors = [
                'span.next-button a',
                '.nav-buttons .nextprev a[rel*="next"]',
                'p.nextprev a:last-child',
            ]
            
            for selector in next_selectors:
                try:
                    next_button = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if next_button and next_button.is_displayed():
                        text = next_button.text.lower()
                        if 'next' in text or '›' in text:
                            href = next_button.get_attribute('href')
                            if href:
                                if self.config.VERBOSE:
                                    print(f"[i] Navegando a la siguiente página...")
                                
                                self.driver.get(href)
                                time.sleep(self.config.SCROLL_DELAY + 1)
                                return True
                except:
                    continue
            
            if self.config.VERBOSE:
                print("[!] No se encontró botón 'next' - fin de páginas")
            return False
            
        except Exception as e:
            if self.config.VERBOSE:
                print(f"[!] Error al buscar botón 'next': {str(e)}")
            return False
    
    
    def scrape(self):
        print(f"\n[*] Navegando a {self.config.BASE_URL}...")
        self.driver.get(self.config.BASE_URL)

        time.sleep(3)
        self._accept_cookies_if_present()
        self._random_delay(2, 3)

        print("[*] Iniciando extracción de posts...\n")

        posts_extracted = 0
        pages_scraped = 0
        pages_without_new_posts = 0

        while True:
            if self.config.MAX_POSTS and posts_extracted >= self.config.MAX_POSTS:
                print(f"\n[✓] Se alcanzó el límite de {self.config.MAX_POSTS} posts")
                break

            posts_in_this_page = 0

            # Guardar URL REAL del feed antes de procesar posts
            self.current_feed_url = self.driver.current_url

            # 🔥 Obtener posts visibles (DOM fresco)
            visible_posts = self._get_visible_posts()

            if not visible_posts:
                print("[!] No se encontraron posts en la página")
                break

            if self.config.VERBOSE:
                print(f"[i] Página {pages_scraped + 1}: {len(visible_posts)} posts encontrados")

            # 🔥 Extraer URLs de los posts visibles (NO elementos)
            post_urls = []
            for post in visible_posts:
                try:
                    if self.config.USE_OLD_REDDIT:
                        link = post.find_element(By.CSS_SELECTOR, 'a[href*="/comments/"]').get_attribute("href")
                    else:
                        link = post.get_attribute("permalink")
                        link = "https://www.reddit.com" + link if link else None

                    if link and "/comments/" in link and link not in self.processed_post_ids:
                        post_urls.append(link)

                except Exception:
                    continue

            # 🔥 Procesar cada URL sin stale elements
            for post_url in post_urls:
                try:
                    if self.config.VERBOSE:
                        print(f"[→] Procesando post {posts_extracted + 1}: {post_url}")

                    self.driver.get(post_url)

                    wait = WebDriverWait(self.driver, self.config.TIMEOUT)

                    if self.config.USE_OLD_REDDIT:
                        full_post = wait.until(
                            EC.presence_of_element_located((By.CSS_SELECTOR, 'div#siteTable'))
                        )
                        post_data = self.post_extractor.extract_post_data(
                            full_post.find_element(By.CSS_SELECTOR, 'div.thing')
                        )
                    else:
                        full_post = wait.until(
                            EC.presence_of_element_located(
                                (By.CSS_SELECTOR, 'shreddit-post, div[data-testid="post-content"]')
                            )
                        )
                        post_data = self.post_extractor.extract_post_data(full_post)

                    # 🔥 Evitar repeticiones
                    post_id = post_data.get("post_id", post_url)
                    if post_id in self.processed_post_ids:
                        continue

                    # Análisis de sentimiento
                    text_for_sentiment = f"{post_data['title']} {post_data.get('text_content', '')}"
                    sentiment_scores = self.sentiment_analyzer.analyze(text_for_sentiment)

                    post_data['sentiment'] = sentiment_scores['compound_label']
                    post_data['sentiment_score'] = sentiment_scores['compound']
                    post_data['sentiment_positive'] = sentiment_scores['pos']
                    post_data['sentiment_negative'] = sentiment_scores['neg']
                    post_data['sentiment_neutral'] = sentiment_scores['neu']

                    post_data['scraped_at'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                    # Guardar
                    self.data.append(post_data)
                    self.processed_post_ids.add(post_id)

                    posts_extracted += 1
                    posts_in_this_page += 1

                    if posts_extracted % self.config.PROGRESS_REPORT_FREQUENCY == 0:
                        print(f"[✓] Posts extraídos: {posts_extracted}")

                    # 🔧 Reiniciar ChromeDriver cada 50 posts
                    if posts_extracted % 50 == 0:
                        print("[i] Reiniciando ChromeDriver para evitar inestabilidad...")

                        current_url = self.current_feed_url

                        try:
                            self.driver.quit()
                        except:
                            pass

                        self.driver = self._initialize_driver()
                        self.driver.get(current_url)
                        time.sleep(2)

                except Exception as e:
                    print(f"[!] Error procesando {post_url}: {e}")
                    continue

            # 🔥 Volver SIEMPRE al feed REAL antes de avanzar página
            self.driver.get(self.current_feed_url)
            time.sleep(1)

            pages_scraped += 1

            if posts_in_this_page == 0:
                pages_without_new_posts += 1
                if pages_without_new_posts >= 3:
                    print(f"\n[i] No se encontraron nuevos posts en {pages_without_new_posts} páginas")
                    print("[i] Finalizando scraping...")
                    break
            else:
                pages_without_new_posts = 0

            # Avanzar página
            if self.config.USE_OLD_REDDIT:
                if not self._click_next_page():
                    print("\n[i] No hay más páginas disponibles")
                    break
                self._random_delay(2, 3)
            else:
                self._scroll_down()
                self._random_delay()

        print(f"\n[✓] Extracción finalizada. Total de posts: {len(self.data)}")
        print(f"[✓] Páginas procesadas: {pages_scraped}")
    
    def save_to_csv(self):
        # guardar todo en un csv
        if not self.data:
            print("[!] No hay datos para guardar")
            return
        
        print(f"\n[*] Guardando {len(self.data)} posts en {self.config.OUTPUT_FILE}...")
        
        try:
            # conseguir todas las columnas posibles
            fieldnames = []
            for post in self.data:
                for key in post.keys():
                    if key not in fieldnames:
                        fieldnames.append(key)
            
            # ordenar campos de forma lógica
            preferred_order = [
                'title', 'author', 'subreddit', 'karma', 'upvote_ratio',
                'num_comments', 'flair', 'content_type', 'text_content',
                'media_url', 'external_url', 'posted_time', 'posted_hour',
                'sentiment', 'sentiment_score', 'sentiment_positive',
                'sentiment_negative', 'sentiment_neutral', 'scraped_at', 'post_id'
            ]
            
            ordered_fieldnames = [f for f in preferred_order if f in fieldnames]
            remaining_fields = [f for f in fieldnames if f not in ordered_fieldnames]
            fieldnames = ordered_fieldnames + remaining_fields
            
            # escribir csv
            with open(self.config.OUTPUT_FILE, 'w', newline='', encoding=self.config.CSV_ENCODING) as csvfile:
                writer = csv.DictWriter(
                    csvfile,
                    fieldnames=fieldnames,
                    delimiter=self.config.CSV_DELIMITER,
                    quoting=csv.QUOTE_MINIMAL
                )
                
                writer.writeheader()
                writer.writerows(self.data)
            
            print(f"[✓] Dataset guardado exitosamente en: {self.config.OUTPUT_FILE}")
            print(f"[✓] Total de registros: {len(self.data)}")
            
        except Exception as e:
            print(f"[✗] Error al guardar CSV: {str(e)}")
            raise
    
    
    def close(self):
        # cerrar el navegador cuando terminamos
        if hasattr(self, 'driver'):
            try:
                self.driver.quit()
                print("\n[✓] Navegador cerrado")
            except Exception as e:
                print(f"[!] Error al cerrar navegador: {str(e)}")
