from inputTypes import GetMovieRecommendationsInput, GetMovieDescriptionInput
from recommender import MovieRecommender
from subtitles import initializeOpensubtitles, downloadAndSaveSubtitle, checkSubtitleFile, summarizeSubtitles, extractKeyThemes

def clear_screen():
    print("\033[H\033[J") # https://stackoverflow.com/a/50560686

def get_valid_input(prompt, valid_options, allow_multiple=True):
    while True:
        clear_screen()
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

def get_movie_description(input: GetMovieDescriptionInput):
    movie_name = f"{input.year} - {input.title}"
    language = "en"                                             # TODO: Summarys in different languages?

    # Due to the API limit subtitles will be downloaded
    cleaned_subtitles = checkSubtitleFile(movie_name)

    if cleaned_subtitles == None:
        ost = initializeOpensubtitles()                         # TODO: Exception handling when API limit is reached
        cleaned_subtitles = downloadAndSaveSubtitle(ost, movie_name, language)

    summarized_description = summarizeSubtitles(cleaned_subtitles)

    key_themes = extractKeyThemes(cleaned_subtitles, 3)

    description = {
        "genre": key_themes,
        "summary": summarized_description
        }

    return description

def get_available_languages(recommender):
    languages = []

    for i in range(len(recommender.dataset)):
        if recommender.dataset["original_language"][i] not in languages:
            languages.append(recommender.dataset["original_language"][i])

    return languages

def get_available_genres(recommender):
    result = []

    for i in range(len(recommender.dataset)):
        genres = recommender.dataset["genres"][i].split("-")
        for genre in genres:
            if genre in result:
                continue
            result.append(genre)

    return result

def main():
    use_default = input("Use default dataset path (../data/movies_dataset_preprocessed.csv)? (Y/n): ").lower()

    if len(use_default) == 0 or use_default == "y":
        dataset_path = "../data/movies_dataset_preprocessed.csv"
    else:
        dataset_path = input("Enter the path to your dataset: ")

    recommender = MovieRecommender(dataset_path)

    while True:
        valid_genres = get_available_genres(recommender)
        genres = get_valid_input("Enter preferred genres (comma-separated): ", valid_genres)

        valid_moods = recommender._mood_to_emotion.keys()
        mood = get_valid_input("Enter preferred mood: ", valid_moods, False)[0]

        valid_eras = recommender._era_ranges
        era = get_valid_input("Enter preferred era: ", valid_eras, False)[0]

        valid_languages = get_available_languages(recommender)
        language = get_valid_input("Enter preferred language: ", valid_languages, False)[0]

        clear_screen()

        notes = input("\nEnter any additional notes (or press Enter to skip): ")

        clear_screen()

        recommendations = recommender.get_movies(
            GetMovieRecommendationsInput(
                mood=mood,
                era=era,
                language=language,
                additionalNotes=notes,
                genres=genres,
            )
        )

        show_movies = True

        while show_movies:
            clear_screen()

            print("\nTop 4 Recommended Movies:")
            for i, movie in enumerate(recommendations[:4], 1):
                print(f"{i}: {movie["title"]}")
                print(f"\t- Genre: {movie["genre"]}")
                print(f"\t- Rating: {movie["rating"]}")
                print(f"\t- Year: {movie["year"]}")
                print(f"\t- Confidence: {movie["confidence"]:.2%}")

            want_summary = input("\nWould you like to see a movie summary? (y/n): ").lower()

            if want_summary == "y":
                while True:
                    movie_id = input("Enter movie ID: ")

                    if len(movie_id) == 0:
                        break

                    try:
                        description = get_movie_description(
                            GetMovieDescriptionInput(
                                title=recommendations[int(movie_id) - 1]["title"],
                                id="0",
                                year=recommendations[int(movie_id) - 1]["year"],
                            )
                        )
                    except:
                        description = None

                    clear_screen()

                    if description:
                        print(f"\nMovie Introduction:")
                        print(description["summary"])
                        print(f"\nMovie Themes:")
                        for theme in description["genre"]:
                            print(f"\t- {theme}")
                    else:
                        print("Oops. Something went wrong... Please try again.")

                    repeat = input("\nWould you like to see the list of recommended movies again? (y/n): ").lower()

                    if repeat == "y":
                        break
            else:
                show_movies = False

        repeat = input("\nWould you like to get more recommendations? (y/n): ").lower()

        if repeat != "y":
            print("\nBye.")
            break

if __name__ == "__main__":
    main()
