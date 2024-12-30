"use client";

import { useEffect, useRef, useState } from "react";
import {
  HiStar,
  HiPlay,
  HiOutlineClipboardDocumentList,
  HiXMark,
  HiSignal,
  HiBookOpen,
} from "react-icons/hi2";
import { motion, AnimatePresence } from "framer-motion";
import { Movie, PreferenceStep } from "@/lib/types";
import AILoadingAnimation from "@/components/LoadingAnimation";
import { getMovieDescription } from "@/api/getMovieDescription";
import { getMovieRecommendation } from "@/api/getMovieRecommendations";
import { HiX } from "react-icons/hi";

interface ResultsStep {
  pref: PreferenceStep;
}

const ResultsStep = ({ pref }: ResultsStep) => {
  const [isLoading, setIsLoading] = useState(true);
  const isRequestInProgress = useRef(false);
  const [movies, setMovies] = useState<Movie[]>([]);
  const [showSummary, setShowSummary] = useState<string | null>(null);
  const [isGeneratingSummary, setIsGeneratingSummary] = useState(false);
  const [currentSummary, setCurrentSummary] = useState<string | null>(null);
  const [currentGenres, setCurrentGenres] = useState<string[] | null>([]);
  const [showError, setShowError] = useState(false);

  useEffect(() => {
    const fetchMovies = async () => {
      if (!isLoading || isRequestInProgress.current) return;

      isRequestInProgress.current = true;

      try {
        const response = await getMovieRecommendation({
          genres: pref.genres.map((genre) => genre.toLowerCase()),
          mood: pref.mood.toLowerCase(),
          language: pref.language.toLowerCase(),
          additionalNotes: pref.additionalNotes.toLowerCase(),
          era: pref.era.toLowerCase(),
        });

        if (response == null) {
          setShowError(true);
          return;
        }

        const movies = response?.movies ?? [];

        for (let i = 0; i < movies.length; i++) {
          movies[i].id = i + movies[i].title + movies[i].year;
        }

        setMovies(movies);
      } catch (error) {
        setShowError(true);
      } finally {
        setIsLoading(false);
        isRequestInProgress.current = false;
      }
    };

    fetchMovies();
  }, [isLoading, pref]);

  const container = {
    hidden: { opacity: 0 },
    show: {
      opacity: 1,
      transition: { staggerChildren: 0.1 },
    },
  };

  const item = {
    hidden: { opacity: 0, y: 20 },
    show: { opacity: 1, y: 0 },
  };

  const handleShowSummary = async (movie: Movie) => {
    setShowSummary(movie.id);
    setIsGeneratingSummary(true);
    const response = await getMovieDescription({
      id: movie.id,
      title: movie.title,
      year: movie.year,
    });
    if (!response) {
      setShowError(true);
      return;
    }
    setCurrentSummary(response?.summary ?? null);
    setCurrentGenres(response?.genre ?? null);

    setIsGeneratingSummary(false);
  };

  return (
    <div className="space-y-8">
      <motion.div
        variants={container}
        initial="hidden"
        animate="show"
        className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-6"
      >
        <AnimatePresence mode="wait">
          {isLoading ? (
            <AILoadingAnimation />
          ) : (
            movies.map((movie) => (
              <motion.div
                key={movie.id}
                variants={item}
                className={`relative group ${showSummary === movie.id ? "lg:col-span-2 lg:row-span-2" : ""}`}
                layoutId={`movie-${movie.id}`}
                transition={{ duration: 0.3, ease: "easeInOut" }}
              >
                <div className="relative overflow-hidden rounded-2xl bg-slate-100 h-full">
                  <motion.div
                    className={`aspect-[2/3] relative ${showSummary === movie.id ? "lg:aspect-[16/9]" : ""}`}
                    layoutId={`image-${movie.id}`}
                    transition={{ duration: 0.3, ease: "easeInOut" }}
                  >
                    <img
                      src={"https://image.tmdb.org/t/p/w500" + movie.poster}
                      alt={movie.title}
                      className="w-full h-full object-cover"
                    />

                    {showSummary !== movie.id && (
                      <motion.div
                        initial={{ opacity: 0 }}
                        whileHover={{ opacity: 1 }}
                        className="absolute inset-0 bg-gradient-to-t from-slate-900 via-slate-900/50 to-transparent"
                      >
                        <div className="absolute inset-0 flex items-center justify-center gap-3">
                          <motion.button
                            whileHover={{ scale: 1.1 }}
                            whileTap={{ scale: 0.95 }}
                            onClick={() => handleShowSummary(movie)}
                            className="p-3 rounded-full bg-white/20 text-white backdrop-blur-sm"
                          >
                            <HiBookOpen className="w-6 h-6" />
                          </motion.button>
                        </div>
                      </motion.div>
                    )}

                    <motion.div
                      layoutId={`stats-${movie.title}-${movie.id}`}
                      transition={{ duration: 0.3, ease: "easeInOut" }}
                      className="absolute top-0 left-0 right-0 p-3 text-white bg-gradient-to-b from-slate-900"
                    >
                      <div className="flex items-center justify-end text-sm">
                        <div className="flex items-center">
                          <HiSignal className="w-4 h-4 text-yellow-400 mr-1" />
                          <span>{(movie.confidence * 100).toFixed(0)}%</span>
                        </div>
                      </div>
                    </motion.div>

                    <motion.div
                      layoutId={`info-${movie.title}-${movie.id}`}
                      transition={{ duration: 0.3, ease: "easeInOut" }}
                      className="absolute bottom-0 left-0 right-0 p-4 text-white bg-gradient-to-t from-slate-900"
                    >
                      <h3 className="text-lg font-semibold leading-tight mb-1">
                        {movie.title}
                      </h3>
                      <div className="flex items-center justify-between text-sm">
                        <div className="flex items-center gap-2">
                          <span>{movie.year}</span>
                          {movie.duration && (
                            <span className="text-white/70">
                              {movie.duration}
                            </span>
                          )}
                        </div>
                        <div className="flex items-center">
                          <HiStar className="w-4 h-4 text-yellow-400 mr-1" />
                          <span>{movie.rating.toFixed(1)}</span>
                        </div>
                      </div>
                    </motion.div>
                  </motion.div>

                  <AnimatePresence>
                    {showSummary === movie.id && (
                      <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="p-6 bg-slate-100"
                      >
                        <div className="flex justify-between items-start mb-4">
                          <h3 className="text-lg font-semibold text-slate-700">
                            AI Introduction
                          </h3>
                          <button
                            onClick={() => setShowSummary(null)}
                            className="p-2 rounded-full hover:bg-slate-200"
                          >
                            <HiXMark className="w-5 h-5 text-slate-500" />
                          </button>
                        </div>

                        {isGeneratingSummary ? (
                          <div className="space-y-3">
                            <div className="h-4 bg-slate-200 rounded-full w-3/4 animate-pulse" />
                            <div className="h-4 bg-slate-200 rounded-full animate-pulse" />
                            <div className="h-4 bg-slate-200 rounded-full w-5/6 animate-pulse" />
                          </div>
                        ) : (
                          <>
                            {currentSummary && (
                              <p className="text-slate-600 text-sm leading-relaxed mb-4">
                                {currentSummary}
                              </p>
                            )}
                            <div className="space-y-2">
                              <h4 className="font-medium text-slate-700 text-sm">
                                Key Themes
                              </h4>
                              <div className="flex flex-wrap gap-2">
                                {currentGenres &&
                                  currentGenres.map((theme) => (
                                    <span
                                      key={movie.title + theme}
                                      className="px-2.5 py-1 bg-slate-200 rounded-full text-xs text-slate-600"
                                    >
                                      {theme}
                                    </span>
                                  ))}
                              </div>
                            </div>
                          </>
                        )}
                      </motion.div>
                    )}
                  </AnimatePresence>
                </div>
              </motion.div>
            ))
          )}
        </AnimatePresence>
      </motion.div>

      {showError && (
        <div className="absolute inset-x-0 -bottom-2 flex justify-center">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            transition={{ duration: 0.3 }}
            className="bg-red-500 text-white px-6 py-3 rounded-lg shadow-lg"
          >
            <span>
              Error while trying to generate movie recommendation. Please try
              again later.
            </span>
            <button onClick={() => setShowError(false)} className="ml-4">
              <HiX />
            </button>
          </motion.div>
        </div>
      )}
    </div>
  );
};

export default ResultsStep;
