interface GetVailableGenresResponse {
  genres: string[];
}

export const getAvailableGenres =
  async (): Promise<GetVailableGenresResponse | null> => {
    const baseUrl = "http://127.0.0.1:8000";
    const endpoint = "/availableGenres";
    try {
      console.log("getAvailableGenres");
      const response = await fetch(baseUrl + endpoint, {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Failed to fetch genres");
      }

      const responseData = await response.json();
      console.log("getAvailableGenres Response:", responseData);
      return responseData;
    } catch (error) {
      console.error("Error fetching getAvailableGenres:", error);
      return null;
    }
  };
