import {Movie} from "@/lib/types";

interface GetMovieRecommendationsInput {
    mood: string;
    era: string;
    language: string;
    additionalNotes: string;
    genres: string[];
}

interface GetMovieRecommendationsResponse {
    movies: Movie[];
}

export const getMovieRecommendation = async (body: GetMovieRecommendationsInput): Promise<GetMovieRecommendationsResponse | null> => {
    const baseUrl = "http://127.0.0.1:8000"
    const endpoint = "/movieRecommendation"
    try {
        console.log("getMovieRecommendation", body);
        const response = await fetch(baseUrl + endpoint, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
            },
            body: JSON.stringify(body),
        });

        if (!response.ok) {
            throw new Error("Failed to fetch recommendations");
        }

        const responseData = await response.json();
        console.log("getMovieRecommendation Response:", responseData);
        return responseData;
    } catch (error) {
        console.error("Error fetching getMovieRecommendation:", error);
        return null;
    }
};