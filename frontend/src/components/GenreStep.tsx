"use client";

import {motion} from "framer-motion";
import {
  HiBolt, HiClock,
  HiFaceSmile,
  HiFilm, HiFire, HiHeart,
  HiHome, HiMagnifyingGlass,
  HiMap, HiMusicalNote,
  HiPaintBrush, HiRocketLaunch, HiShieldCheck,
  HiShieldExclamation, HiSparkles, HiSun,
  HiVideoCamera, HiPuzzlePiece, HiOutlineClipboardDocumentList, HiTrophy, HiBell
} from "react-icons/hi2";

interface GenreStepProps {
  selectedGenres: string[];
  onGenreToggle: (genre: string) => void;
}

export const GenreStep = ({selectedGenres, onGenreToggle}: GenreStepProps) => {
  // Some ideas for genres which could be used is from:
  // - Wikipedia: https://en.wikipedia.org/wiki/History_of_film
  // - IMDB: https://www.imdb.com/feature/genre/
  const genres = [
    {
      name: "Action",
      icon: <HiBolt className="w-5 h-5"/>
    },
    {
      name: "Adventure",
      icon: <HiMap className="w-5 h-5"/>
    },
    {
      name: "Animation",
      icon: <HiPaintBrush className="w-5 h-5"/>
    },
    {
      name: "Comedy",
      icon: <HiFaceSmile className="w-5 h-5"/>
    },
    {
      name: "Crime",
      icon: <HiShieldExclamation className="w-5 h-5"/>
    },
    {
      name: "Documentary",
      icon: <HiVideoCamera className="w-5 h-5"/>
    },
    {
      name: "Drama",
      icon: <HiFilm className="w-5 h-5"/>
    },
    {
      name: "Family",
      icon: <HiHome className="w-5 h-5"/>
    },
    {
      name: "Fantasy",
      icon: <HiSparkles className="w-5 h-5"/>
    },
    {
      name: "Game Show",
      icon: <HiOutlineClipboardDocumentList className="w-5 h-5" />
    },
    {
      name: "Historical",
      icon: <HiClock className="w-5 h-5"/>
    },
    {
      name: "Horror",
      icon: <HiPuzzlePiece className="w-5 h-5"/>
    },
    {
      name: "Musical",
      icon: <HiMusicalNote className="w-5 h-5"/>
    },
    {
      name: "Mystery",
      icon: <HiMagnifyingGlass className="w-5 h-5"/>
    },
    {
      name: "Reality TV",
      icon: <HiShieldExclamation className="w-5 h-5"/>
    },
    {
      name: "Romance",
      icon: <HiHeart className="w-5 h-5"/>
    },
    {
      name: "Seasonal",
      icon: <HiBell className="w-5 h-5" />
    },
    {
      name: "Science Fiction",
      icon: <HiRocketLaunch className="w-5 h-5"/>
    },
    {
      name: "Sport",
      icon: <HiTrophy className="w-5 h-5"/>
    },
    {
      name: "Thriller",
      icon: <HiFire className="w-5 h-5"/>
    },
    {
      name: "War",
      icon: <HiShieldCheck className="w-5 h-5"/>
    },
    {
      name: "Western",
      icon: <HiSun className="w-5 h-5"/>
    }
  ];

  return (
      <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
        {genres.map((genre) => (
            <motion.button
                key={genre.name}
                onClick={() => onGenreToggle(genre.name)}
                className={`p-4 rounded-xl text-sm font-medium transition-all
                            ${selectedGenres.includes(genre.name)
                    ? "bg-slate-900 text-white shadow-lg"
                    : "bg-white text-slate-600 hover:bg-slate-100"
                }`}
                whileHover={{scale: 1.02}}
                whileTap={{scale: 0.98}}
            >
              <div className="flex items-center space-x-2">
                <span>{genre.icon}</span>
                <span>{genre.name}</span>
              </div>
            </motion.button>
        ))}
      </div>
  )
}

export default GenreStep;
