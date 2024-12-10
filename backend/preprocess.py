from pathlib import Path
import re
import time
import pandas as pd
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

COLUMNS = ["id", "title", "genres", "original_language", "overview", "popularity", "release_date", "status", "keywords",
           "credits", "poster_path"]


def drop_columns(df: pd.DataFrame) -> pd.DataFrame:
    column_names = list(df.columns)
    for col in column_names:
        if col not in COLUMNS:
            df = df.drop(col, axis=1)
    return df


def filter_released_movies(df: pd.DataFrame) -> pd.DataFrame:
    df = df[df["status"] == "Released"]
    df = df.drop("status", axis=1)
    return df


def drop_na(df: pd.DataFrame) -> pd.DataFrame:
    column_names = list(df.columns)
    for col in column_names:
        df = df[df[col].notna()]
    return df


def get_release_year(df: pd.DataFrame) -> pd.DataFrame:
    df["release_date"] = pd.to_datetime(df["release_date"])
    df["release_year"] = df["release_date"].dt.year
    df = df.drop("release_date", axis=1)
    return df


def correct_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    df["title"] = df["title"].astype("string")
    df["genres"] = df["genres"].astype("string")
    df["original_language"] = df["original_language"].astype("string")
    df["overview"] = df["overview"].astype("string")
    df["keywords"] = df["keywords"].astype("string")
    return df


def clean_text(text: str, lt: WordNetLemmatizer, sws: set) -> str:
    if not isinstance(text, str):
        return ""

    text = re.sub(r"[^a-zA-Z\s]", " ", text.lower())
    tokens = word_tokenize(text)
    lemmatized_tokens = []
    for token in tokens:
        if token not in sws and len(token) > 2:
            lemmatized_tokens.append(lt.lemmatize(token))

    return " ".join(lemmatized_tokens)


def create_rich_features(row, lt: WordNetLemmatizer, sws: set) -> str:
    features = [
        clean_text(str(row["title"]), lt, sws),
        clean_text(str(row["overview"]), lt, sws),
        clean_text(str(row["genres"]), lt, sws),
        clean_text(str(row["keywords"]), lt, sws),
        clean_text(str(row["credits"]), lt, sws)
    ]

    rich_text = " ".join(filter(None, features))

    if rich_text.strip():
        return rich_text

    return "No rich features"


def add_rich_feature_column(old_df, lt, sws):
    new_df = old_df.copy()
    new_df["rich_features"] = new_df.apply(lambda row: create_rich_features(row, lt, sws), axis=1)
    return new_df


def print_details(df):
    print(df.head())
    print(len(df))
    column_names = list(df.columns)
    print(column_names)


def main():
    print("Starting preprocessing")

    print("Reading CSV")
    df = pd.read_csv("../data/movies_dataset.csv")
    print("Preparing lemmatizer and stopword set")
    lt = WordNetLemmatizer()
    sws = set(stopwords.words("english"))

    print("Dropping columns")
    df = drop_columns(df)
    print("Filtering released movies")
    df = filter_released_movies(df)
    print("Dropping NA")
    df = drop_na(df)  # cuts from 700.000 to 180.000 entries
    print("Getting release year")
    df = get_release_year(df)
    print("Correcting dtypes")
    df = correct_dtypes(df)
    print("Adding rich feature column")
    df = add_rich_feature_column(df, lt, sws)
    print("Saving to CSV")
    df.to_csv("../data/movies_dataset_preprocessed.csv")

    print_details(df)


if __name__ == "__main__":
    start_time = time.time()

    main()

    run_time = time.time() - start_time
    print(run_time)
