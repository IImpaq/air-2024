<h1 align="center">:film_strip: Movie Finder :film_strip:</h1>

A intelligent movie recommendation system that uses advanced techniques to recommend movies based on your preferences.

<p align="center">
  <img src="assets/hero.gif" alt="Hero Trailer Video" width="100%">
</p>

## :sparkles: Key Features

- Platform-independent movie recommendations
- Genre Selection
- Mood Choice
- Era Timeframe Options
- Language Decision
- Notes for in-depth personalization

## :rocket: Getting Started

### :computer: Prerequisites

- Git
- Bun.js (OR: npm & node)
- Python 3.11+

### :package: Installation

```bash
# Clone the repository
git clone git@github.com:IImpaq/movie-finder.git
cd movie-finder

# Prepare the backend
cd backend
pip install -r requirements.txt
python fetch.py      # Fetch dataset from huggingface
python preprocess.py # Prepare and preprocess the data
cd ..

# Prepare the frontend
cd frontend
bun install # OR: npm install
cd ..
```

### :gear: Running

**Full-Stack Application**

```bash
# Terminal 1: Start Frontend
cd frontend
bun run dev # Website Available at http://localhost:3000

# Terminal 2: Start Backend
cd backend
uvicorn app:app --reload  # API available at http://localhost:8000
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

## :books: Dataset

Already included is the preprocessed dataset. It includes around 180.000 rows and the following columns:
```js
["id", "title", "genres", "original_language", "overview", "popularity", "vote_average", "release_date", "status", "keywords", "credits", "poster_path"]
```
The preprocessed dataset is generated from the raw data of the [wykonos/movies](https://huggingface.co/datasets/wykonos/movies) collection that is published on [Hugging Face](https://huggingface.co/).

## :wrench: Tech Stack

- Frontend: NextJS & TypeScript
- Backend: Python, FastAPI & PyTorch

## :link: Links

- [Design Document](design-document/design-document.pdf)
- [Report](report/report.pdf)
- [Presentation](presentation/presentation.pdf)
- [Questionnaire](questionnaire/questionnaire.pdf)
- [Evaluation](evaluation/)
- [Movie Dataset](https://huggingface.co/datasets/wykonos/movies)

## :brain: Team & Roles
- **Patrick Eckel:** Design Document, Frontend, Data Transfer
- **Marcus Gugacs:** Design Document, Frontend, Recommender, CLI, Evaluation, Questionnaire, Report, Presentation
- **Martin Tobias Klug:** Design Document, Subtitle Fetching, Summarization Pipeline, Report
- **Lukas Leitner:** Design Document, Data Preprocessing, Report, Presentation

## :memo: License

MIT License (see [LICENSE](LICENSE.md)).

## :telephone: Contact
If you have any questions or want to get in touch, just [send an email](mailto:iimpaq@proton.me)

---
Made with :heart:
