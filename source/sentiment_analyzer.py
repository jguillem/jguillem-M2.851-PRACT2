"""
Análisis de sentimiento con VADER
Autores: Jordi Guillem y Xairo Campos
"""

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class SentimentAnalyzer:
    # clase para analizar sentimientos en textos
    
    def __init__(self):
        # inicializar el analizador
        self.analyzer = SentimentIntensityAnalyzer()
    
    
    def analyze(self, text):
        # analizar el sentimiento de un texto
        if not text or not isinstance(text, str):
            return self._get_neutral_scores()
        
        text = text.strip()
        
        if not text:
            return self._get_neutral_scores()
        
        scores = self.analyzer.polarity_scores(text)
        
        # añadir etiqueta según el score
        # >= 0.05 es positivo, <= -0.05 es negativo
        compound = scores['compound']
        if compound >= 0.05:
            label = 'positive'
        elif compound <= -0.05:
            label = 'negative'
        else:
            label = 'neutral'
        
        scores['compound_label'] = label
        
        return scores
    
    
    def _get_neutral_scores(self):
        # por defecto devolver neutral
        return {
            'pos': 0.0,
            'neg': 0.0,
            'neu': 1.0,
            'compound': 0.0,
            'compound_label': 'neutral'
        }
    
    
    def batch_analyze(self, texts):
        # analizar varios textos de golpe
        return [self.analyze(text) for text in texts]
