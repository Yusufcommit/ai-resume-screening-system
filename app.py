import os
import tempfile
import pandas as pd
import streamlit as st

from parser import extract_text, extract_candidate_name, extract_email
from ranking import calculate_final_score
from explainer import generate_explanation


st.set_page_config(page_title="AI Resume Screening System", layout="wide")

st.title("AI-Powered Resume Screening and Ranking System")
st.markdown("Upload resumes and compare them against a job description.")

job_description = st.text_area("Paste Job Description", height=220)

uploaded_files = st.file_uploader(
    "Upload Resume Files (PDF or DOCX)",
    type=["pdf", "docx"],
    accept_multiple_files=True
)

if st.button("Analyze Candidates"):
    if not job_description.strip():
        st.warning("Please paste a job description first.")
    elif not uploaded_files:
        st.warning("Please upload at least one resume.")
    else:
        results = []

        with st.spinner("Analyzing resumes..."):
            for uploaded_file in uploaded_files:
                suffix = os.path.splitext(uploaded_file.name)[1]
                with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                    tmp.write(uploaded_file.read())
                    tmp_path = tmp.name

                try:
                    resume_text = extract_text(tmp_path)
                    candidate_name = extract_candidate_name(resume_text)
                    email = extract_email(resume_text)

                    score_data = calculate_final_score(resume_text, job_description)
                    explanation = generate_explanation(score_data, candidate_name)

                    results.append({
                        "Candidate Name": candidate_name,
                        "Email": email,
                        "Final Score": score_data["final_score"],
                        "Skill Score": score_data["skill_score"],
                        "Experience Score": score_data["experience_score"],
                        "Education Score": score_data["education_score"],
                        "Semantic Score": score_data["semantic_score"],
                        "Matched Skills": ", ".join(score_data["matched_skills"]),
                        "Missing Skills": ", ".join(score_data["missing_skills"]),
                        "Explanation": explanation
                    })
                except Exception as e:
                    st.error(f"Error processing {uploaded_file.name}: {e}")
                finally:
                    os.remove(tmp_path)

        if results:
            df = pd.DataFrame(results).sort_values(by="Final Score", ascending=False).reset_index(drop=True)
            st.subheader("Candidate Rankings")
            st.dataframe(df, use_container_width=True)

            st.subheader("Top Candidate")
            top = df.iloc[0]
            st.success(f"Best Match: {top['Candidate Name']} ({top['Final Score']}%)")
            st.write(top["Explanation"])

            st.subheader("Score Overview")
            chart_df = df[["Candidate Name", "Final Score"]].set_index("Candidate Name")
            st.bar_chart(chart_df)

            csv = df.to_csv(index=False).encode("utf-8")
            st.download_button(
                label="Download Results as CSV",
                data=csv,
                file_name="resume_ranking_results.csv",
                mime="text/csv"
            )