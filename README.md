<h1 align="center">Movie Finder 🎞️</h1>

A intelligent movie recommendation system that uses advanced techniques to recommend movies based on your preferences.

## ✨ Key Features

- Platform-independent movie recommendations
- Genre Selection
- Mood Choice
- Era Timeframe Options
- Language Decision
- Notes for in-depth personalization

## 🚀 Getting Started

```bash
# Clone the repository
git clone git@github.com:IImpaq/air-2024.git

# Change directory
cd air-2024

# Install backend requirements
cd backend && pip install -r requirements.txt && cd ..

# Install frontend requirements
cd frontend && bun install && cd ..

# Fetch & preprocess data
cd backend && python fetch.py && python preprocess.py && cd ..

### To run the full-stack application locally, follow the instructions below:
# Launch Frontend
cd frontend && bun run dev

# Launch backend
cd backend && uvicorn main:app --reload

### To run the recommender system as a cli app, follow the instructions below:
# Launch the recommender system
cd backend && python cli.py
```

## 🛠️ Tech Stack

- Frontend: NextJS & TypeScript
- Backend: Python, FastAPI & PyTorch

## 📝 License
TODO Add license

## 🔗 Links

- [Design Document](design-document/design-document.pdf)
- [Report](report/report.pdf)
- [Presentation](presentation/presentation.pdf)

---
Made with ❤️
