# Resume Screening System 

An automated HR-tech solution built with **Python**, **NLP (spaCy)**, and **Machine Learning (Scikit-learn)** to parse, analyze, and rank candidate resumes against specific job roles.

## Project Overview
Manual resume screening is time-consuming and prone to bias. This system automates the process by:
1. **Parsing** unstructured data from PDF resumes.
2. **Cleaning** text using Natural Language Processing (Lemmatization & Stop-word removal).
3. **Categorizing** skills into domains (AI/ML, MERN, DevOps, etc.).
4. **Ranking** candidates using **TF-IDF Vectorization** and **Cosine Similarity**.
5. **Identifying Skill Gaps** to help recruiters understand what a candidate is missing.

## Tech Stack
- **Language:** Python 3.10+
- **NLP Library:** `spaCy` (en_core_web_sm)
- **Machine Learning:** `Scikit-learn` (TF-IDF, Cosine Similarity)
- **Data Handling:** `Pandas`, `NumPy`
- **File Parsing:** `PyPDF2`

## Project Structure
```text
Resume_Project/
├── data/               # Drop PDF resumes here
├── app.py              # Main execution logic & ranking
├── parser_utils.py     # PDF extraction & NLP cleaning
├── requirements.txt    # Project dependencies
└── README.md           # Documentation


## How To Run

Setup Virtual Environment

-->
python3 -m venv venv
source venv/bin/activate


Install Dependencies

-->
python3 -m pip install -r requirements.txt
python3 -m spacy download en_core_web_sm

Launch the Application
Start the Streamlit local server:

-->
python3 -m streamlit run app.py