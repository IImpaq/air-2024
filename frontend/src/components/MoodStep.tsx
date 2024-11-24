"use client";

import {motion} from "framer-motion";
import {
  HiBolt,
  HiClock,
  HiCloud, HiCloudArrowDown,
  HiFaceSmile,
  HiHeart, HiLightBulb,
  HiMoon, HiOutlineHeart,
  HiQuestionMarkCircle,
  HiSparkles,
  HiSun
} from "react-icons/hi2";

interface MoodStepProps {
  selectedMood: string;
  onMoodSelect: (mood: string) => void;
}

export const MoodStep = ({selectedMood, onMoodSelect}: MoodStepProps) => {
  const moods = [
    {
      name: "Dark",
      icon: <HiMoon className="w-5 h-5"/>
    },
    {
      name: "Emotional",
      icon: <HiHeart className="w-5 h-5"/>
    },
    {
      name: "Humorous",
      icon: <HiFaceSmile className="w-5 h-5"/>
    },
    {
      name: "Inspiring",
      icon: <HiSparkles className="w-5 h-5"/>
    },
    {
      name: "Intense",
      icon: <HiBolt className="w-5 h-5"/>
    },
    {
      name: "Melancholic",
      icon: <HiCloudArrowDown className="w-5 h-5"/>
    },
    {
      name: "Mysterious",
      icon: <HiQuestionMarkCircle className="w-5 h-5"/>
    },
    {
      name: "Relaxing",
      icon: <HiCloud className="w-5 h-5"/>
    },
    {
      name: "Romantic",
      icon: <HiOutlineHeart className="w-5 h-5"/>
    },
    {
      name: "Suspenseful",
      icon: <HiClock className="w-5 h-5"/>
    },
    {
      name: "Thought-provoking",
      icon: <HiLightBulb className="w-5 h-5"/>
    },
    {
      name: "Uplifting",
      icon: <HiSun className="w-5 h-5"/>
    }
  ];

  return (
      <div className="grid grid-cols-2 md:grid-cols-3 gap-3">
        {moods.map((mood) => (
            <motion.button
                key={mood.name}
                onClick={() => onMoodSelect(mood.name)}
                className={`p-4 rounded-xl text-sm font-medium transition-all
                  ${selectedMood === mood.name
                    ? "bg-slate-900 text-white shadow-lg"
                    : "bg-white text-slate-600 hover:bg-slate-100"
                }`}
                whileHover={{scale: 1.02}}
                whileTap={{scale: 0.98}}
            >
              <div className="flex items-center space-x-2">
                <span>{mood.icon}</span>
                <span>{mood.name}</span>
              </div>
            </motion.button>
        ))}
      </div>
  );
};

export default MoodStep;
