import pandas as pd
import os
import time

COLUMNS = ['id', 'title', 'genres', 'original_language', 'overview', 'popularity', 'release_date', 'status', 'keywords']

def main():
    print("Starting preprocessing")

    #df = pd.read_csv("hf://datasets/wykonos/movies/movies_dataset.csv") # could be loaded directely but too slow

    df = pd.read_csv("movies_dataset.csv")

    df = drop_columns(df)

    df = filter_released_movies(df)

    df = drop_na(df) # cuts from 700.000 to 180.000 entries 

    df = get_release_year(df)

    df = correct_dtypes(df)

    print_details(df)

    df.to_csv('../data/movies_dataset_preprocessed')

    

def drop_columns(df): 
    column_names = list(df.columns)
    for col in column_names: 
        if col not in COLUMNS:
            df = df.drop(col, axis=1)
    return df

def filter_released_movies(df):
    df = df[df['status'] == 'Released']
    df = df.drop('status', axis=1)
    return df

def drop_na(df):
    column_names = list(df.columns)
    for col in column_names:
        df = df[df[col].notna()]
    return df

def get_release_year(df):
    df['release_date'] = pd.to_datetime(df['release_date'])
    df['release_year'] = df['release_date'].dt.year
    df = df.drop('release_date', axis=1)
    return df

def correct_dtypes(df):
    df['title'] = df['title'].astype('string') 
    df['genres'] = df['genres'].astype('string')
    df['original_language'] = df['original_language'].astype('string')
    df['overview'] = df['overview'].astype('string')
    df['keywords'] = df['keywords'].astype('string')
    return df

def print_details(df):
    print(df.head())
    print(len(df))
    column_names = list(df.columns)
    print(column_names)




if __name__=="__main__":
    start_time = time.time()
    
    main()

    run_time = time.time() - start_time
    print(run_time)
