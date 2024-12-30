<h1 align="center">Movie Finder 🎞️</h1>

A intelligent movie recommendation system that uses advanced techniques to recommend movies based on your preferences.

<p align="center">
  <img src="assets/hero.gif" alt="Hero Trailer Video" width="600px">
</p>

## ✨ Key Features

- Platform-independent movie recommendations
- Genre Selection
- Mood Choice
- Era Timeframe Options
- Language Decision
- Notes for in-depth personalization

## 🚀 Getting Started

### Prerequisites

- Git
- Bun.js
- Python 3.12

### Installation

```bash
# Clone the repository
git clone git@github.com:IImpaq/air-2024.git
cd air-2024

# Prepare the backend
cd backend
pip install -r requirements.txt
python fetch.py      # Fetch dataset from huggingface
python preprocess.py # Prepare and preprocess the data
cd ..

# Prepare the frontend
cd frontend
bun install
cd ..
```

### Running

**Full-Stack Application**

```bash
# Terminal 1: Start Frontend
cd frontend
bun run dev # Website Available at http://localhost:3000

# Terminal 2: Start Backend
cd backend
uvicorn main:app --reload  # API available at http://localhost:8000
```

**CLI Mode**

```bash
# Run backend/movie recommender in interactive cli mode
cd backend
python cli.py
```

**Evaluate the recommender system**

```bash
# Run the automated evaluation script
cd backend
python evaluation.py
```

## 🛠️ Tech Stack

- Frontend: NextJS & TypeScript
- Backend: Python, FastAPI & PyTorch

## 📝 License

MIT License (see [LICENSE.MD](LICENSE.md)).

## 🔗 Links

- [Design Document](design-document/design-document.pdf)
- [Report](report/report.pdf)
- [Presentation](presentation/presentation.pdf)
- [Questionnaire](questionnaire/questionnaire.pdf)
- [Evaluation](evaluation/)
- [Movie Dataset](https://huggingface.co/datasets/wykonos/movies)

---
Made with ❤️
