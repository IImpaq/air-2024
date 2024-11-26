from typing import Union
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI
from mockData import moviesMock


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GetMovieRecommendationsInput(BaseModel):
   mood: str
   era: str
   language: str
   additionalNotes: str
   genres: list[str]

class GetMovieDescriptionInput(BaseModel):
    name: str
    id: str



@app.get("/")
def read_root():
    return {"Advanced": "Information Retrieval"}

@app.post("/movieRecommendation")
def movie_recommendation(input: GetMovieRecommendationsInput):
    print("movieRecommendation with data:", input)
    return {"recommendations": moviesMock}

@app.post("/movieDescription")
def movie_description(input: GetMovieDescriptionInput):
    print("movieRecommendation with data:", input.name, input.id)
    return {"name": input.name, "id": input.id, "recommendations": ["Movie1", "Movie2", "Movie3"]}
