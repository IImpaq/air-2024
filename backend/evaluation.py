from collections import Counter
from inputTypes import GetMovieRecommendationsInput
from itertools import combinations
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
from recommender import MovieRecommender
import seaborn as sns
import sys
import time

class MovieRecommenderEvaluation:
    def __init__(self, recommender: MovieRecommender, cwd = "../evaluation/"):
        if not os.path.exists(cwd):
            print(f"Evaluation directory does not exist: {cwd}")
            sys.exit(1)

        self.recommender = recommender
        self.cwd = cwd
        self.results = {
            "response_times": [],
            "genre_variety": [],
            "confidence_scores": [],
            "rating_distribution": [],
            "genre_distribution": {},
            "precision": [],
            "recall": [],
            "f1_scores": []
        }

    def run(self, test_cases, num_iterations = 3):
        print("Running evaluation...")

        for case_id in range(len(test_cases)):
            for i in range(num_iterations):
                print("\033[H\033[J") # https://stackoverflow.com/a/50560686
                print("-"*50 + f" Iteration {i + 1}/{num_iterations} for test case: {case_id + 1}/{len(test_cases)} " + "-"*50)
                print(f"User Preferences -> Language: {test_cases[case_id].language}, Era: {test_cases[case_id].era}, Genres: {test_cases[case_id].genres}")
                self._test(test_cases[case_id])

        self._calculate_metrics()
        self._plot()

    def _test(self, test_case):
        start_time = time.time()

        try:
            recommendations = self.recommender.get_movies(test_case)

            execution_time = time.time() - start_time
            self.results["response_times"].append(execution_time)

            self._eval_recommendations(recommendations, test_case)
        except Exception as e:
            print(f"Error in during test: {str(e)}")

    def _eval_recommendations(self, recommendations, test_case):
        genres = set()
        for recommendation in recommendations:
            genres.update(recommendation["genre"].split(","))
        self.results["genre_variety"].append(len(genres))

        confidence_scores = [recommendation["confidence"] for recommendation in recommendations]
        self.results["confidence_scores"].extend(confidence_scores)

        ratings = [recommendation["rating"] for recommendation in recommendations]
        self.results["rating_distribution"].extend(ratings)

        for recommendation in recommendations:
            for genre in recommendation["genre"].split("-"):
                genre = genre.strip()
                self.results["genre_distribution"][genre] = self.results["genre_distribution"].get(genre, 0) + 1

        precision, recall = self._calc_precission_recall(recommendations, test_case)
        f1_score = self._calc_f_score(1, precision, recall)

        self.results["precision"].append(precision)
        self.results["recall"].append(recall)
        self.results["f1_scores"].append(f1_score)

    def _calc_precission_recall(self, recommendations, user_preferences):
        era_range = self.recommender._era_ranges[user_preferences.era]

        def is_relevant(movie, preferences):
            year = int(movie["year"])

            popularity_match = movie["popularity"] > 10.0
            confidence_match = movie["confidence"] >= 0.5
            rating_match = movie["rating"] > 5.0
            # These three should always match
            era_match = era_range[0] <= year <= era_range[1]
            genre_match = any(preferred_genre.lower() in movie["genre"].lower() for preferred_genre in preferences.genres)
            language_match = movie["language"] == preferences.language

            relevance_score = sum([
                language_match,
                genre_match,
                era_match,
                rating_match,
                confidence_match,
                popularity_match
            ])

            return relevance_score >= 5

        recommended_relevant = sum([
            1 if is_relevant(movie, user_preferences) else 0 for movie in recommendations
        ])

        total_possible_relevant = sum([
            1 if (
                movie["original_language"] == user_preferences.language and
                any(genre.lower() in movie["genres"].lower() for genre in user_preferences.genres) and
                era_range[0] <= movie["release_year"] <= era_range[1] and
                movie["vote_average"] > 5.0 and
                movie["popularity"] > 10.0
            ) else 0 for movie in self.recommender.dataset.to_dict("records")
        ])

        precision = recommended_relevant / len(recommendations) if len(recommendations) > 0 else 0
        recall = recommended_relevant / total_possible_relevant if total_possible_relevant > 0 else 0

        return precision, recall

    def _calc_f_score(self, beta, precision, recall):
        # https://en.wikipedia.org/wiki/F-score
        return (1 + (beta ** 2)) * (precision * recall) / (((beta ** 2) * precision) + recall)

    def _calculate_metrics(self):
        self.results["metrics"] = {
            "avg_response_time": np.mean(self.results["response_times"]),
            "std_response_time": np.std(self.results["response_times"]),
            "avg_genre_variety": np.mean(self.results["genre_variety"]),
            "std_genre_variety": np.std(self.results["genre_variety"]),
            "avg_confidence": np.mean(self.results["confidence_scores"]),
            "std_confidence": np.std(self.results["confidence_scores"]),
            "avg_rating": np.mean(self.results["rating_distribution"]),
            "std_rating": np.std(self.results["rating_distribution"]),
            "avg_precision": np.mean(self.results["precision"]),
            "avg_recall": np.mean(self.results["recall"]),
            "avg_f1": np.mean(self.results["f1_scores"]),
        }

    def _plot(self):
        plt.figure(figsize=(10, 6))
        sns.histplot(self.results["response_times"])
        plt.title("Response Time Distribution")
        plt.xlabel("Time (seconds)")
        plt.tight_layout()
        plt.savefig(self.cwd + "response_time_dist.png")
        plt.close()

        plt.figure(figsize=(10, 6))
        sns.histplot(self.results["confidence_scores"])
        plt.title("Confidence Score Distribution")
        plt.tight_layout()
        plt.savefig(self.cwd + "confidence_dist.png")
        plt.close()

        plt.figure(figsize=(12, 6))
        genre_counts = Counter(self.results["genre_distribution"]).most_common(10)
        genres, counts = zip(*genre_counts)
        plt.bar(genres, counts)
        plt.xticks(rotation=45)
        plt.title("Top 10 Recommended Genres")
        plt.tight_layout()
        plt.savefig(self.cwd + "top_genres.png")
        plt.close()

    def save(self, filename = "results.json"):
        with open(self.cwd + filename, "w") as f:
            json.dump(self.results, f, indent=2)

    def summary(self):
        print("="*50 + " SUMMARY " + "="*50)

        print("\nResponse Time Statistics:")
        print(f"\t- Average: {self.results["metrics"]["avg_response_time"]:.2f} seconds")
        print(f"\t- Standard Deviation: {self.results["metrics"]["std_response_time"]:.2f} seconds")
        print(f"\t- Min: {min(self.results["response_times"]):.2f} seconds")
        print(f"\t- Median: {np.median(self.results["response_times"]):.2f} seconds")
        print(f"\t- Max: {max(self.results["response_times"]):.2f} seconds")

        print("\nGenre Diversity Statistics:")
        print(f"\t- Average genres per recommendation: {self.results["metrics"]["avg_genre_variety"]:.2f}")
        print(f"\t- Standard Deviation: {self.results["metrics"]["std_genre_variety"]:.2f}")
        print(f"\t- Min genres: {min(self.results["genre_variety"])}")
        print(f"\t- Max genres: {max(self.results["genre_variety"])}")

        print("\nConfidence Score Statistics:")
        print(f"\t- Average confidence: {self.results["metrics"]["avg_confidence"]:.2%}")
        print(f"\t- Standard Deviation: {self.results["metrics"]["std_confidence"]:.2%}")
        print(f"\t- Min confidence: {min(self.results["confidence_scores"]):.2%}")
        print(f"\t- Max confidence: {max(self.results["confidence_scores"]):.2%}")

        print("\nRating Statistics:")
        print(f"\t- Average rating: {self.results["metrics"]["avg_rating"]:.2f}")
        print(f"\t- Standard Deviation: {self.results["metrics"]["std_rating"]:.2f}")
        print(f"\t- Min rating: {min(self.results["rating_distribution"]):.2f}")
        print(f"\t- Max rating: {max(self.results["rating_distribution"]):.2f}")


        print("\nTop 5 Most Recommended Genre Combinations:")
        sorted_genres = sorted(self.results["genre_distribution"].items(), key=lambda x: x[1], reverse=True)[:5]
        for genre, count in sorted_genres:
            print(f"\t- {genre}: {count} recommendations")

        print("\nRecommendation Quality Metrics:")
        print(f"\t- Average Precision: {self.results["metrics"]["avg_precision"]:.2%}")
        print(f"\t- Average Recall: {self.results["metrics"]["avg_recall"]:.2%}")
        print(f"\t- Average F1 Score: {self.results["metrics"]["avg_f1"]:.2%}")

