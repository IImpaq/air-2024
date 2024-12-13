export interface LanguageOption {
  id: string;
  label: string;
  description: string;
  icon: JSX.Element;
}

export interface PreferenceStep {
  genres: string[];
  mood: string;
  era: string;
  language: string;
  additionalNotes: string;
}

export interface Movie {
  id: string;
  title: string;
  genre: string;
  rating: number;
  year: number;
  poster: string;
  confidence: number;
  duration?: string;
  summary?: string;
}


