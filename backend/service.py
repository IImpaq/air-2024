from recommender import MovieRecommender
from mockData import moviesMock, descriptionMock
from inputTypes import GetMovieRecommendationsInput, GetMovieDescriptionInput
from subtitles import initializeOpensubtitles, downloadAndSaveSubtitle, checkSubtitleFile, summarizeSubtitles, extractKeyThemes
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
    # Cleaning entires from recommendations which are only used for evaluation
    result = []
    for recommendation in recommendations:
        result.append({
          "title": recommendation["title"],
          "genre": recommendation["genre"],
          "rating": recommendation["rating"],
          "year": recommendation["year"],
          "poster": recommendation["poster"],
          "confidence": recommendation["confidence"]
        })

    print(f"Generated recommendations: {recommendations}")
    return result


def proceedMovieDescription(input: GetMovieDescriptionInput):
    print(input)

    movie_name = f"{input.year} - {input.title}"
    language = "en"                                             # TODO: Summarys in different languages?

    # Due to the API limit subtitles will be downloaded
    cleaned_subtitles = checkSubtitleFile(movie_name)

    if cleaned_subtitles == None:
        ost = initializeOpensubtitles()                         # TODO: Exception handling when API limit is reached
        cleaned_subtitles = downloadAndSaveSubtitle(ost, movie_name, language)

    summarized_description = summarizeSubtitles(cleaned_subtitles)

    key_themes = extractKeyThemes(cleaned_subtitles, 3)

    print("Summary: " + summarized_description)
    description = {
        "genre": key_themes,
        "summary": summarized_description
        }

    return description
