import streamlit as st
import pickle
import docx
import PyPDF2
import re
import os

# Configure the page for a clean and professional look
st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="🤖",
    layout="centered"
)

# Use caching to load models only once, which significantly improves performance.
@st.cache_resource
def load_resources():
    """Loads all necessary machine learning models and encoders."""
    # IMPORTANT: Ensure 'clf.pkl', 'tfidf.pkl', and 'encoder.pkl' are in the same directory.
    base_path = os.path.dirname(__file__)
    
    with open(os.path.join(base_path, 'clf.pkl'), 'rb') as f:
        svc_model = pickle.load(f)
    with open(os.path.join(base_path, 'tfidf.pkl'), 'rb') as f:
        tfidf = pickle.load(f)
    with open(os.path.join(base_path, 'encoder.pkl'), 'rb') as f:
        le = pickle.load(f)
    return svc_model, tfidf, le

def clean_resume(txt):
    """Cleans the raw resume text using regular expressions."""
    clean_text = re.sub(r'http\S+\s', ' ', txt)
    clean_text = re.sub(r'RT|cc', ' ', clean_text)
    clean_text = re.sub(r'#\S+\s', ' ', clean_text)
    clean_text = re.sub(r'@\S+', '  ', clean_text)
    clean_text = re.sub(r'[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', clean_text)
    clean_text = re.sub(r'[^\x00-\x7f]', ' ', clean_text)
    clean_text = re.sub(r'\s+', ' ', clean_text)
    return clean_text.strip()

def extract_text(uploaded_file):
    """Extracts text from uploaded file based on its extension."""
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()
    
    if file_extension == '.pdf':
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        return "".join(page.extract_text() for page in pdf_reader.pages)
    elif file_extension == '.docx':
        doc = docx.Document(uploaded_file)
        return "\n".join(para.text for para in doc.paragraphs)
    elif file_extension == '.txt':
        return uploaded_file.read().decode('utf-8', errors='ignore')
    else:
        st.error("Unsupported file type. Please upload a PDF, DOCX, or TXT file.")
        return None

def predict_category(resume_text, model, vectorizer, label_encoder):
    """Predicts the job category of a resume using the loaded models."""
    cleaned_text = clean_resume(resume_text)
    vectorized_text = vectorizer.transform([cleaned_text])
    prediction_id = model.predict(vectorized_text)[0]
    category_name = label_encoder.inverse_transform([prediction_id])[0]
    return category_name

def main():
    st.title("🤖 AI-Powered Resume Screener")
    st.markdown("""
    Upload a resume, and our AI will instantly categorize it into the correct job profile.
    This helps recruiters quickly sort through applications and find the right candidates faster.
    """)
    
    st.sidebar.header("How to Use")
    st.sidebar.info(
        "1. **Upload a resume** (PDF, DOCX, or TXT).\n"
        "2. The AI will analyze the text.\n"
        "3. The **predicted job category** will be displayed."
    )

    try:
        svc_model, tfidf, le = load_resources()
    except FileNotFoundError:
        st.error("Model files not found! Please ensure `clf.pkl`, `tfidf.pkl`, and `encoder.pkl` are present.")
        return

    uploaded_file = st.file_uploader("Choose a resume file", type=["pdf", "docx", "txt"])

    if uploaded_file is not None:
        with st.spinner('Analyzing resume...'):
            resume_text = extract_text(uploaded_file)
        
        if resume_text:
            st.success("Resume processed successfully!")
            
            prediction = predict_category(resume_text, svc_model, tfidf, le)
            
            st.markdown("---")
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.image("https://cdn-icons-png.flaticon.com/512/3242/3242257.png", width=120)

            with col2:
                st.subheader("Predicted Job Category:")
                st.markdown(f"## **{prediction}**")
            
            with st.expander("Show Extracted Resume Text"):
                st.text_area("", resume_text, height=300)

if __name__ == "__main__":
    main()
