from inputTypes import GetMovieRecommendationsInput
from recommender import MovieRecommender

def get_valid_input(prompt, valid_options, allow_multiple=True):
    while True:
        print("\033[H\033[J") # https://stackoverflow.com/a/50560686
        print(f"\nPossible inputs: {", ".join(valid_options)}")
        user_input = input(prompt).strip()

        if allow_multiple:
            selections = [x.strip() for x in user_input.split(",")]
            invalid = [x for x in selections if x not in valid_options]

            if invalid:
                print(f"Invalid inputs: {", ".join(invalid)}. Please try again.")
            else:
                return selections
        else:
            if user_input not in valid_options:
                print(f"Invalid input: {user_input}. Please try again.")
            else:
                return [user_input]

def proceedAvailableLanguages(recommender):
    languages = []

    for i in range(len(recommender.dataset)):
        if recommender.dataset["original_language"][i] not in languages:
            languages.append(recommender.dataset["original_language"][i])

    return languages

def proceedAvailableGenres(recommender):
    result = []

    for i in range(len(recommender.dataset)):
        genres = recommender.dataset["genres"][i].split("-")
        for genre in genres:
            if genre in result:
                continue
            result.append(genre)

    return result

def main():
    use_default = input("Use default dataset path (../data/movies_dataset_preprocessed.csv)? (y/n): ").lower()

    if use_default == "y":
        dataset_path = "../data/movies_dataset_preprocessed.csv"
    else:
        dataset_path = input("Enter the path to your dataset: ")

    recommender = MovieRecommender(dataset_path)

    while True:
        valid_genres = proceedAvailableGenres(recommender)
        genres = get_valid_input("Enter preferred genres (comma-separated): ", valid_genres)

        valid_moods = recommender._mood_to_emotion.keys()
        mood = get_valid_input("Enter preferred mood: ", valid_moods, False)[0]

        valid_eras = recommender._era_ranges
        era = get_valid_input("Enter preferred era: ", valid_eras, False)[0]

        valid_languages = proceedAvailableLanguages(recommender)
        language = get_valid_input("Enter preferred language: ", valid_languages, False)[0]

        notes = input("\nEnter any additional notes (or press Enter to skip): ")

        print("\033[H\033[J") # https://stackoverflow.com/a/50560686

        recommendations = recommender.get_movies(
            GetMovieRecommendationsInput(
                mood=mood,
                era=era,
                language=language,
                additionalNotes=notes,
                genres=genres,
            )
        )

        print("\033[H\033[J") # https://stackoverflow.com/a/50560686

        print("\nTop 4 Recommended Movies:")
        for i, movie in enumerate(recommendations[:4], 1):
            print(f"{i}: {movie["title"]}")
            print(f"\t- Genre: {movie["genre"]}")
            print(f"\t- Rating: {movie["rating"]}")
            print(f"\t- Year: {movie["year"]}")
            print(f"\t- Confidence: {movie["confidence"]:.2%}")

        repeat = input("\nWould you like to get more recommendations? (y/n): ").lower()
        if repeat != "y":
            print("\nBye.")
            break

if __name__ == "__main__":
    main()
