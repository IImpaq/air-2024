"use client";

import {useState} from "react";
import {HiOutlineEmojiHappy, HiOutlineGlobe} from "react-icons/hi";
import {HiOutlineClock, HiOutlinePencil, HiOutlineTag} from "react-icons/hi2";
import {motion, AnimatePresence} from "framer-motion";
import {PreferenceStep} from "@/lib/types";
import LanguageSelection from "@/components/LanguageSelection";
import EraSelection from "@/components/EraSelection";
import GenreStep from "@/components/GenreStep";
import MoodStep from "@/components/MoodStep";
import NotesStep from "@/components/NotesStep";

interface PreferenceFormProps {
  onSubmit: (preferences: PreferenceStep) => void;
}

const PreferenceForm = ({onSubmit}: PreferenceFormProps) => {
  const [step, setStep] = useState(1);
  const [preferences, setPreferences] = useState<PreferenceStep>({
    genres: [],
    mood: "",
    era: "",
    language: "",
    additionalNotes: ""
  });

  const stepDetails = [
    {
      title: "What genres interest you?",
      description: "Select multiple genres that catch your attention",
      icon: <HiOutlineTag className="w-6 h-6 text-slate-700"/>
    },
    {
      title: "What's your preferred mood?",
      description: "Pick the type of experience you're looking for",
      icon: <HiOutlineEmojiHappy className="w-6 h-6 text-slate-700"/>
    },
    {
      title: "Choose your favorite era",
      description: "Tell us which time period interests you most",
      icon: <HiOutlineClock className="w-6 h-6 text-slate-700"/>
    },
    {
      title: "Language preferences",
      description: "Choose your preferred viewing language",
      icon: <HiOutlineGlobe className="w-6 h-6 text-slate-700"/>
    },
    {
      title: "Any additional preferences?",
      description: "Optional: Tell us more about what you're looking for",
      icon: <HiOutlinePencil className="w-6 h-6 text-slate-700"/>
    }
  ]

  const handleNext = () => {
    if (step === 5) {
      onSubmit(preferences);
      return;
    }
    setStep(prev => prev + 1);
  };

  return (
      <div className="w-full">
        <div className="flex space-x-2 mb-8">
          {[1, 2, 3, 4, 5].map((i) => (
              <div key={i} className="flex-1">
                <motion.div className="h-1 rounded-full bg-slate-200" initial={false}>
                  <motion.div className="h-full rounded-full bg-slate-800"
                              initial={{scaleX: 0}}
                              animate={{
                                scaleX: step >= i ? 1 : 0,
                                transition: {
                                  duration: 0.3,
                                  delay: step >= i ? (i - Math.min(step - 1, i)) * 0.1 : 0
                                }
                              }}
                              style={{originX: 0}}
                  />
                </motion.div>
              </div>
          ))}
        </div>

        <AnimatePresence mode="wait">
          <motion.div key={step}
                      initial={{opacity: 0, y: 20}}
                      animate={{opacity: 1, y: 0}}
                      exit={{opacity: 0, y: -20}}
                      transition={{duration: 0.3}}
                      className="space-y-8"
          >
            <div className="text-center space-y-2">
              <div className="inline-block p-3 bg-slate-100 rounded-xl mb-4">
                {stepDetails[step - 1].icon}
              </div>

              <h2 className="text-2xl font-semibold text-slate-900">
                {stepDetails[step - 1].title}
              </h2>

              <p className="text-slate-600">
                {stepDetails[step - 1].description}
              </p>
            </div>

            <div className="bg-slate-50 rounded-2xl p-6">
              {step === 1 && (
                  <GenreStep selectedGenres={preferences.genres}
                             onGenreToggle={(genre: string) => setPreferences(prev => ({
                               ...prev,
                               genres: prev.genres.includes(genre)
                                   ? prev.genres.filter(g => g !== genre)
                                   : [...prev.genres, genre]
                             }))}/>
              )}

              {step === 2 && (
                  <MoodStep selectedMood={preferences.mood}
                            onMoodSelect={(mood: string) => setPreferences(prev => ({...prev, mood}))}/>
              )}

              {step === 3 && (
                  <EraSelection value={preferences.era}
                                onChange={(era) => setPreferences(prev => ({...prev, era}))}
                  />
              )}

              {step === 4 && (
                  <LanguageSelection value={preferences.language}
                                     onChange={(language) => setPreferences(prev => ({
                                       ...prev,
                                       language
                                     }))}
                  />
              )}

              {step === 5 && (
                  <NotesStep value={preferences.additionalNotes}
                             onChange={(value) => setPreferences(prev => ({...prev, additionalNotes: value}))}
                  />
              )}
            </div>
          </motion.div>
        </AnimatePresence>

        <div className="flex justify-between mt-8">
          <motion.button whileHover={{scale: 1.02}}
                         whileTap={{scale: 0.98}}
                         onClick={() => setStep(prev => Math.max(1, prev - 1))}
                         className={`px-8 py-4 rounded-xl font-medium transition-all ${step === 1 ? "bg-slate-100 text-slate-400 cursor-not-allowed" : "bg-slate-100 text-slate-600 hover:bg-slate-200"}`}
                         disabled={step === 1}
          >
            Back
          </motion.button>

          <motion.button whileHover={{scale: 1.02}}
                         whileTap={{scale: 0.98}}
                         onClick={handleNext}
                         className="px-8 py-4 bg-slate-900 text-white rounded-xl font-medium shadow-lg hover:bg-slate-800 transition-all"
          >
            {step === 5 ? "Find Movies" : "Continue"}
          </motion.button>
        </div>
      </div>
  );
}

export default PreferenceForm;
