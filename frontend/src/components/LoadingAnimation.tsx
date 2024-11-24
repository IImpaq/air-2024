"use client";

import {motion} from "framer-motion";

const AnimatedStatus = () => {
  const messages = [
    "Analyzing your preferences...",
    "Exploring movie databases...",
    "Finding hidden gems...",
    "Creating recommendations..."
  ];

  return (
      <>
        {messages.map((message, i) => (
            <motion.p key={message}
                      className="absolute inset-0 text-slate-400 text-sm font-medium"
                      initial={{opacity: 0, y: 10}}
                      animate={{
                        opacity: [0, 1, 1, 0],
                        y: [10, 0, 0, -10],
                      }}
                      transition={{
                        duration: 2,
                        delay: i * 2,
                        repeat: Infinity,
                        repeatDelay: (messages.length - 1) * 2,
                      }}
            >
              {message}
            </motion.p>
        ))}
      </>
  );
};

const LoadingAnimation = () => {
  return (
      <motion.div initial={{opacity: 0}}
                  animate={{opacity: 1}}
                  exit={{opacity: 0}}
                  className="col-span-2 md:col-span-3 lg:col-span-4 h-[60vh] flex items-center justify-center"
      >
        <div className="relative w-[500px] h-[500px] flex items-center justify-center">
          <div className="relative w-[400px] h-[400px]">
            <motion.div className="absolute inset-0 rounded-full"
                        style={{
                          background: `
                            radial-gradient(circle at center, 
                                transparent 20%, 
                                rgba(148, 163, 184, 0.1) 30%,
                                rgba(148, 163, 184, 0.3) 35%,
                                rgba(148, 163, 184, 0.4) 40%,
                                rgba(71, 85, 105, 0.4) 50%,
                                rgba(71, 85, 105, 0.2) 60%,
                                rgba(71, 85, 105, 0.1) 65%,
                                transparent 70%
                            )
                          `,
                          filter: "blur(40px) brightness(1.1)",
                        }}
                        animate={{
                          rotate: 360,
                          scale: [1, 1.15, 0.9, 1.1, 0.95, 1],
                          borderRadius: ["50%", "30%", "70%", "35%", "65%", "50%"],
                        }}
                        transition={{
                          duration: 6,
                          repeat: Infinity,
                          ease: "easeInOut",
                        }}
            />

            <motion.div className="absolute inset-0 flex items-center justify-center">
              <motion.div className="text-center z-10 space-y-6"
                          initial={{opacity: 0, scale: 0.9}}
                          animate={{opacity: 1, scale: 1}}
                          transition={{delay: 0.2}}
              >
                <h3 className="text-2xl font-semibold text-slate-600">
                  Curating Movies
                </h3>
                <div className="h-6 relative">
                  <AnimatedStatus/>
                </div>
              </motion.div>
            </motion.div>
          </div>
        </div>
      </motion.div>
  );
};

export default LoadingAnimation;
