from recommender import MovieRecommender
from mockData import moviesMock, descriptionMock
from inputTypes import GetMovieRecommendationsInput, GetMovieDescriptionInput
import time

recommender = MovieRecommender("../data/movies_dataset_preprocessed.csv")

def proceedAvailableLanguages():
    languages = []

    for i in range(len(recommender.dataset)):
        if recommender.dataset["original_language"][i] not in languages:
            languages.append(recommender.dataset["original_language"][i])

    return languages

def proceedMovieRecommendation(input: GetMovieRecommendationsInput):
    print(f"Generating recommendation for: {input}")

    recommendations = recommender.get_movies(input)

    print(f"Generated recommendations: {recommendations}")
    return recommendations


def proceedMovieDescription(input: GetMovieDescriptionInput):
    print(input)
    print("start")
    # TODO Implement description here
    time.sleep(3)
    print("end")

    description = descriptionMock
    return description
