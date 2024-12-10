"use client";

import {useEffect, useState} from "react";
import {
  HiLanguage
} from "react-icons/hi2";
import {motion} from "framer-motion";
import {LanguageOption} from "@/lib/types";
import {getAvailableLanguages} from "@/api/getAvailableLanguages";

interface LanguageStepProps {
  value: string;
  onChange: (id: string) => void;
}

const LanguageStep = ({value, onChange}: LanguageStepProps) => {
  const [hoveredOption, setHoveredOption] = useState<string | null>(null);
  const [options, setOptions] = useState<LanguageOption[]>([]);

  // Fetch languages from getAvailableLanguages() once on first time
  useEffect(() => {
    getAvailableLanguages().then(response => {
      if (response) {
        console.log("Available Languages:", response.languages);
        setOptions(response.languages.map((language) => {
          const languageLabel = new Intl.DisplayNames(['en'], {type: 'language'}).of(language)?.toString() || language;

          return {
            id: language,
            label: languageLabel,
            description: `Films originally produced in ${languageLabel}`,
            icon: <HiLanguage className="w-5 h-5"/>,
          };
        }));
      }
    });
  }, []);

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
      {options.map((option) => (
        <motion.button
            key={option.id}
            onClick={() => onChange(option.id)}
            onHoverStart={() => setHoveredOption(option.id)}
            onHoverEnd={() => setHoveredOption(null)}
            className="group relative text-left"
        >
          <motion.div className={`w-full p-6 rounded-xl transition-all duration-300
            ${value === option.id ? 'bg-slate-900 text-white shadow-lg' : 'bg-white hover:bg-slate-50'}`}
                      whileHover={{y: -2}}
                      whileTap={{y: 0}}
          >
            <div className="flex items-start space-x-4">
              <div
                  className={`p-2 rounded-lg ${value === option.id ? 'bg-white/10' : 'bg-slate-100 group-hover:bg-slate-200'}`}>
                <span className={value === option.id ? 'text-white' : 'text-slate-600'}>
                  {option.icon}
                </span>
              </div>

              <div className="flex-1">
                <h3 className={`font-medium align-center ${value === option.id ? 'text-white' : 'text-slate-900'}`}>
                  {option.label}
                </h3>

                <motion.p initial={{height: 0, opacity: 0}}
                          animate={{
                            height: hoveredOption === option.id || value === option.id ? 'auto' : 0,
                            opacity: hoveredOption === option.id || value === option.id ? 1 : 0
                          }}
                          transition={{duration: 0.2}}
                          className={`text-sm mt-2 ${value === option.id ? 'text-slate-300' : 'text-slate-600'}`}
                >
                  {option.description}
                </motion.p>
              </div>
            </div>
          </motion.div>
        </motion.button>
      ))}
    </div>
  );
}

export default LanguageStep;
