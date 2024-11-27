from mockData import moviesMock, descriptionMock
from inputTypes import GetMovieRecommendationsInput, GetMovieDescriptionInput
import time
def proceedMovieRecommendation(input: GetMovieRecommendationsInput):
    print(input)
    #TODO Implement recommendations here
    time.sleep(3)
    recommended_movies = moviesMock
    return recommended_movies



def proceedMovieDescription(input: GetMovieDescriptionInput):
    print(input)
    print("start")
    #TODO Implement description here
    time.sleep(3)
    print("end")

    description = descriptionMock
    return description
