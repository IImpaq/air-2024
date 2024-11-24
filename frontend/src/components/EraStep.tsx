"use client";

import {useState} from "react";
import {motion} from "framer-motion";

interface EraStepProps {
  value: string;
  onChange: (era: string) => void;
}

const EraStep = ({value, onChange}: EraStepProps) => {
  const [hoveredEra, setHoveredEra] = useState<string | null>(null);

  // Information is mostly sourced from Wikipedia:
  // https://en.wikipedia.org/wiki/History_of_film
  const eras = [
    {
      "id": "silent",
      "name": "Silent Era",
      "years": "1895 - 1927",
      "description": "Early cinema, pioneering filmmaking, and silent masterpieces",
      "icon": "🎥"
    },
    {
      "id": "golden",
      "name": "Golden Age",
      "years": "1927 - 1948",
      "description": "Studio system era, classic Hollywood, and rise of the talkies",
      "icon": "✨"
    },
    {
      "id": "postwar",
      "name": "Post-War Era",
      "years": "1948 - 1965",
      "description": "Fall of studio system, film noir, and international cinema",
      "icon": "🌟"
    },
    {
      "id": "new",
      "name": "New Hollywood",
      "years": "1965 - 1983",
      "description": "Auteur filmmaking, counterculture, and rise of blockbusters",
      "icon": "🎬"
    },
    {
      "id": "blockbuster",
      "name": "Blockbuster Era",
      "years": "1983 - 1999",
      "description": "High-concept films, special effects, and franchise movies",
      "icon": "💫"
    },
    {
      "id": "digital",
      "name": "Digital Age",
      "years": "2000 - 2010",
      "description": "Digital filmmaking, streaming platforms, and global cinema",
      "icon": "🎯"
    },
    {
      "id": "streaming",
      "name": "Streaming Era",
      "years": "2010 - Now",
      "description": "Service originals, direct-to-streaming releases, and platform wars",
      "icon": "📱"
    },
    {
      "id": "any",
      "name": "All Eras",
      "years": "Any Time",
      "description": "Films from all periods of cinema history",
      "icon": "🎪"
    }
  ];

  return (
      <div className="space-y-3">
        {eras.map((era) => (
            <motion.button key={era.id}
                           onClick={() => onChange(era.id)}
                           onHoverStart={() => setHoveredEra(era.id)}
                           onHoverEnd={() => setHoveredEra(null)}
                           className="w-full group relative"
            >
              <motion.div className={`w-full p-6 rounded-xl transition-all duration-300
          ${value === era.id
                  ? "bg-slate-900 text-white shadow-lg"
                  : "bg-white hover:bg-slate-50"
              }`}
                          whileHover={{y: -2}}
                          whileTap={{y: 0}}
              >
                <div className="flex items-start space-x-4">
                  <span className="text-2xl">{era.icon}</span>

                  <div className="flex-1 text-left">
                    <div className="flex items-center justify-between">
                      <h3 className={`font-medium ${value === era.id ? "text-white" : "text-slate-900"}`}>
                        {era.name}
                      </h3>
                      <span className={`text-sm ${value === era.id ? "text-slate-300" : "text-slate-500"}`}>
                    {era.years}
                  </span>
                    </div>

                    <motion.p initial={{height: 0, opacity: 0}}
                              animate={{
                                height: hoveredEra === era.id || value === era.id ? "auto" : 0,
                                opacity: hoveredEra === era.id || value === era.id ? 1 : 0
                              }}
                              transition={{duration: 0.2}}
                              className={`text-sm mt-2 ${value === era.id ? "text-slate-300" : "text-slate-600"}`}
                    >
                      {era.description}
                    </motion.p>
                  </div>
                </div>
              </motion.div>
            </motion.button>
        ))}

        <div className="mt-6 px-4 py-8">
          <div className="h-1 bg-slate-200 rounded-full relative">
            {eras.slice(0, -1).map((era, index) => (
                <div key={era.id}
                     className="absolute flex flex-col items-center -translate-x-1/2"
                     style={{
                       left: `${(index / (eras.slice(0, -1).length - 1)) * 100}%`
                     }}
                >
                  <motion.div
                      className={`w-3 h-3 cursor-pointer rounded-full -mt-1 ${(value === era.id || value === "any") ? "bg-slate-900" : "bg-slate-400"}`}
                      whileHover={{scale: 1.2}}
                      onClick={() => onChange(era.id)}
                  />
                  <span className="text-xs text-slate-600 whitespace-nowrap mt-2">
                    {era.years}
                  </span>
                </div>
            ))}
          </div>
        </div>
      </div>
  );
}

export default EraStep;
