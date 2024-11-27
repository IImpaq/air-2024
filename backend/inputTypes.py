from pydantic import BaseModel

class GetMovieDescriptionInput(BaseModel):
    title: str
    id: str
    year: int

class GetMovieRecommendationsInput(BaseModel):
    mood: str
    era: str
    language: str
    additionalNotes: str
    genres: list[str]