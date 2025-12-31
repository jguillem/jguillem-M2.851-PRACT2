"""
Script para analizar el dataset generado
Autores: Jordi Guillem y Xairo Campos
"""

import pandas as pd
import sys


def analyze_dataset(filepath):
    # analizar y mostrar stats del dataset
    try:
        # leer csv
        df = pd.read_csv(filepath)
        
        print("=" * 80)
        print("ANÁLISIS DEL DATASET DE REDDIT")
        print("=" * 80)
        
        # info básica
        print(f"\n📊 Información General:")
        print(f"   - Total de posts: {len(df)}")
        print(f"   - Columnas: {len(df.columns)}")
        print(f"   - Memoria utilizada: {df.memory_usage(deep=True).sum() / 1024 / 1024:.2f} MB")
        
        # valores nulos
        print(f"\n🔍 Valores Nulos:")
        null_counts = df.isnull().sum()
        if null_counts.sum() > 0:
            for col, count in null_counts[null_counts > 0].items():
                print(f"   - {col}: {count} ({count/len(df)*100:.2f}%)")
        else:
            print("   ✓ No hay valores nulos")
        
        # stats de karma
        print(f"\n⭐ Estadísticas de Karma:")
        print(f"   - Media: {df['karma'].mean():.2f}")
        print(f"   - Mediana: {df['karma'].median():.2f}")
        print(f"   - Máximo: {df['karma'].max()}")
        print(f"   - Mínimo: {df['karma'].min()}")
        
        # stats de comentarios
        print(f"\n💬 Estadísticas de Comentarios:")
        print(f"   - Media: {df['num_comments'].mean():.2f}")
        print(f"   - Mediana: {df['num_comments'].median():.2f}")
        print(f"   - Máximo: {df['num_comments'].max()}")
        
        # distribución de sentimientos
        print(f"\n😊 Distribución de Sentimientos:")
        sentiment_dist = df['sentiment'].value_counts()
        for sentiment, count in sentiment_dist.items():
            print(f"   - {sentiment.capitalize()}: {count} ({count/len(df)*100:.2f}%)")
        
        # tipos de contenido
        print(f"\n📁 Tipos de Contenido:")
        content_dist = df['content_type'].value_counts()
        for content_type, count in content_dist.items():
            print(f"   - {content_type.capitalize()}: {count} ({count/len(df)*100:.2f}%)")
        
        # autores más activos
        print(f"\n👥 Top 5 Autores Más Activos:")
        top_authors = df['author'].value_counts().head(5)
        for i, (author, count) in enumerate(top_authors.items(), 1):
            print(f"   {i}. {author}: {count} posts")
        
        # flairs más comunes
        if 'flair' in df.columns:
            print(f"\n🏷️  Top 5 Flairs Más Comunes:")
            top_flairs = df[df['flair'] != '']['flair'].value_counts().head(5)
            for i, (flair, count) in enumerate(top_flairs.items(), 1):
                print(f"   {i}. {flair}: {count} posts")
        
        # posts con más engagement
        print(f"\n🔥 Top 3 Posts con Más Karma:")
        top_posts = df.nlargest(3, 'karma')[['title', 'author', 'karma', 'num_comments']]
        for i, row in enumerate(top_posts.itertuples(), 1):
            print(f"\n   {i}. '{row.title[:60]}...'")
            print(f"      Autor: {row.author} | Karma: {row.karma} | Comentarios: {row.num_comments}")
        
        print("\n" + "=" * 80)
        print("✓ Análisis completado")
        print("=" * 80)
        
    except FileNotFoundError:
        print(f"[✗] Error: No se encontró el archivo '{filepath}'")
        print("[i] Asegúrate de haber ejecutado el scraper primero: python main.py")
    except Exception as e:
        print(f"[✗] Error al analizar el dataset: {str(e)}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    # ruta por defecto
    default_path = "../data/raw/reddit_datascience_dataset.csv"
    
    # permitir especificar ruta como argumento
    filepath = sys.argv[1] if len(sys.argv) > 1 else default_path
    
    analyze_dataset(filepath)
