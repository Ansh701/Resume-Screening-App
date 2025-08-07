<div align="center">

# ✨ AI-Powered Resume Screening App ✨

<p>
  <img alt="Python" src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white">
  <img alt="Streamlit" src="https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white">
  <img alt="Scikit-learn" src="https://img.shields.io/badge/Scikit--learn-F7931E?style=for-the-badge&logo=scikit-learn&logoColor=white">
  <img alt="Render" src="https://img.shields.io/badge/Render-46E3B7?style=for-the-badge&logo=render&logoColor=white">
</p>

An intelligent web application that harnesses the power of Machine Learning to automatically screen, categorize, and visualize resumes. This tool helps recruiters efficiently sort through applications and identify the best candidates in seconds.

---

<a href="https://resume-screening-app-xuw7.onrender.com" target="_blank">
  <img src="https://img.shields.io/badge/Live%20Demo-🚀-blue?style=for-the-badge" alt="Live Demo">
</a>

</div>

## 🌟 Key Features

* **🤖 AI-Powered Categorization**: Automatically predicts the job profile (e.g., "Python Developer," "Data Scientist," "Network Security Engineer") from the resume content.
* **📄 Multi-Format Support**: Accepts resumes in **PDF**, **DOCX**, and **TXT** formats for maximum flexibility.
* **🎨 Interactive UI**: A clean, modern, and user-friendly interface built with Streamlit for a seamless experience.
* **⚙️ Efficient Backend**: Caches machine learning models on startup for fast and responsive predictions.

## 🛠️ Tech Stack & Libraries

<div align="center">
  <table>
    <tr>
      <td align="center" width="150">
        <a href="https://www.python.org/" target="_blank">
          <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Python-logo-notext.svg/1200px-Python-logo-notext.svg.png" alt="Python" width="50px">
        </a>
        <br><strong>Python</strong>
      </td>
      <td align="center" width="150">
        <a href="https://streamlit.io/" target="_blank">
          <img src="https://streamlit.io/images/brand/streamlit-logo-primary-colormark-darktext.svg" alt="Streamlit" width="50px">
        </a>
        <br><strong>Streamlit</strong>
      </td>
      <td align="center" width="150">
        <a href="https://scikit-learn.org/" target="_blank">
          <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/05/Scikit_learn_logo_small.svg/1200px-Scikit_learn_logo_small.svg.png" alt="Scikit-learn" width="50px">
        </a>
        <br><strong>Scikit-learn</strong>
      </td>
      <td align="center" width="150">
        <a href="https://pandas.pydata.org/" target="_blank">
          <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/e/ed/Pandas_logo.svg/1200px-Pandas_logo.svg.png" alt="Pandas" width="50px">
        </a>
        <br><strong>Pandas</strong>
      </td>
      <td align="center" width="150">
        <a href="https://render.com/" target="_blank">
          <img src="https://avatars.githubusercontent.com/u/44933556?s=200&v=4" alt="Render" width="50px">
        </a>
        <br><strong>Render</strong>
      </td>
    </tr>
  </table>
</div>

## 🚀 How to Run Locally

To get this application running on your local machine, follow these steps:

1.  **Clone the Repository**
    ```bash
    git clone <your-github-repository-url>
    cd resume-screening-app
    ```

2.  **Create a Virtual Environment (Recommended)**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

3.  **Install Dependencies**
    Ensure you have all the model files (`clf.pkl`, `tfidf.pkl`, `encoder.pkl`) in the project directory. Then, install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the Streamlit App**
    ```bash
    streamlit run app.py
    ```
    Your web browser will automatically open to the application's local URL.

## 📂 Project Structure
├── app.py                 
├── requirements.txt       
├── clf.pkl                
├── tfidf.pkl              
├── encoder.pkl            
└── README.md             
