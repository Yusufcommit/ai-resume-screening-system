# AI-Powered Resume Screening and Ranking System

## Overview
This project is an AI-based system that analyzes and ranks resumes according to a given job description using Natural Language Processing (NLP) techniques.

## Problem Statement
Recruiters often spend a significant amount of time manually reviewing resumes. This process is inefficient and prone to bias. This system automates resume screening by evaluating candidates objectively based on job requirements.

## Features
- Upload multiple resumes (PDF/DOCX)
- Extract candidate information automatically
- Rank candidates based on:
  - Skill matching
  - Experience relevance
  - Education level
  - Semantic similarity using NLP
- Identify missing skills
- Provide explanation for each candidate score
- Visualize results using charts

## Technologies Used
- Python
- Streamlit
- Sentence Transformers (NLP)
- pandas
- scikit-learn
- pdfplumber
- python-docx

## How to Run

```bash
pip install -r requirements.txt
streamlit run app.py
Demo Screenshots
Main Interface

Candidate Ranking

Score Visualization

Project Structure

ai-resume-screening-system/
│
├── app.py
├── parser.py
├── ranking.py
├── explainer.py
├── utils.py
│
├── requirements.txt
├── README.md
│
├── screenshots/
│ ├── ui.png
│ ├── results.png
│ ├── chart.png

Future Improvements
Improve NLP model accuracy
Add database integration
Deploy as a web application
Enhance user interface and experience
Implement bias detection in candidate evaluation