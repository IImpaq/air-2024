interface GetMovieDescriptionInput {
    id: string;
    title: string;
    year: number;
}

interface GetMovieDescriptionResponse {
    genre: string[];
    summary: string;
}

export const getMovieDescription = async (body: GetMovieDescriptionInput): Promise<GetMovieDescriptionResponse | null> => {
    const baseUrl = "http://127.0.0.1:8000";
    const endpoint = "/movieDescription"

    try {
        console.log("getMovieDescription", body);
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
        console.log("getMovieDescription Response:", responseData);
        return responseData;
    } catch (error) {
        console.error("Error fetching getMovieDescription:", error);
        return null;
    }
};