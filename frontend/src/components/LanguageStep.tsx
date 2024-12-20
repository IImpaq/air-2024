"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { LanguageOption } from "@/lib/types";

interface LanguageStepProps {
  languages: LanguageOption[];
  value: string;
  onChange: (id: string) => void;
}

const LanguageStep = ({ languages, value, onChange }: LanguageStepProps) => {
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
          <motion.div
            className={`w-full p-6 rounded-xl transition-all duration-300
            ${value === language.id ? "bg-slate-900 text-white shadow-lg" : "bg-white hover:bg-slate-50"}`}
          >
            <div className="flex items-center space-x-4">
              <div
                className={`p-2 rounded-lg ${value === language.id ? "bg-white/10" : "bg-slate-100 group-hover:bg-slate-200"}`}
              >
                <span
                  className={
                    value === language.id ? "text-white" : "text-slate-600"
                  }
                >
                  {language.icon}
                </span>
              </div>

              <h3
                className={`font-medium justify-center align-center ${value === language.id ? "text-white" : "text-slate-900"}`}
              >
                {language.label}
              </h3>
            </div>
          </motion.div>
        </motion.button>
      ))}
    </div>
  );
};

export default LanguageStep;
