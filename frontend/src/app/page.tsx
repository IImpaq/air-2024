"use client";

import {useState} from "react";
import {motion, AnimatePresence} from "framer-motion";
import {HiOutlineFilm} from "react-icons/hi";
import PreferenceForm from "@/components/PreferenceForm";
import ResultsStep from "@/components/ResultsStep";
import {Movie, PreferenceStep} from "@/lib/types";
import {getMovieRecommendation} from "@/api/getMovieRecommendations";

const Home = () => {
  const [step, setStep] = useState<"landing" | "preferences" | "results">("landing");
  const [movies, setMovies] = useState<Movie[]>([]);

  const onSubmit = async (preferences: PreferenceStep) => {
      const response = await getMovieRecommendation({
          genres: preferences.genres,
          mood: preferences.mood,
          language: preferences.language,
          additionalNotes: preferences.additionalNotes,
          era: preferences.era
      });

      if(response == null){
          // handle error case
          return;
      }

      const movies = response?.movies ?? [];
      setMovies(movies);
      setStep("results");

  }
  return (
      <main className="min-h-screen bg-slate-50 relative overflow-hidden">
        <div className="container mx-auto px-4 py-16 relative">
          <AnimatePresence mode="wait">
            {step === "landing" && (
                <motion.div key="landing"
                            initial={{opacity: 0, y: 20}}
                            animate={{opacity: 1, y: 0}}
                            exit={{opacity: 0, y: -20}}
                            transition={{duration: 0.4}}
                            className="flex flex-col items-center justify-center min-h-[80vh]"
                >
                  <motion.div initial={{y: 20, opacity: 0}}
                              animate={{y: 0, opacity: 1}}
                              transition={{delay: 0.1, duration: 0.4}}
                              className="mb-8"
                  >
                    <div className="inline-block p-4 rounded-2xl bg-white shadow-xl mb-6">
                      <HiOutlineFilm className="w-16 h-16 text-slate-800"/>
                    </div>
                  </motion.div>

                  <motion.h1 initial={{y: 20, opacity: 0}}
                             animate={{y: 0, opacity: 1}}
                             transition={{delay: 0.2, duration: 0.4}}
                             className="text-6xl font-bold text-slate-900 mb-6 tracking-tight text-center"
                  >
                    Movie Finder
                  </motion.h1>

                  <motion.p initial={{y: 20, opacity: 0}}
                            animate={{y: 0, opacity: 1}}
                            transition={{delay: 0.3, duration: 0.4}}
                            className="text-xl text-slate-600 mb-12 leading-relaxed max-w-2xl text-center"
                  >
                    Discover your next cinematic experience through the power of AI,<br/>
                    where personalized recommendations are tailored just for you.
                  </motion.p>

                  <motion.div initial={{y: 20, opacity: 0}}
                              animate={{y: 0, opacity: 1}}
                              transition={{delay: 0.4, duration: 0.4}}
                              className="flex flex-col items-center gap-4"
                  >
                    <motion.button whileHover={{scale: 1.02, boxShadow: "0 20px 40px rgba(0,0,0,0.1)"}}
                                   whileTap={{scale: 0.98}}
                                   onClick={() => setStep("preferences")}
                                   className="px-12 py-5 bg-slate-900 text-white rounded-2xl text-lg font-medium shadow-lg transition-all duration-300 hover:bg-slate-800"
                    >
                      Get Started
                    </motion.button>
                    <span className="text-sm text-slate-500 text-center">No account required<br/>Private & Free</span>
                  </motion.div>
                </motion.div>
            )}

            {step === "preferences" && (
                <motion.div key="preferences"
                            initial={{opacity: 0, y: 20}}
                            animate={{opacity: 1, y: 0}}
                            exit={{opacity: 0, y: -20}}
                            transition={{duration: 0.4}}
                            className="max-w-3xl mx-auto"
                >
                  <div className="bg-white rounded-3xl shadow-xl p-8">
                    <motion.h2 initial={{y: 20, opacity: 0}}
                               animate={{y: 0, opacity: 1}}
                               transition={{delay: 0.1, duration: 0.4}}
                               className="text-3xl font-bold text-slate-900 mb-6 text-center"
                    >
                      Tell us your preferences
                    </motion.h2>
                    <PreferenceForm onSubmit={async (pref) => onSubmit(pref)}/>
                  </div>
                </motion.div>
            )}

            {step === "results" && (
                <motion.div key="results"
                            initial={{opacity: 0, y: 20}}
                            animate={{opacity: 1, y: 0}}
                            exit={{opacity: 0, y: -20}}
                            transition={{duration: 0.4}}
                            className="max-w-6xl mx-auto"
                >
                  <div className="bg-white rounded-3xl shadow-xl p-8">
                    <motion.div initial={{y: 20, opacity: 0}}
                                animate={{y: 0, opacity: 1}}
                                transition={{delay: 0.1, duration: 0.4}}
                                className="text-center mb-12"
                    >
                      <h2 className="text-3xl font-bold text-slate-900 mb-4">Your Perfect Matches</h2>
                      <p className="text-slate-600">Based on your preferences, we think you&#39;ll love these films</p>
                    </motion.div>

                    <ResultsStep movies={movies}/>

                    <motion.div initial={{y: 20, opacity: 0}}
                                animate={{y: 0, opacity: 1}}
                                transition={{delay: 0.2, duration: 0.4}}
                                className="text-center mt-12"
                    >
                      <motion.button whileHover={{scale: 1.02}}
                                     whileTap={{scale: 0.98}}
                                     onClick={() => setStep("preferences")}
                                     className="px-8 py-4 bg-slate-100 text-slate-700 rounded-2xl hover:bg-slate-200 transition-all duration-300"
                      >
                        Refine Selection
                      </motion.button>
                    </motion.div>
                  </div>
                </motion.div>
            )}
          </AnimatePresence>
        </div>
      </main>
  );
};

export default Home;
