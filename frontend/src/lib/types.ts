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
  year: number;
  poster: string;
  rating: number;
  genre?: string;
  duration?: string;
  summary?: string;
}