def load_or_generate_testcases(cwd = "../evaluation/"):
    if not os.path.exists(cwd + "testcases.json"):
        print("Generating test cases...")

        with open(cwd + "preferences.json", "r") as f:
            preferences = json.load(f)

        test_cases = []

        for mood in preferences["moods"]:
            for era in preferences["eras"]:
                for language in preferences["languages"]:
                    for n in range(1, 5):
                        for genre_combo in combinations(preferences["genres"], n):
                            test_case = {
                                "mood": mood,
                                "era": era,
                                "language": language,
                                "genres": list(genre_combo),
                                "additionalNotes": ""
                            }
                            test_cases.append(test_case)

        with open(cwd + "testcases.json", "w") as f:
            json.dump(test_cases, f, indent=2)

    with open(cwd + "testcases.json", "r") as f:
        test_cases_raw = json.load(f)
        test_cases = [GetMovieRecommendationsInput(**tc) for tc in test_cases_raw]

    return test_cases

def reduce_dataset(dataset_path, reduced_path, percent):
    df = pd.read_csv(dataset_path)
    df = df.sample(frac=percent, random_state=42)
    df.to_csv(reduced_path)

def main():
    if len(sys.argv) != 3 and len(sys.argv) != 4:
        print("Usage: python evaluation.py <dataset_percent> <iterations_per_test> <num_test_cases (optional)>")
        print("Example: python evaluation.py 0.1 3 50")
        sys.exit(1)

    test_cases = load_or_generate_testcases()

    dataset_percent = float(sys.argv[1])
    iterations_per_test = int(sys.argv[2])
    num_test_cases = int(sys.argv[3]) if len(sys.argv) == 4 else len(test_cases)

    test_cases = np.random.choice(np.array(test_cases), size=num_test_cases, replace=False)

    original_path = "../data/movies_dataset_preprocessed.csv"
    reduced_path = "../data/movies_dataset_preprocessed_reduced.csv"

    if not os.path.exists(original_path):
        print(f"Dataset not found: {original_path}")
        print("Please fetch dataset and preprocess it before running evaluation (see README.md)")
        sys.exit(1)

    reduce_dataset(original_path, reduced_path, dataset_percent)

    recommender = MovieRecommender(dataset_path=reduced_path)
    evaluator = MovieRecommenderEvaluation(recommender)

    evaluator.run(test_cases, num_iterations=iterations_per_test)
    evaluator.save()
    evaluator.summary()

if __name__ == "__main__":
    main()
