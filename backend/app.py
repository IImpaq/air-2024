from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from service import proceedMovieRecommendation, proceedMovieDescription, proceedAvailableLanguages, proceedAvailableGenres
from inputTypes import GetMovieRecommendationsInput, GetMovieDescriptionInput

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Advanced": "Information Retrieval"}

@app.get("/availableGenres")
def available_genres():
    genres = proceedAvailableGenres()
    return {"genres": genres}

@app.get("/availableLanguages")
def available_languages():
    languages = proceedAvailableLanguages()
    return {"languages": languages}

@app.post("/movieRecommendation")
def movie_recommendation(input: GetMovieRecommendationsInput):
    print("movieRecommendation with body:", input.dict())
    recommended_movies = proceedMovieRecommendation(input)
    return {"movies": recommended_movies}

@app.post("/movieDescription")
def movie_description(input: GetMovieDescriptionInput):
    print("movieDescription with body:", input.dict())
    movie_description = proceedMovieDescription(input)
    print(movie_description)
    return {"genre": movie_description["genre"], "summary": movie_description["summary"]}
