"use client";

import {useState} from "react";
import {motion} from "framer-motion";
import {LanguageOption} from "@/lib/types";

interface LanguageStepProps {
  languages: LanguageOption[];
  value: string;
  onChange: (id: string) => void;
}

const LanguageStep = ({languages, value, onChange}: LanguageStepProps) => {
  const [hoveredOption, setHoveredOption] = useState<string | null>(null);

  return (
      <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
        {languages.map((language) => (
            <motion.button
                key={language.id}
                onClick={() => onChange(language.id)}
                onHoverStart={() => setHoveredOption(language.id)}
                onHoverEnd={() => setHoveredOption(null)}
                className="group relative text-left"
            >
              <motion.div className={`w-full p-6 rounded-xl transition-all duration-300
            ${value === language.id ? 'bg-slate-900 text-white shadow-lg' : 'bg-white hover:bg-slate-50'}`}
                          whileHover={{y: -2}}
                          whileTap={{y: 0}}
              >
                <div className="flex items-start space-x-4">
                  <div
                      className={`p-2 rounded-lg ${value === language.id ? 'bg-white/10' : 'bg-slate-100 group-hover:bg-slate-200'}`}>
                <span className={value === language.id ? 'text-white' : 'text-slate-600'}>
                  {language.icon}
                </span>
                  </div>

                  <div className="flex-1">
                    <h3 className={`font-medium align-center ${value === language.id ? 'text-white' : 'text-slate-900'}`}>
                      {language.label}
                    </h3>

                    <motion.p initial={{height: 0, opacity: 0}}
                              animate={{
                                height: hoveredOption === language.id || value === language.id ? 'auto' : 0,
                                opacity: hoveredOption === language.id || value === language.id ? 1 : 0
                              }}
                              transition={{duration: 0.2}}
                              className={`text-sm mt-2 ${value === language.id ? 'text-slate-300' : 'text-slate-600'}`}
                    >
                      {language.description}
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
