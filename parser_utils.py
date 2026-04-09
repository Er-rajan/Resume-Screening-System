


def load_spacy_model():
    """Automatically downloads the English model if missing."""
    model_name = "en_core_web_sm"
    try:
        
        return spacy.load(model_name)
    except OSError:
        print(f"[{model_name}] not found in venv. Downloading now...")
        
        subprocess.run([sys.executable, "-m", "spacy", "download", model_name])
        return spacy.load(model_name)


nlp = load_spacy_model()


def extract_text_from_pdf(pdf_path):
    """Extracts text from PDF files."""
    text = ""
    try:
        with open(pdf_path, 'rb') as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                extracted = page.extract_text()
                if extracted:
                    text += extracted
    except Exception as e:
        print(f"Error reading PDF {pdf_path}: {e}")
    return text

def extract_text_from_docx(docx_path):
    """Extracts text from Word (.docx) files."""
    try:
        doc = docx.Document(docx_path)
        return " ".join([para.text for para in doc.paragraphs])
    except Exception as e:
        print(f"Error reading Docx {docx_path}: {e}")
        return ""


def clean_resume(text):
    """
    Cleans the raw text:
    1. Removes URLs, emails, and special characters.
    2. Tokenizes and Lemmatizes (running -> run).
    3. Removes Stopwords (the, is, at).
    """
    
    text = re.sub(r'\S+@\S+', '', text)  # Emails
    text = re.sub(r'http\S+', '', text)   # URLs
    text = re.sub(r'[^a-zA-Z\s]', ' ', text) # Special chars & Numbers
    text = re.sub(r'\s+', ' ', text)     # Extra whitespace
    
    
    doc = nlp(text.lower())
    
    tokens = [token.lemma_ for token in doc if not token.is_stop and not token.is_punct]
    
    return " ".join(tokens)