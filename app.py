import streamlit as st
import pickle
import docx
import PyPDF2
import re
import os
import time

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Resume Screener",
    page_icon="🤖",
    layout="centered"
)

# --- Custom CSS for Styling ---
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }
    h1 {
        color: #2E3B4E;
        text-align: center;
        font-weight: bold;
    }
    .stFileUploader {
        border: 2px dashed #B0C4DE;
        border-radius: 10px;
        padding: 25px;
        background-color: #F8F9FA;
    }
    .result-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 35px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.1);
        text-align: center;
        margin-top: 20px;
    }
    .result-card h2 {
        color: #1E90FF;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# --- Model and Resource Loading ---
@st.cache_resource
def load_resources():
    """Loads all necessary machine learning models and encoders."""
    base_path = os.path.dirname(__file__)
    with open(os.path.join(base_path, 'clf.pkl'), 'rb') as f:
        svc_model = pickle.load(f)
    with open(os.path.join(base_path, 'tfidf.pkl'), 'rb') as f:
        tfidf = pickle.load(f)
    with open(os.path.join(base_path, 'encoder.pkl'), 'rb') as f:
        le = pickle.load(f)
    return svc_model, tfidf, le

# --- Text Processing and Prediction Functions ---
def clean_resume(txt):
    """Cleans the raw resume text."""
    clean_text = re.sub(r'http\S+\s', ' ', txt)
    clean_text = re.sub(r'RT|cc', ' ', clean_text)
    clean_text = re.sub(r'#\S+\s', ' ', clean_text)
    clean_text = re.sub(r'@\S+', '  ', clean_text)
    clean_text = re.sub(r'[%s]' % re.escape("""!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~"""), ' ', clean_text)
    clean_text = re.sub(r'[^\x00-\x7f]', ' ', clean_text)
    clean_text = re.sub(r'\s+', ' ', clean_text)
    return clean_text.strip()

def extract_text(uploaded_file):
    """Extracts text from the uploaded file."""
    file_extension = os.path.splitext(uploaded_file.name)[1].lower()
    if file_extension == '.pdf':
        pdf_reader = PyPDF2.PdfReader(uploaded_file)
        return "".join(page.extract_text() for page in pdf_reader.pages)
    elif file_extension == '.docx':
        doc = docx.Document(uploaded_file)
        return "\n".join(para.text for para in doc.paragraphs)
    elif file_extension == '.txt':
        return uploaded_file.read().decode('utf-8', errors='ignore')
    return None

def predict_category(resume_text, model, vectorizer, label_encoder):
    """Predicts the job category of a resume."""
    cleaned_text = clean_resume(resume_text)
    vectorized_text_sparse = vectorizer.transform([cleaned_text])
    
    # FIX: Convert sparse matrix to a dense array for the model
    vectorized_text_dense = vectorized_text_sparse.toarray()
    
    prediction_id = model.predict(vectorized_text_dense)[0]
    category_name = label_encoder.inverse_transform([prediction_id])[0]
    return category_name

# --- Main Application ---
def main():
    st.title("🤖 AI-Powered Resume Screener")
    st.markdown("Upload a resume, and our AI will instantly categorize it into the correct job profile.")
    
    st.sidebar.header("How to Use")
    st.sidebar.info(
        "1. **Upload a resume** (PDF, DOCX, or TXT).\n"
        "2. The AI will analyze the text.\n"
        "3. The **predicted job category** will be displayed."
    )

    try:
        svc_model, tfidf, le = load_resources()
    except FileNotFoundError as e:
        st.error(f"A model file is missing: {e.filename}. Please ensure `clf.pkl`, `tfidf.pkl`, and `encoder.pkl` are present.")
        return

    uploaded_file = st.file_uploader("Choose a resume file", type=["pdf", "docx", "txt"])

    if uploaded_file is not None:
        with st.spinner('Analyzing resume...'):
            resume_text = extract_text(uploaded_file)
            time.sleep(1) # Simulate processing
        
        if resume_text:
            st.success("Resume processed successfully!")
            
            prediction = predict_category(resume_text, svc_model, tfidf, le)
            
            # Display result in a styled card
            st.markdown('<div class="result-card">', unsafe_allow_html=True)
            st.subheader("Predicted Job Category:")
            result_placeholder = st.empty()
            result_placeholder.markdown("<h2>...</h2>", unsafe_allow_html=True)
            time.sleep(0.5) # Animate the result
            result_placeholder.markdown(f"<h2>{prediction}</h2>", unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            with st.expander("Show Extracted Resume Text"):
                st.text_area("", resume_text, height=250)

if __name__ == "__main__":
    main()
