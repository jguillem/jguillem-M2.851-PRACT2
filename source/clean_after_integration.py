import pandas as pd

def clean_dataset(df):
    """
    Limpieza avanzada del dataset integrado con imputación completa
    según las reglas definidas.
    """

    # ============================================================
    # 0. NORMALIZAR VALORES FALTANTES "RAROS" A NaN
    # ============================================================
    df = df.replace(["nan", "None", "NaT", "", " "], pd.NA)

    # ============================================================
    # 1. IMPUTACIÓN DE CAMPOS STRING
    # ============================================================

    string_defaults = {
        "title": "untitled",
        "author": "unknown",
        "flair": "no flair",
        "text_content": "no content",
        "media_url": "no media url",
        "external_url": "no external url",
        "post_id": "no post id",
        "sentiment": "neutral",
    }

    for col, default in string_defaults.items():
        if col in df.columns:
            df[col] = df[col].fillna(default)

    # ============================================================
    # 2. IMPUTACIÓN DE CAMPOS NUMÉRICOS
    # ============================================================

    # karma → media redondeada
    if "karma" in df.columns:
        mean_karma = df["karma"].dropna().mean()
        df["karma"] = df["karma"].fillna(round(mean_karma)).astype(int)

    # upvote_ratio_new → media redondeada
    if "upvote_ratio_new" in df.columns:
        mean_ratio = df["upvote_ratio_new"].dropna().mean()
        df["upvote_ratio_new"] = df["upvote_ratio_new"].fillna(round(mean_ratio)).astype(int)

    # num_comments → 0
    if "num_comments" in df.columns:
        df["num_comments"] = df["num_comments"].fillna(0).astype(int)

    # ============================================================
    # 3. SENTIMENT: asegurar que son numéricos ANTES de imputar
    # ============================================================

    sentiment_cols = ["sentiment_positive", "sentiment_negative", "sentiment_neutral"]

    for col in sentiment_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    # Imputación básica (solo si hay NaN)
    if "sentiment_positive" in df.columns:
        df["sentiment_positive"] = df["sentiment_positive"].fillna(0)
    if "sentiment_negative" in df.columns:
        df["sentiment_negative"] = df["sentiment_negative"].fillna(0)
    if "sentiment_neutral" in df.columns:
        df["sentiment_neutral"] = df["sentiment_neutral"].fillna(1)

    # ============================================================
    # 4. NORMALIZACIÓN INTELIGENTE DE SENTIMIENTOS
    # ============================================================

    def normalize_sentiment_row(row):
        pos, neg, neu = row

        # Si ya están normalizados (todos entre 0 y 1 y suman ≈ 1)
        if 0 <= pos <= 1 and 0 <= neg <= 1 and 0 <= neu <= 1:
            s = pos + neg + neu
            if 0.99 <= s <= 1.01:
                return row  # no tocar

        # Si son conteos (valores grandes)
        s = pos + neg + neu
        if s == 0:
            return pd.Series([0.0, 0.0, 1.0])

        return pd.Series([pos/s, neg/s, neu/s])

    if all(col in df.columns for col in sentiment_cols):
        df[sentiment_cols] = df[sentiment_cols].apply(normalize_sentiment_row, axis=1)

    # ============================================================
    # 5. IMPUTACIÓN CONDICIONAL
    # ============================================================

    if "content_type" in df.columns and "text_content" in df.columns:
        df["content_type"] = df["content_type"].fillna(
            df["text_content"].apply(lambda x: "text" if x != "no content" else "unknown")
        )

    # ============================================================
    # 6. permalink → URL completa old.reddit.com
    # ============================================================

    if "permalink" in df.columns and "post_id" in df.columns:
        df["permalink"] = df["permalink"].fillna(
            df["post_id"].apply(lambda x: f"https://old.reddit.com/r/datascience/{x}")
        )

    # ============================================================
    # 7. CONVERSIONES DE TIPO
    # ============================================================

    if "posted_time" in df.columns:
        df["posted_time"] = pd.to_datetime(df["posted_time"], errors="coerce")

    if "scraped_at" in df.columns:
        df["scraped_at"] = pd.to_datetime(df["scraped_at"], errors="coerce")

    if "posted_hour" in df.columns:
        df["posted_hour"] = pd.to_numeric(df["posted_hour"], errors="coerce")

    # ============================================================
    # 8. CATEGORÍAS
    # ============================================================

    categorical_cols = ["post_id", "author", "flair", "content_type", "sentiment"]
    for col in categorical_cols:
        if col in df.columns:
            df[col] = df[col].astype("category")

    return df