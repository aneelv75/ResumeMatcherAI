
import streamlit as st
import os
import tempfile
import pandas as pd
import requests

# ✅ Together.ai API Setup
TOGETHER_API_KEY = "9bd11a3547ac3106bfedc8f4dd60c96bf1c21355ab39ac50e753b1169de9a12c"
TOGETHER_API_URL = "https://api.together.xyz/v1/chat/completions"
MODEL = "meta-llama/Llama-3-8b-chat-hf"

st.set_page_config(page_title="Resume Matcher AI (Together.ai)", layout="centered")
st.title("📄 Resume Matcher AI")

# Upload JD and Resumes
jd_file = st.file_uploader("Upload Job Description (.txt or .docx)", type=["txt", "docx"])
resumes = st.file_uploader("Upload Resumes (.pdf, .docx, .txt)", type=["pdf", "docx", "txt"], accept_multiple_files=True)

# Toggle for debugging output
show_debug = st.checkbox("💬 Show Raw AI Replies (for debugging)", value=False)

# Call Together API
def get_score_and_reason(prompt):
    headers = {
        "Authorization": f"Bearer {TOGETHER_API_KEY}",
        "Content-Type": "application/json"
    }
    data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are an AI assistant that evaluates resumes for job fit."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.4
    }

    try:
        response = requests.post(TOGETHER_API_URL, headers=headers, json=data, timeout=60)
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Score: 0\nReason: Could not evaluate. Error {response.status_code}: {response.text}"
    except Exception as e:
        return f"Score: 0\nReason: API call failed. {str(e)}"

# Run the Matching
if st.button("Match Resumes with JD") and jd_file and resumes:
    with tempfile.TemporaryDirectory() as tmpdir:
        jd_path = os.path.join(tmpdir, "jd.txt")
        with open(jd_path, "wb") as f:
            f.write(jd_file.read())
        jd_text = open(jd_path, "r", encoding="utf-8", errors="ignore").read()
        jd_text = jd_text[:1000]  # Limit length for stability

        output_data = []
        debug_outputs = {}

        for resume_file in resumes:
            resume_path = os.path.join(tmpdir, resume_file.name)
            with open(resume_path, "wb") as f:
                f.write(resume_file.read())
            resume_text = open(resume_path, "r", encoding="utf-8", errors="ignore").read()
            resume_text = resume_text[:1000]

            prompt = f"""Evaluate the following resume based on the job description.
Provide a Score out of 100 followed by reasoning.

JOB DESCRIPTION:
{jd_text}

RESUME:
{resume_text}
"""

            response_text = get_score_and_reason(prompt)
            debug_outputs[resume_file.name] = response_text

            # Extract score
            score = 0
            reason = response_text.strip()
            for line in response_text.splitlines():
                if "score" in line.lower():
                    try:
                        score = int(''.join(filter(str.isdigit, line)))
                        reason = response_text.replace(line, "").strip()
                        break
                    except:
                        score = 0
            output_data.append({
                "Resume": resume_file.name,
                "Score": score,
                "Reason": reason if reason else "LLM did not provide an explanation."
            })

        df = pd.DataFrame(output_data)
        st.success("✅ Matching Complete")
        st.dataframe(df)

        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button("⬇ Download CSV", data=csv, file_name="resume_scores.csv", mime='text/csv')

        if show_debug:
            st.subheader("🪵 Raw AI Replies")
            for name, raw in debug_outputs.items():
                st.text_area(f"Raw Output: {name}", value=raw, height=200)
