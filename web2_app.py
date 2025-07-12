
import streamlit as st
import os
import tempfile
import subprocess
import pandas as pd
from docx import Document
import PyPDF2
import smtplib
from email.mime.text import MIMEText
from notion_export import push_to_notion  # ✅ Notion export added

# Streamlit page config
st.set_page_config(page_title="Resume Matcher AI", layout="centered")
st.title("📄 Resume Matcher AI")

# Email alert function
def send_email(subject, body, to_email):
    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = "aneelv75@gmail.com"
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login("aneelv75@gmail.com", "kakfojajhvmwtlsn")
        server.send_message(msg)

# Extract text from supported file types
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

# Upload JD and resumes
jd_file = st.file_uploader("Upload Job Description (.txt or .docx)", type=["txt", "docx"])
resumes = st.file_uploader("Upload Resumes (.pdf, .docx, .txt)", type=["pdf", "docx", "txt"], accept_multiple_files=True)

# Match button logic
if st.button("Match Resumes with JD") and jd_file and resumes:
    with tempfile.TemporaryDirectory() as tmpdir:
        jd_path = os.path.join(tmpdir, jd_file.name)
        with open(jd_path, "wb") as f:
            f.write(jd_file.read())

        jd_text = extract_text(jd_path)
        output_data = []

        for resume_file in resumes:
            resume_path = os.path.join(tmpdir, resume_file.name)
            with open(resume_path, "wb") as f:
                f.write(resume_file.read())

            resume_text = extract_text(resume_path)

prompt = f"""You are an expert hiring assistant. Score the following resume against the job description.

Only output in this format:
Score: <number>
Reason: <reason>

JOB DESCRIPTION:
{jd_text}

RESUME:
{resume_text}
"""

            command = ["ollama", "run", "llama3", prompt]
            result = subprocess.run(command, capture_output=True)

            output_text = result.stdout.decode("utf-8", errors="ignore")
            score = 0
            reason = ""

            for line in output_text.splitlines():
                if "score:" in line.lower():
                    try:
                        score = int(line.split(":")[1].strip())
                    except:
                        score = 0
                elif "reason:" in line.lower():
                    reason = line.split(":", 1)[1].strip()

            if not reason.strip():
                reason = "LLM did not provide a reason."

            output_data.append({
                "Resume": resume_file.name,
                "Score": score,
                "Reason": reason
            })

            # ✅ Send each row to Notion
            push_to_notion(resume_file.name, score, reason)

        df = pd.DataFrame(output_data)
        st.success("✅ Matching Complete")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button("⬇ Download CSV", data=csv, file_name="resume_scores.csv", mime="text/csv")

        top = df.sort_values(by="Score", ascending=False).head(3)
        body = top.to_string(index=False)
        send_email(
            subject="Top Resume Matches – Auto Report",
            body=body,
            to_email="aneelv75@gmail.com"
        )
