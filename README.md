# Phishing URL Detection System

A machine learning–based web application that detects whether a given website URL is **legitimate or phishing** using structural URL features and multiple classification models. The system analyzes lexical characteristics of URLs and predicts potential phishing threats through a trained machine learning model.

The project includes an interactive **Streamlit web interface** where users can enter a URL and receive an instant prediction.

---

## Project Overview

Phishing attacks are a major cybersecurity threat used to steal credentials, financial data, and personal information. This project aims to identify phishing websites by analyzing the structural properties of URLs instead of relying on blacklists.

The system extracts multiple URL-based features such as:

* URL length
* Hostname length
* Number of dots and special characters
* Digit ratio in URL
* Subdomain count
* Presence of HTTP/HTTPS tokens
* Prefix–suffix patterns
* URL shortening services

These features are used to train machine learning models capable of distinguishing between legitimate and phishing websites.

---

## Features

* Machine learning–based phishing URL classification
* Feature engineering using lexical URL characteristics
* Multiple ML models evaluated and compared
* Interactive Streamlit web interface for real-time prediction
* Model evaluation using accuracy, precision, recall, and F1-score
* Confusion matrix and feature importance analysis

---

## Machine Learning Models Used

The following models were implemented and evaluated:

* Logistic Regression
* Decision Tree Classifier
* Random Forest Classifier
* Multi-Layer Perceptron (MLP)
* XGBoost Classifier

The final trained model is saved and integrated with the web application for predictions.

---

## Technologies Used

Programming Language

* Python

Libraries

* Pandas
* NumPy
* Scikit-learn
* XGBoost
* Matplotlib
* Seaborn
* Streamlit
* Pickle

---

## Project Structure

phishing-url-detection/

app.py                → Streamlit web application
phishing_model.pkl    → Trained machine learning model
Notebook/
    model_training.ipynb  → Model training and evaluation notebook
Dataset/
    dataset.csv           → Dataset used for training
README.md             → Project documentation

---

## How the System Works

1. User enters a website URL in the web interface.
2. The system extracts structural features from the URL.
3. The extracted features are passed to the trained machine learning model.
4. The model predicts whether the URL is **Phishing** or **Legitimate**.
5. The result is displayed instantly in the interface.

---

## Running the Project Locally

### 1. Clone the repository

git clone https://github.com/vishalkumar-2006/-Phishing-URL-Detection-Web-Application-Using-Machine-Learning.git

### 2. Install required libraries

pip install -r requirements.txt

### 3. Run the Streamlit application

streamlit run app.py

### 4. Open the application in your browser

http://localhost:8501

---

## Current Status

The project currently includes a **functional local web application built using Streamlit**.
The system can analyze URLs and predict whether they are phishing or legitimate.

The application can be deployed to cloud platforms in the future for public access.

---

## Future Improvements

* Deploy the application for public use
* Improve detection of domain impersonation attacks (e.g., g00gle.com)
* Integrate domain reputation APIs
* Add additional phishing detection features
* Improve model performance using larger datasets

---

## Educational Purpose

This project was developed to explore **machine learning applications in cybersecurity**, specifically focusing on phishing website detection using URL-based analysis.
