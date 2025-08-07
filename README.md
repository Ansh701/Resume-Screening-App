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
      <td align="center">
        <a href="https://www.python.org/" target="_blank">
          <img src="https://www.vectorlogo.zone/logos/python/python-icon.svg" alt="Python" width="50px">
        </a>
        <br><strong>Python</strong>
      </td>
      <td align="center">
        <a href="https://streamlit.io/" target="_blank">
          <img src="https://www.vectorlogo.zone/logos/streamlit/streamlit-icon.svg" alt="Streamlit" width="50px">
        </a>
        <br><strong>Streamlit</strong>
      </td>
      <td align="center">
        <a href="https://scikit-learn.org/" target="_blank">
          <img src="https://www.vectorlogo.zone/logos/scikit-learn/scikit-learn-icon.svg" alt="Scikit-learn" width="50px">
        </a>
        <br><strong>Scikit-learn</strong>
      </td>
      <td align="center">
        <a href="https://pandas.pydata.org/" target="_blank">
          <img src="https://www.vectorlogo.zone/logos/pandas-dev/pandas-dev-icon.svg" alt="Pandas" width="50px">
        </a>
        <br><strong>Pandas</strong>
      </td>
      <td align="center">
        <a href="https://render.com/" target="_blank">
          <img src="https://www.vectorlogo.zone/logos/render/render-icon.svg" alt="Render" width="50px">
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
├── app.py                  # The main Streamlit application script
├── requirements.txt        # Python dependencies for deployment
├── clf.pkl                 # Trained classifier model
├── tfidf.pkl               # Trained TF-IDF vectorizer
├── encoder.pkl             # Trained LabelEncoder
└── README.md               # Project documentation
