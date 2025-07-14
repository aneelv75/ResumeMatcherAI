
import streamlit as st
import os
import tempfile
import pandas as pd
import requests

# Set your Together.ai API key
TOGETHER_API_KEY = "9bd11a3547ac3106bfedc8f4dd60c96bf1c21355ab39ac50e753b1169de9a12c"
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
MODEL = "meta-llama/Llama-3-8b-chat-hf"

# Streamlit App
st.set_page_config(page_title="Resume Matcher AI (Cloud)", layout="centered")
st.title("📄 Resume Matcher AI")

# JD Upload
jd_file = st.file_uploader("Upload Job Description (.txt or .docx)", type=["txt", "docx"])

# Resume Upload
resumes = st.file_uploader("Upload Resumes (.pdf, .docx, .txt)", type=["pdf", "docx", "txt"], accept_multiple_files=True)

# API call to Together.ai
def get_score_and_reason(prompt):
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are an AI resume evaluator."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.5
    }
    response = requests.post(TOGETHER_API_URL, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        return "Score: 0\nReason: Could not evaluate due to API error."

# Match button
if st.button("Match Resumes with JD") and jd_file and resumes:
    with tempfile.TemporaryDirectory() as tmpdir:
        jd_path = os.path.join(tmpdir, "jd.txt")
        with open(jd_path, "wb") as f:
            f.write(jd_file.read())

        jd_text = open(jd_path, "r", encoding="utf-8", errors="ignore").read()

        output_data = []

        for resume_file in resumes:
            resume_path = os.path.join(tmpdir, resume_file.name)
            with open(resume_path, "wb") as f:
                f.write(resume_file.read())

            resume_text = open(resume_path, "r", encoding="utf-8", errors="ignore").read()

            prompt = f"""Evaluate this resume based on the job description below:
JOB DESCRIPTION:
{jd_text}

RESUME:
{resume_text}

Return a score out of 100 and a reason.
Format:
Score: <number>
Reason: <reason>
"""

            response_text = get_score_and_reason(prompt)

            score = 0
            reason = "N/A"
            for line in response_text.splitlines():
                if line.lower().startswith("score:"):
                    try:
                        score = int(line.split(":")[1].strip())
                    except:
                        score = 0
                elif line.lower().startswith("reason:"):
                    reason = line.split(":", 1)[1].strip()

            output_data.append({
                "Resume": resume_file.name,
                "Score": score,
                "Reason": reason
            })

        df = pd.DataFrame(output_data)
        st.success("✅ Matching Complete")
        st.dataframe(df)

        # Download
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇ Download CSV", data=csv, file_name="resume_scores.csv", mime='text/csv')
