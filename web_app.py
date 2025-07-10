import streamlit as st
import os
import tempfile
import subprocess
import pandas as pd

# App Title
st.set_page_config(page_title="Resume Matcher AI", layout="centered")
st.title("📄 Resume Matcher AI")

# Upload JD
jd_file = st.file_uploader("Upload Job Description (.txt)", type=["txt"])

# Upload Resumes
resumes = st.file_uploader("Upload Resumes (.pdf, .docx, .txt)", type=["pdf", "docx", "txt"], accept_multiple_files=True)

# Run button
if st.button("Match Resumes with JD") and jd_file and resumes:
    with tempfile.TemporaryDirectory() as tmpdir:
        jd_path = os.path.join(tmpdir, "jd.txt")
        with open(jd_path, "wb") as f:
            f.write(jd_file.read())

        output_data = []

        for resume_file in resumes:
            resume_path = os.path.join(tmpdir, resume_file.name)
            with open(resume_path, "wb") as f:
                f.write(resume_file.read())

            command = ["ollama", "run", "llama3", f"""
            Evaluate this resume based on the job description below:
            JOB DESCRIPTION:
            {open(jd_path).read()}

            RESUME:
            {open(resume_path).read()}

            Return a score out of 100 and a reason.
            Format:
            Score: <number>
            Reason: <reason>
            """]

            result = subprocess.run(command, capture_output=True)
            output_text = result.stdout.decode("utf-8")

            # Parse Score and Reason
            score = 0
            reason = "Could not parse."
            for line in output_text.splitlines():
                if line.lower().startswith("score:"):
                    score = int(line.split(":")[1].strip())
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
