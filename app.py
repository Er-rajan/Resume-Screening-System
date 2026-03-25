import streamlit as st
import pandas as pd
import os
from parser_utils import extract_text_from_pdf, clean_resume
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


SKILL_DB = {
    "MERN_Stack": ["MongoDB", "Express", "React", "Node", "JavaScript", "Redux", "Next.js"],
    "AI_ML": ["Python", "PyTorch", "TensorFlow", "Scikit-learn", "NLP", "Computer Vision", "Keras"],
    "Databases": ["MySQL", "PostgreSQL", "Redis", "Firebase", "Oracle", "MongoDB"],
    "OS": ["Linux", "Ubuntu", "Fedora", "Windows Server", "Unix", "WSL"]
}
ALL_SKILLS_STRING = " ".join([s for sub in SKILL_DB.values() for s in sub])


st.set_page_config(page_title="AI Resume Screener", layout="wide")
st.title("Resume Screening & Ranking System")
st.markdown("Upload candidate resumes to rank them against the **Full Stack & AI/ML** skill set.")


st.sidebar.header("Upload Section")
uploaded_files = st.sidebar.file_uploader(
    "Upload Resumes (PDF or TXT)", 
    type=["pdf", "txt"], 
    accept_multiple_files=True
)

if uploaded_files:
    results = []
    
    for uploaded_file in uploaded_files:
        
        if uploaded_file.name.endswith(".pdf"):
            
            with open("temp.pdf", "wb") as f:
                f.write(uploaded_file.getbuffer())
            raw_text = extract_text_from_pdf("temp.pdf")
            os.remove("temp.pdf")
        else:
            raw_text = str(uploaded_file.read(), "utf-8")

        if not raw_text.strip():
            st.warning(f"Skipping {uploaded_file.name}: Could not extract text.")
            continue

        
        cleaned_resume = clean_resume(raw_text)
        
        
        category_scores = {cat: len([s for s in skills if s.lower() in raw_text.lower()]) 
                           for cat, skills in SKILL_DB.items()}
        
        
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform([cleaned_resume, clean_resume(ALL_SKILLS_STRING)])
        match_score = round(cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:2])[0][0] * 100, 2)

        results.append({
            "Candidate": uploaded_file.name,
            "Match %": match_score,
            "AI/ML": category_scores["AI_ML"],
            "MERN": category_scores["MERN_Stack"],
            "DB/OS": category_scores["Databases"] + category_scores["OS"]
        })

    
    if results:
        df = pd.DataFrame(results).sort_values(by="Match %", ascending=False)
        
        st.subheader(" Ranking Results")
        st.dataframe(df, use_container_width=True)
        
        
        top_name = df.iloc[0]['Candidate']
        st.success(f"**Top Recommendation:** {top_name} with a {df.iloc[0]['Match %']}% match!")
else:
    st.info("Please upload PDF or TXT resumes in the sidebar to begin.")