"use client";

import {motion} from "framer-motion";

interface NotesStepProps {
  value: string;
  onChange: (value: string) => void;
}

export const NotesStep = ({value, onChange}: NotesStepProps) => {
  return (
      <div className="bg-slate-50 rounded-2xl p-6">
        <motion.div initial={{opacity: 0, y: 10}}
                    animate={{opacity: 1, y: 0}}
                    className="space-y-4"
        >
        <textarea value={value}
                  onChange={(e) => onChange(e.target.value)}
                  placeholder="For example: I enjoy movies with unexpected plot twists, specific actors or beautiful landscapes. I prefer avoiding excessive violence..."
                  className="w-full h-32 p-4 rounded-xl bg-white text-slate-600 placeholder:text-slate-400 border-2 border-transparent focus:border-slate-200 focus:ring-0 resize-none"
        />
          <p className="text-sm text-slate-500">
            This helps us better understand your preferences and provide more personalized recommendations.
          </p>
        </motion.div>
      </div>
  );
};

export default NotesStep;
