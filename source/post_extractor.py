"""
Extractor de datos de posts individuales
Autores: Jordi Guillem y Xairo Campos
"""

import re
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from urllib.parse import urlparse, parse_qs, unquote
import unicodedata



class PostExtractor:
    # clase para sacar los datos de cada post
    
    def __init__(self, driver, config):
        self.driver = driver
        self.config = config
    

    # intenta limpiar caracters raros
    def _clean_mojibake(self,text: str) -> str:
        if not text:
            return ""

        # Intenta re-decodificar los casos donde UTF-8 se trató como Latin-1
        try:
            text = text.encode("latin1").decode("utf-8")
        except Exception:
            pass

        # Si todavía hay artefactos, aplica corrección manual de los casos más comunes
        replacements = {
            "â€™": "'",
            "â€˜": "'",
            "â€œ": "“",
            "â€": "”",
            "â€“": "-   ",
            "â€”": "—",
            "â€¦": "…",
            "ŌĆÖ": "'",
            "ŌĆ£": "“",
            "ŌĆØ": "”",
            "Â": "",
        }
        for bad, good in replacements.items():
            text = text.replace(bad, good)

        # Normaliza Unicode (acentos, guiones, comillas inteligentes)
        text = unicodedata.normalize("NFKC", text)

        return text.strip()

    def _clean_and_normalize_text(self,text):
        if not text:
            return ""
        try:
            text = text.encode('latin1').decode('utf-8')
        except Exception:
            pass
        import unicodedata
        return unicodedata.normalize("NFKC", text)
    
        
    def _safe_get_element_text(self, element, selector, attribute=None):
        try:
            target = element.find_element(By.CSS_SELECTOR, selector)
            text = target.get_attribute(attribute) if attribute else target.text
            return self._clean_mojibake(text)
        except NoSuchElementException:
            return ''
        except Exception:
            return ''
        

    # para links de imagenes, externos y de video hace falta que busque más elementos
    def _safe_get_element_media(self, element, selector, attribute=None):
        list_urls = []
        try:            
            target = element.find_elements(By.CSS_SELECTOR, selector)
            for e in target:               
                if attribute:
                    if e.get_attribute(attribute):
                        list_urls.append(e.get_attribute(attribute))
                        return list_urls or ''
            if not list_urls: return ''
        except NoSuchElementException:
            return []
        except Exception:
            return []
        
        
    def _extract_post_id(self, post_element):
        # conseguir el ID del post
        try:
            # probar diferentes sitios donde puede estar el ID
            post_id = post_element.get_attribute('id')
            if post_id:
                return post_id
            
            post_id = post_element.get_attribute('data-post-id')
            if post_id:
                return post_id
            
            # intentar sacarlo del permalink
            permalink = self._safe_get_element_text(post_element, 'a[data-click-id="comments"]', 'href')
            if permalink:
                match = re.search(r'/comments/([a-z0-9]+)/', permalink)
                if match:
                    return match.group(1)
            
            return ''
        except:
            return ''
    
    
    def _extract_title(self, post_element):
        # sacar el título
        selectors = [
            'a.title',  # old reddit
            'p.title a.title',
            'h3',  # new reddit
            'div[slot="title"]',
            'a[data-click-id="body"]',
            '[data-testid="post-title"]'
             # --- Reddit moderno ---
            '[data-testid="post-title"]',
            'h1[slot="title"]',
            'h1[id^="post-title-"]',
            'shreddit-post h1[slot="title"]',
            'shreddit-post h1[id^="post-title-"]',
        ]
        
        for selector in selectors:
            title = self._safe_get_element_text(post_element, selector)
            if title:                
                return title.strip()
        
        return 'N/A'
    
    
    def _extract_author(self, post_element):
        # sacar quien lo publicó
        selectors = [
            'a.author',
            'a[slot="author"]',
            'a[href*="/user/"]',
            '[data-testid="post-author"]'
        ]
        
        for selector in selectors:
            author = self._safe_get_element_text(post_element, selector)
            if author:
                # quitar el u/ si tiene
                author = author.replace('u/', '').strip()
                if author:
                    return author
        
        return 'Unknown'
    
    
    def _extract_karma(self, post_element):
        # sacar los puntos del post
        selectors = [
            'div.score.unvoted',
            'div.score',
            'faceplate-number[slot="score"]',
            '[data-testid="post-score"]',
            'div[slot="score"]'
        ]
        
        for selector in selectors:
            karma_text = self._safe_get_element_text(post_element, selector)
            if karma_text and karma_text != '•':
                # limpiar (puede venir como "1.2k" o "5.0k votes")
                karma_cleaned = re.sub(r'[^\d.k-]', '', karma_text.lower())
                try:
                    if 'k' in karma_cleaned:
                        return int(float(karma_cleaned.replace('k', '')) * 1000)
                    return int(float(karma_cleaned))
                except ValueError:
                    continue
        
        return 0
    

    def _extract_upvote_ratio(self, post_element):
        # Intentar primero con nuevo Reddit
        ratio_text = self._safe_get_element_text(post_element, '[data-testid="upvote-ratio"]')
        if ratio_text:
            match = re.search(r'(\d+)%', ratio_text)
            if match:
                return float(match.group(1)) / 100.0

        # Intentar con old Reddit — no hay ratio, así que devolvemos None o un flag
        score_text = self._safe_get_element_text(post_element, 'div.score.unvoted', attribute='title')
        if score_text:
            try:
                return int(score_text)  # es el score, no ratio
            except:
                pass

        return 0.0
    
    def _extract_upvote_count_new(self, post_element):    
        try:
            # Obtener el atributo 'score' directamente
            value = post_element.get_attribute("score")
            if not value:
                return 0

            # Normalizar valor
            value = value.replace(",", "").lower()
            if value.isdigit():
                return int(value)
            elif "k" in value:
                return int(float(value.replace("k", "")) * 1000)
            elif "m" in value:
                return int(float(value.replace("m", "")) * 1_000_000)
            else:
                return int(value)

        except Exception as e:
            print(f"Error extrayendo score: {e}")
            pass

        return 0.0
        


    def _extract_num_comments(self, post_element):
        """
        Extrae el número de comentarios de un post en:
        - old.reddit
        - reddit moderno (www.reddit.com)
        - reddit redesign (faceplate)
        - vista móvil / compacta

        Soporta:
        - NBSP (\xa0)
        - "184 comments"
        - "184 comments" (NBSP)
        - "1,234 comments"
        - "1.2k comments"
        - "1.1M comments"
        - "View all 184 comments"
        - "184 comments • 97% Upvoted"
        - "Comments (184)"
        """

        # 1. Intentar atributo directo (Reddit moderno)
        try:
            attr_val = post_element.get_attribute("comment-count")
            if attr_val:
                return int(attr_val)
        except Exception:
            pass

        # 2. Selectores para todas las versiones de Reddit
        selectors = [
            # Reddit moderno
            '[data-testid="comment-count"]',
            'a[data-click-id="comments"]',
            'faceplate-number[slot="comment-count"]',

            # Old Reddit
            'ul.flat-list li.first a',
            'a.comments',

            # Otros posibles
            'span:contains("comments")',
            'span[data-click-id="comments"]',
        ]

        # Regex robusta
        number_regex = r'(\d[\d,\.]*)\s*([kKmM]?)'

        for selector in selectors:
            text = self._safe_get_element_text(post_element, selector)
            if not text:
                continue

            # Normalizar Unicode (NBSP, etc.)
            text = unicodedata.normalize("NFKC", text)
            text = text.replace("\xa0", " ")

            # Casos tipo "Comments (184)"
            paren_match = re.search(r'\((\d[\d,\.]*)\)', text)
            if paren_match:
                num = paren_match.group(1).replace(",", "")
                try:
                    return int(float(num))
                except:
                    pass

            # Buscar números normales
            matches = re.findall(number_regex, text)
            if not matches:
                continue

            # Tomar el último número encontrado
            num_str, suffix = matches[-1]
            num_str = num_str.replace(",", "")

            try:
                number = float(num_str)
            except ValueError:
                continue

            # Multiplicadores
            if suffix.lower() == "k":
                number *= 1000
            elif suffix.lower() == "m":
                number *= 1_000_000

            return int(number)

        return 0
    
    
    def _extract_flair(self, post_element):
        # etiqueta del post
        selectors = [
            'span.linkflairtext',
            'span.flair',
            'faceplate-tracker[noun="post_flair"]',
            'span[slot="flair"]',
            '[data-testid="post-flair"]'
        ]
        
        for selector in selectors:
            flair = self._safe_get_element_text(post_element, selector)
            if flair:
                return flair.strip()
        
        return ''
    
    def _resolve_reddit_media_url(self,href):
        if 'reddit.com/media?url=' in href:
            parsed = urlparse(href)
            query = parse_qs(parsed.query)
            if 'url' in query:
                return unquote(query['url'][0])
        return href

    def _is_image_url(self,url: str) -> bool:
        """
        Detecta si un enlace apunta a una imagen (png, jpg, jpeg, gif, webp, etc.)
        Ejemplos válidos:
        - https://i.redd.it/xyz.png
        - https://preview.redd.it/abc.jpeg?width=500&format=png
        """
        image_pattern = re.compile(r'\.(png|jpe?g|gif|bmp|webp|svg|tiff)(\?.*)?$', re.IGNORECASE)
        # Algunos casos de imágenes con parámetros 'format=png' o similares
        return bool(image_pattern.search(url)) or 'format=png' in url or 'format=jpg' in url or 'format=jpeg' in url


    def _is_video_url(self,url: str) -> bool:
        """
        Detecta si un enlace apunta a un video (YouTube, Reddit video, etc.)
        Ejemplos válidos:
        - https://youtu.be/abc123
        - https://youtube.com/watch?v=xyz
        - https://v.redd.it/abcd1234
        """
        video_domains = ["youtu.be", "youtube.com", "v.redd.it", "redditmedia.com/media"]
        parsed = urlparse(url)
        return any(domain in parsed.netloc for domain in video_domains)


    def _is_external_url(self,url: str) -> bool:
        """
        Detecta si un enlace NO pertenece al dominio Reddit.
        Ejemplos:
        - https://reddit.com/... => False
        - https://i.redd.it/... => False
        - https://preview.redd.it/... => False
        - https://example.com/... => True
        """
        reddit_domains = ["reddit.com", "redd.it", "redditmedia.com", "preview.redd.it"]
        parsed = urlparse(url)
        return not any(domain in parsed.netloc for domain in reddit_domains)


    def _extract_post_text(self,post_element):
        text_content = ''
        
        # intentar sacar texto        
        text_selectors = [
            # Reddit moderno
            'div[data-test-id="post-content"] div[data-click-id="text"]',
            'div[data-test-id="post-content"] div.RichTextJSON-root',
            'div[data-test-id="post-content"] div[data-adclicklocation="text"]',
            'div[data-test-id="post-content"] div[data-testid="post-container"] div[data-click-id="text"]',            
            'shreddit-post shreddit-post-text-body[slot="text-body"] div.md',

            # Old Reddit
            'div.expando div.usertext-body div.md',
            'div.thing div.usertext-body div.md',
            'div#siteTable div.usertext-body div.md',
        ]


        for selector in text_selectors:
            text = self._safe_get_element_text(post_element, selector)
            if text:
                text_content = self._clean_and_normalize_text(text.strip()[:500])  # limitar a 500 chars
                break
            
        return text_content

    def _extract_content_type_and_media_old(self,post_element):
        
        content_type = []
        media_url_list = []        
        external_url_list = []
        text_content = ''

        
        # buscar contenido multimedia
        # en old.reddit todas las imagenes y videls son links href
        img_selectors = [
            'a.thumbnail.outbound',
            'img[slot="thumbnail"]',
            'img[alt="Post image"]',
            'a[slot="thumbnail"] img',
            'img.preview',
            'div.md a[href*="preview.redd.it"]'
        ]
        
        for selector in img_selectors:
            url_list = self._safe_get_element_media(post_element, selector, 'href')
            if url_list:
                break          

        if url_list:
            try:           
                for link in url_list:   
                    if self._is_image_url(link):
                        media_url_list.append(link)
                        if 'image' not in content_type:
                            content_type.append('image')
                        break
                    elif self._is_video_url(link):
                        media_url_list.append(link)
                        if 'video' not in content_type:
                            content_type.append('video')
                        break
                    elif self._is_external_url(link):
                        external_url_list.append(link)
                        break
            except Exception as e:
                print(f"Error al buscar enlaces en texto: {e}")

        text_content = self._extract_post_text(post_element)

        if text_content != '':        
            content_type.append("text")

        media_url_list = " | ".join(map(str, media_url_list))
        external_url_list = " | ".join(map(str, external_url_list))
        
        # controla los casos en que el post es un link externo
        if not content_type and external_url_list:
            content_type = "link"            
        else:
            content_type = " | ".join(map(str, content_type))

        return content_type, media_url_list, external_url_list, text_content

    def _extract_content_type_and_media(self, post_element):
      
        # ver qué tipo de contenido es y si tiene media
        content_type = []
        media_url_list = []
        external_url_list = []
        text_content = ''
        
        # buscar imágenes
        img_selectors = [
            'a.thumbnail.outbound',
            'img[slot="thumbnail"]',
            'img[alt="Post image"]',
            'a[slot="thumbnail"] img',
            'img.preview',
            'div.md a[href*="preview.redd.it"]',
            "div.media-lightbox-img img.preview-img"
        ]

        for selector in img_selectors:
            url_list = self._safe_get_element_media(post_element, selector, 'src')
            if url_list:              
                break
        
        if url_list and url_list is not None:
            try:           
                for link in url_list:  
                    if self._is_image_url(link):
                        media_url_list.append(link)
                        if 'image' not in content_type:
                            content_type.append('image')
                        break
                    elif self._is_video_url(link):
                        media_url_list.append(link)
                        if 'video' not in content_type:
                            content_type.append('video')
                        break
                    elif self._is_external_url(link):
                        external_url_list.append(link)
                        break
            except Exception as e:
                print(f"Error al buscar enlaces de imagen: {e}")



        # buscar videos
        video_selectors = [
            'video',
            'shreddit-player',
            "shreddit-embed"
        ]
      

        for selector in img_selectors:
            url_list = self._safe_get_element_media(post_element, selector, 'html')
            if url_list:              
                break

        if url_list and url_list is not None:
            try:           
                for link in url_list:   
                    if self._is_image_url(link):
                        media_url_list.append(link)
                        if 'image' not in content_type:
                            content_type.append('image')
                        break
                    elif self._is_video_url(link):
                        media_url_list.append(link)
                        if 'video' not in content_type:
                            content_type.append('video')
                        break
                    elif self._is_external_url(link):
                        external_url_list.append(link)
                        break
            except Exception as e:
                print(f"Error al buscar enlaces de video: {e}")

        
        
        # buscar links externos
        link_selectors = [
            "div.media-lightbox-img a[target='_blank'][href^='http']",
            'a[slot="outbound-link"]',
            'a[target="_blank"][rel*="noopener"]'
        ]

       

        for selector in img_selectors:
            url_list = self._safe_get_element_media(post_element, selector, 'href')
            if url_list:              
                break


        if url_list and url_list is not None:    
            try:           
                for link in url_list:   
                    if self._is_image_url(link):
                        media_url_list.append(link)
                        if 'image' not in content_type:
                            content_type.append('image')
                        break
                    elif self._is_video_url(link):
                        media_url_list.append(link)
                        if 'video' not in content_type:
                            content_type.append('video')
                        break
                    elif self._is_external_url(link):
                        external_url_list.append(link)
                        break
            except Exception as e:
                print(f"Error al buscar enlaces externos: {e}")

        
       

        text_content = self._extract_post_text(post_element)

        if text_content != '':        
            content_type.append("text")

        media_url_list = " | ".join(map(str, media_url_list))
        external_url_list = " | ".join(map(str, external_url_list))
        
        # controla los casos en que el post es un link externo
        if not content_type and external_url_list:
            content_type = "link"            
        else:
            content_type = " | ".join(map(str, content_type))

        return content_type, media_url_list, external_url_list, text_content

 
    
    def _extract_timestamp(self, post_element):
        # cuándo se publicó
        selectors = [
            'faceplate-timeago',
            'time',
            'a[data-click-id="timestamp"]'
        ]
        
        for selector in selectors:
            time_elem = self._safe_get_element_text(post_element, selector, 'datetime')
            if time_elem:
                try:
                    dt = datetime.fromisoformat(time_elem.replace('Z', '+00:00'))
                    return dt.strftime("%Y-%m-%d %H:%M:%S"), dt.hour
                except:
                    pass

            ts_attr = self._safe_get_element_text(post_element, selector, 'ts')
            if ts_attr and ts_attr.isdigit():
                try:
                    # ts viene en milisegundos → convertir a segundos
                    timestamp = int(ts_attr) / 1000
                    dt = datetime.fromtimestamp(timestamp, tz=timezone.utc)
                    return dt.strftime("%Y-%m-%d %H:%M:%S"), dt.hour
                except Exception:
                    pass
                
            # si no hay datetime, intentar con el texto
            time_text = self._safe_get_element_text(post_element, selector)
            if time_text:
                # formato relativo tipo "2 hours ago"
                return time_text, -1
        
        try:
            created_ts = post_element.get_attribute('created-timestamp')
            if created_ts:
                dt = datetime.fromisoformat(created_ts.replace('Z', '+00:00'))
                return dt.strftime("%Y-%m-%d %H:%M:%S"), dt.hour
        except Exception:
            pass

        return 'Unknown', -1
    
    
    def extract_post_data(self, post_element):
        
        
        # extraer todo de un post
        post_id = self._extract_post_id(post_element)
        
        # metadatos básicos
        title = self._extract_title(post_element)
        author = self._extract_author(post_element)
        karma = self._extract_karma(post_element)
        
        num_comments = self._extract_num_comments(post_element)
        flair = self._extract_flair(post_element)

        
        
        # contenido y media
        if self.config.USE_OLD_REDDIT:
            content_type, media_url, external_url, text_content = self._extract_content_type_and_media_old(post_element)
            upvote_ratio = self._extract_upvote_ratio(post_element)
        else:
            content_type, media_url, external_url, text_content = self._extract_content_type_and_media(post_element)
            upvote_ratio = self._extract_upvote_count_new(post_element)

        
        # timestamp
        posted_time, posted_hour = self._extract_timestamp(post_element)
        
        # juntar todo en un diccionario
        post_data = {
            'post_id': post_id,
            'title': title,
            'author': author,
            'subreddit': self.config.SUBREDDIT,
            'karma': karma,
            'upvote_ratio': upvote_ratio,
            'num_comments': num_comments,
            'flair': flair,
            'content_type': content_type,
            'text_content': text_content,
            'media_url': media_url,
            'external_url': external_url,
            'posted_time': posted_time,
            'posted_hour': posted_hour
        }
        
        return post_data
