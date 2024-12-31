import re
import os
import torch
from opensubtitlescom import OpenSubtitles
from transformers import pipeline
from dotenv import load_dotenv
from keybert import KeyBERT

load_dotenv(dotenv_path='../KEYS.env')

API_KEY = os.getenv("API_KEY")
USER_AGENT = os.getenv("USER_AGENT")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

MAX_SUM_LENGTH = 120
MIN_SUM_LENGTH = 30
SAMPLE_SUM = False # decides if summarization is stochastic

def initializeOpensubtitles():
    """Init OpenSubtitles API."""
    ost = OpenSubtitles(api_key=API_KEY, user_agent=USER_AGENT)
    ost.login(USERNAME,PASSWORD)
    return ost


def checkSubtitleFile(movie_name):
    """
    Checks if the cleaned subtitle file exists already
    """
    base_dir = os.path.dirname(os.path.dirname(__file__))
    subtitles_dir = os.path.join(base_dir, "data", "subtitles", "cleaned")

    cleaned_file = os.path.join(subtitles_dir, f"{movie_name}.txt")
    if os.path.exists(cleaned_file):
        print(f"File '{cleaned_file}' exists already. Will use its content.")
        with open(cleaned_file, "r", encoding="utf-8") as file:
            content = file.read()
        return content

    return None


def downloadAndSaveSubtitle(ost, movie_name, language):
    """
    Download and save subtitle files
    """
    response = ost.search(query=movie_name, languages=language)
    if not response.data:
        raise Exception("No subtitles found.") # TODO: Use summary from movie dataset

    base_dir = os.path.dirname(os.path.dirname(__file__))
    raw_dir = os.path.join(base_dir, "data", "subtitles", "raw")
    cleaned_dir = os.path.join(base_dir, "data", "subtitles", "cleaned")
    os.makedirs(raw_dir, exist_ok=True)
    os.makedirs(cleaned_dir, exist_ok=True)

    raw_file = os.path.join(raw_dir, f"{movie_name}.srt")
    cleaned_file = os.path.join(cleaned_dir, f"{movie_name}.txt")

    # currently uses first upload to opensubtitles
    subtitle = response.data[-1] # TODO: verify that subtitle file is correct (Trailer Subtitles? Movie Extras Subtitle?)
    download_data = ost.download(file_id=subtitle.file_id)

    # save raw subtitle file
    with open(raw_file, "wb") as f:
        f.write(download_data)
    print(f"Raw subtitle saved in '{raw_file}'.")

    # clean subtitle
    cleaned_text = preprocessSubtitles(raw_file)
    with open(cleaned_file, "w", encoding="utf-8") as f:
        f.write(cleaned_text)
    print(f"Cleaned subtitle saved in '{cleaned_file}'.")

    return cleaned_text


def preprocessSubtitles(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        srt_content = f.read()

    cleaned_text = re.sub(r"\d{2}:\d{2}:\d{2},\d{3} --> \d{2}:\d{2}:\d{2},\d{3}", "", srt_content)  # remove time
    cleaned_text = re.sub(r"^\d+\s*$", "", cleaned_text, flags=re.MULTILINE)                        # remove IDs
    cleaned_text = re.sub(r"<[^>]+>", "", cleaned_text)                                             # remove html tags
    cleaned_text = re.sub(r"&lt;[^&]+&gt;", "", cleaned_text)                                       # remove html entities
    cleaned_text = re.sub(r"\([^)]*\)", "", cleaned_text)                                           # remove ()
    cleaned_text = re.sub(r"\[[^]]*\]", "", cleaned_text)                                           # remove []
    cleaned_text = re.sub(r"\{[^}]*\}", "", cleaned_text)                                           # remove {}
    cleaned_text = re.sub(r"♪.*", "", cleaned_text)                                                 # remove musical notes
    cleaned_text = re.sub(r"-", "", cleaned_text)                                                   # remove '-'
    cleaned_text = re.sub(r"^\s+", "", cleaned_text, flags=re.MULTILINE)                            # remove leading spaces
    cleaned_text = re.sub(r"_", "", cleaned_text)                                                   # remove '_'
    cleaned_text = re.sub(r"^Sync, corrected by.*", "", cleaned_text, flags=re.MULTILINE)           # remove lines starting with 'Sync, corrected by'
    cleaned_text = re.sub(r"^www\..*", "", cleaned_text, flags=re.MULTILINE)                        # remove lines starting with 'www.'
    cleaned_text = re.sub(r"^Subtitles by.*", "", cleaned_text, flags=re.MULTILINE)                 # remove lines starting with 'Subtitles by'
    cleaned_text = re.sub(r"^[A-Z][A-Z\s]*: ", "", cleaned_text, flags=re.MULTILINE)                # remove names followed by a colon
    cleaned_text = re.sub(r"^[A-Za-z\s]*:$", "", cleaned_text, flags=re.MULTILINE)                  # remove lines that are only names followed by a colon
    cleaned_text = re.sub(r"^\s*$", "", cleaned_text, flags=re.MULTILINE)                           # remove empty lines
    cleaned_text = re.sub(r"\n{2,}", "\n", cleaned_text)                                            # remove spaces
    cleaned_text = cleaned_text.strip()

    return cleaned_text

def summarizeSubtitles(text):
    """
    Currently only summarizes first chunk of subtitle text (got best results with only first chunk)
    """
    if torch.cuda.is_available():
        print("CUDA available")
        device = torch.device("cuda")
    elif torch.backends.mps.is_available():
        print("MPS available")
        device = torch.device("mps")
    else:
        print("Fallback to CPU")
        device = torch.device("cpu")

    summarizer = pipeline("summarization", model="facebook/bart-large-cnn", device=device)

    chunk_size = 1024
    first_chunk = text[:chunk_size] 

    result = summarizer(first_chunk, max_length=MAX_SUM_LENGTH, min_length=MIN_SUM_LENGTH, do_sample=SAMPLE_SUM)

    return result[0]['summary_text']

def extractKeyThemes(cleaned_text, num_topics=3):
    """
    Extract key themes from cleaned text using KeyBERT.
    """
    kw_model = KeyBERT()
    keywords = kw_model.extract_keywords(cleaned_text, stop_words='english')
    themes = [kw for kw, _ in keywords][:num_topics]
    return themes