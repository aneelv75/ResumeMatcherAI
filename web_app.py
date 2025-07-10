
import streamlit as st
import os
import tempfile
import subprocess
import pandas as pd
from docx import Document
import PyPDF2

# Streamlit page config
st.set_page_config(page_title="Resume Matcher AI", layout="centered")
st.title("📄 Resume Matcher AI")

# Function to extract text from different resume file types
def extract_text(file_path):
    if file_path.endswith(".txt"):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()

    elif file_path.endswith(".docx"):
        doc = Document(file_path)
        return "\n".join([para.text for para in doc.paragraphs])

    elif file_path.endswith(".pdf"):
        text = ""
        with open(file_path, "rb") as f:
            reader = PyPDF2.PdfReader(f)
            for page in reader.pages:
                text += page.extract_text() or ""
        return text

    else:
        return "Unsupported file type"

# Upload JD
jd_file = st.file_uploader("Upload Job Description (.txt)", type=["txt"])

# Upload Resumes
resumes = st.file_uploader("Upload Resumes (.pdf, .docx, .txt)", type=["pdf", "docx", "txt"], accept_multiple_files=True)

# Match button
if st.button("Match Resumes with JD") and jd_file and resumes:
    with tempfile.TemporaryDirectory() as tmpdir:
        jd_path = os.path.join(tmpdir, "jd.txt")
        with open(jd_path, "wb") as f:
            f.write(jd_file.read())

        jd_text = extract_text(jd_path)
        output_data = []

        for resume_file in resumes:
            resume_path = os.path.join(tmpdir, resume_file.name)
            with open(resume_path, "wb") as f:
                f.write(resume_file.read())

            resume_text = extract_text(resume_path)

            prompt = f"""Evaluate this resume based on the job description below:
JOB DESCRIPTION:
{jd_text}

RESUME:
{resume_text}

Return a score out of 100 and a reason.
Format:
Score: <number>
Reason: <reason>"""

            command = ["ollama", "run", "llama3", prompt]
            result = subprocess.run(command, capture_output=True)

            output_text = result.stdout.decode("utf-8", errors="ignore")
            error_text = result.stderr.decode("utf-8", errors="ignore")

            print("========== LLM RAW OUTPUT ==========")
            print(output_text)
            print("========== LLM ERRORS (if any) ==========")
            print(error_text)

            # Parse Score and Reason
            score = 0
            reason = "Could not parse."
            for line in output_text.splitlines():
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

        # Download as CSV
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇ Download CSV", data=csv, file_name="resume_scores.csv", mime='text/csv')
