interface GetAvailableLanguagesResponse {
    languages: string[];
}

export const getAvailableLanguages = async (): Promise<GetAvailableLanguagesResponse | null> => {
    const baseUrl = "http://127.0.0.1:8000"
    const endpoint = "/availableLanguages"
    try {
        console.log("getAvailableLanguages");
        const response = await fetch(baseUrl + endpoint, {
            method: "GET",
            headers: {
                "Content-Type": "application/json",
            }
        });

        if (!response.ok) {
            throw new Error("Failed to fetch recommendations");
        }

        const responseData = await response.json();
        console.log("getAvailableLanguages Response:", responseData);
        return responseData;
    } catch (error) {
        console.error("Error fetching getAvailableLanguages:", error);
        return null;
    }
};