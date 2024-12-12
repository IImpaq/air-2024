from inputTypes import GetMovieRecommendationsInput
from nltk.corpus import stopwords
from nltk import WordNetLemmatizer, word_tokenize
import numpy as np
import pandas as pd
from pathlib import Path
import pickle
import re
from sentence_transformers import SentenceTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import torch
from transformers import pipeline
from typing import List, Dict, Tuple


class MovieRecommender:
    def __init__(self, dataset_path: str):
        print("Defining constants...")
        self._era_ranges = {
            "any": (1895, 2024),
            "silent": (1895, 1927),
            "golden": (1927, 1948),
            "postwar": (1948, 1965),
            "new": (1965, 1983),
            "blockbuster": (1983, 1999),
            "digital": (2000, 2010),
            "streaming": (2010, 2024)
        }

        self._similarity_weights = {
            "semantic": 0.4,
            "tfidf": 0.25,
            "sentiment": 0.25,
            "popularity": 0.1
        }

        print("Loading dataset...")
        self.dataset = pd.read_csv(dataset_path)

        print("Selecting device...")
        self.device = self._get_device()

        print("Initializing models...")
        self.semantic_model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")
        self.sentiment_analyzer = pipeline("sentiment-analysis",
                                           model="distilbert-base-uncased-finetuned-sst-2-english", device=self.device)
        self.tfidf = TfidfVectorizer(max_features=5000, min_df=2, max_df=0.95, stop_words="english", ngram_range=(1, 2))
        self.semantic_model.to(self.device)

        print("Setting up NLP utilities (lemmatizer and stopwords)...")
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words("english"))

        print("Setting up cache directory...")
        self.cache_dir = Path("cache")
        self.cache_dir.mkdir(exist_ok=True)

    def _get_device(self):
        if torch.cuda.is_available():
            print("CUDA available")
            return torch.device("cuda")
        elif torch.backends.mps.is_available():
            print("MPS available")
            return torch.device("mps")
        else:
            print("Fallback to CPU")
            return torch.device("cpu")

    def _clean_text(self, text: str) -> str:
        if not isinstance(text, str) or not text.strip():
            return "NEUTRAL"

        text = re.sub(r"[^a-zA-Z\s]", " ", text.lower())
        tokens = word_tokenize(text)

        lemmatized_tokens = []
        for token in tokens:
            if token not in self.stop_words and len(token) > 2:
                lemmatized_tokens.append(self.lemmatizer.lemmatize(token))

        cleaned_text = " ".join(lemmatized_tokens)

        if cleaned_text.strip():
            return cleaned_text

        return "NEUTRAL"

    def _get_cached_embeddings(self, cache_key: str) -> np.ndarray or None:
        cache_file = self.cache_dir / f"{cache_key}.pkl"

        if cache_file.exists():
            return pickle.load(cache_file.open("rb"))

        return None

    def _set_cached_embeddings(self, embeddings: np.ndarray, cache_key: str) -> None:
        cache_file = self.cache_dir / f"{cache_key}.pkl"
        with cache_file.open("wb") as f:
            pickle.dump(embeddings, f)

    def _get_sentiment_score(self, text: str) -> float:
        result = self.sentiment_analyzer(text[:512])
        return result[0]["score"] if result[0]["label"] == "POSITIVE" else 1 - result[0]["score"]

    def _compute_similarity_score(self,
                                  semantic_sim: np.ndarray,
                                  tfidf_sim: np.ndarray,
                                  sentiment_scores: np.ndarray,
                                  popularity: np.ndarray) -> np.ndarray:#
        # TODO: Check if normilization has a bug (? why should it) or dataset is skewed
        normalized_popularity = (popularity - popularity.min()) / (popularity.max() - popularity.min())

        return (
                self._similarity_weights["semantic"] * semantic_sim +
                self._similarity_weights["tfidf"] * tfidf_sim +
                self._similarity_weights["sentiment"] * sentiment_scores +
                self._similarity_weights["popularity"] * normalized_popularity
        )

    def _generate_recommendations(self, movies_df: pd.DataFrame,
                                  preferences: GetMovieRecommendationsInput) -> pd.DataFrame:
        if movies_df.empty:
            raise ValueError("No movies matching with trivial criteria. Maybe loosen the criteria...")

        if movies_df["rich_features"].str.len().sum() == 0:
            raise ValueError(
                "Rich features missing in dataset. Maybe call fetch.py/preprocess.py before starting the backend...")

        # Find potentially cached embeddings
        cache_key = f'movies_{preferences.mood}_{preferences.era}_{preferences.language}_{"-".join(preferences.genres)}_{len(movies_df)}'
        semantic_embeddings = self._get_cached_embeddings(cache_key)

        # If no cached embeddings, encode text features and cache them
        if semantic_embeddings is None:
            semantic_embeddings = self.semantic_model.encode(
                movies_df["rich_features"].values,
                batch_size=32,
                show_progress_bar=True
            )
            self._set_cached_embeddings(semantic_embeddings, cache_key)

        # Fit and transform TF-IDF
        try:
            tfidf_matrix = self.tfidf.fit_transform(movies_df["rich_features"])
            print(f"TF-IDF vocabulary size: {len(self.tfidf.vocabulary_)}")
        except ValueError as e:
            print(f"TF-IDF error: {e}")
            print("Sample of rich_features:")
            print(movies_df["rich_features"].head())
            raise

        # Encode query text
        query_text = f"{preferences.mood} {preferences.additionalNotes}"
        query_embedding = self.semantic_model.encode([query_text])

        # Calculate cosine similarities
        semantic_similarities = cosine_similarity(query_embedding, semantic_embeddings)[0]
        tfidf_similarities = cosine_similarity(self.tfidf.transform([self._clean_text(query_text)]), tfidf_matrix)[0]

        # Calculate sentiment alignment
        sentiment_scores = np.array([self._get_sentiment_score(text) for text in movies_df["overview"]])

        # Get final similarity scores
        final_scores = self._compute_similarity_score(
            semantic_similarities,
            tfidf_similarities,
            sentiment_scores,
            movies_df["popularity"].values
        )

        # Getting the top 4 recommendations
        top_indices = final_scores.argsort()[-4:][::-1]
        recommendations = movies_df.iloc[top_indices].copy()

        # Add confidence score to recommendations
        # TODO: Maybe use this in frontend to visualize usefulness to user
        recommendations["confidence_score"] = final_scores[top_indices]

        return recommendations

    def _compare_genres(self, movie_genres: str, preferred_genres: List[str]) -> bool:
        # Check if either of the lists is empty
        if not movie_genres or not preferred_genres:
            return False

        # Lowercase for case-insensitive comparison
        movie_genres_lower = movie_genres.lower()
        preferred_genres_lower = [genre.lower() for genre in preferred_genres]

        # Check if any of the preferred genres is in movie genres with nice inline syntax
        return any(genre in movie_genres_lower for genre in preferred_genres_lower)

    def get_movies(self, preferences: GetMovieRecommendationsInput) -> List[Dict]:
        # Convert era name to range
        era_range = self._era_ranges.get(preferences.era)

        # Pre-Filter based on trivial criteria to reduce the dataset size
        # TODO: Might improve language selection in frontend later
        # TODO: Add support for selection of multiple languages
        # TODO: Add support for selecting any language
        filtered_df = self.dataset[
            (self.dataset["original_language"] == preferences.language) &
            (self.dataset["release_year"].between(era_range[0], era_range[1])) &
            (self.dataset["genres"].apply(lambda x: self._compare_genres(x, preferences.genres))) &
            (self.dataset["popularity"] >= 10.0) # TODO: Maybe leave popularity out later. Currently at least 10
            ]

        print(f"Movies left after filtering: {len(filtered_df)}")

        # If more than 1000 movies, sample a subset to improve recommendation performance
        if len(filtered_df) > 1000:
            filtered_df = filtered_df.sample(1000)

        # Generate recommendations
        recommendations_pre = self._generate_recommendations(filtered_df, preferences)

        # Post-process recommendations
        # TODO: Maybe cleaner way may be possible
        recommendations_post = []
        for i, row in recommendations_pre.iterrows():
            recommendations_post.append({
                "title": str(row["title"]),
                "genre": row["genres"],
                "rating": float(row["popularity"]),
                "year": str(row["release_year"]),
                "poster": str(row["poster_path"]),
                "confidence_score": row["confidence_score"],
            })

        return recommendations_post
