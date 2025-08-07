import streamlit as st
import pickle
import docx
import PyPDF2
import re
import os
import time
import plotly.graph_objects as go
import numpy as np

# --- Page Configuration ---
st.set_page_config(
    page_title="AI Resume Screener v2",
    page_icon="✨",
    layout="wide"
)

# --- Custom CSS for Advanced Styling ---
st.markdown("""
<style>
    /* Main container styling */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 5rem;
        padding-right: 5rem;
    }
    /* Title styling */
    h1 {
        color: #2E3B4E;
        text-align: center;
        font-weight: bold;
    }
    /* Markdown text styling */
    .stMarkdown p {
        text-align: center;
        color: #4F637B;
    }
    /* File uploader styling */
    .stFileUploader {
        border: 2px dashed #B0C4DE;
        border-radius: 10px;
        padding: 25px;
        background-color: #F8F9FA;
    }
    /* Result card styling */
    .result-card {
        background-color: #ffffff;
        border-radius: 10px;
        padding: 25px;
        box-shadow: 0 4px 8px 0 rgba(0,0,0,0.1);
        text-align: center;
        transition: all 0.3s;
    }
    .result-card:hover {
        box-shadow: 0 8px 16px 0 rgba(0,0,0,0.2);
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
    """Loads all necessary machine learning models, encoders, and PCA."""
    base_path = os.path.dirname(__file__)
    
    # Load ML models
    with open(os.path.join(base_path, 'clf.pkl'), 'rb') as f:
        svc_model = pickle.load(f)
    with open(os.path.join(base_path, 'tfidf.pkl'), 'rb') as f:
        tfidf = pickle.load(f)
    with open(os.path.join(base_path, 'encoder.pkl'), 'rb') as f:
        le = pickle.load(f)
    # Load PCA model for 3D visualization
    with open(os.path.join(base_path, 'pca.pkl'), 'rb') as f:
        pca = pickle.load(f)
        
    return svc_model, tfidf, le, pca

# --- Text Processing and Prediction Functions ---
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
    return None

def predict_category(resume_text, model, vectorizer, label_encoder):
    """Predicts the job category and returns the vectorized text."""
    cleaned_text = clean_resume(resume_text)
    vectorized_text_sparse = vectorizer.transform([cleaned_text])
    
    # Convert sparse matrix to dense array for prediction and PCA
    vectorized_text_dense = vectorized_text_sparse.toarray()
    
    prediction_id = model.predict(vectorized_text_dense)[0]
    category_name = label_encoder.inverse_transform([prediction_id])[0]
    
    return category_name, vectorized_text_dense

# --- Main Application ---
def main():
    st.title("✨ AI Resume Analyzer Pro")
    st.markdown("<p>Harness the power of AI to instantly screen and visualize resume profiles.</p>", unsafe_allow_html=True)
    
    st.sidebar.header("How It Works")
    st.sidebar.info(
        "1. **Upload a resume** (PDF, DOCX, or TXT).\n"
        "2. Our AI processes the text and predicts the job category.\n"
        "3. A **3D visualization** shows where the resume fits in the data landscape.\n"
    )

    try:
        svc_model, tfidf, le, pca = load_resources()
    except FileNotFoundError as e:
        st.error(f"A required model file is missing: {e.filename}. Please ensure `clf.pkl`, `tfidf.pkl`, `encoder.pkl`, and `pca.pkl` are present.")
        return

    uploaded_file = st.file_uploader("Upload your resume to begin analysis", type=["pdf", "docx", "txt"])

    if uploaded_file is not None:
        with st.spinner('AI is analyzing the document... Please wait.'):
            resume_text = extract_text(uploaded_file)
            time.sleep(2) # Simulate processing time
        
        if resume_text:
            st.success("Analysis complete!")
            
            prediction, vectorized_resume = predict_category(resume_text, svc_model, tfidf, le)
            
            st.markdown("---")
            
            col1, col2 = st.columns([1, 1])

            with col1:
                # Animated result display
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.subheader("Predicted Job Category")
                result_placeholder = st.empty()
                result_placeholder.markdown("<h2>...</h2>", unsafe_allow_html=True)
                time.sleep(0.5)
                result_placeholder.markdown(f"<h2>{prediction}</h2>", unsafe_allow_html=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with col2:
                # 3D Visualization
                st.markdown('<div class="result-card">', unsafe_allow_html=True)
                st.subheader("Resume Vector Visualization")
                
                # Reduce dimensionality to 3D using the loaded PCA model
                resume_3d = pca.transform(vectorized_resume)
                
                # Create 3D scatter plot
                fig = go.Figure(data=[go.Scatter3d(
                    x=resume_3d[:, 0], y=resume_3d[:, 1], z=resume_3d[:, 2],
                    mode='markers',
                    marker=dict(
                        size=12,
                        color='royalblue',
                        opacity=0.8,
                        symbol='diamond'
                    )
                )])
                
                fig.update_layout(
                    margin=dict(l=0, r=0, b=0, t=0),
                    scene=dict(
                        xaxis_title='Component 1',
                        yaxis_title='Component 2',
                        zaxis_title='Component 3'
                    )
                )
                st.plotly_chart(fig, use_container_width=True)
                st.markdown('</div>', unsafe_allow_html=True)

            with st.expander("Show Extracted Resume Text"):
                st.text_area("", resume_text, height=250)

if __name__ == "__main__":
    main()
