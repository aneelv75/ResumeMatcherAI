
# 🧠 ResumeMatcherAI – Local LLM-Powered Resume Scorer

A local, privacy-friendly resume-to-JD matcher powered by Ollama (LLaMA 3), Python, and Streamlit.

---

## 📁 Folder Structure

```
ResumeMatcherAI/
├── jd/                        # Job descriptions
│   └── jd.txt
├── resumes/                  # Uploaded resumes
│   ├── chaitanya_resume.pdf
│   └── resume.txt
├── output/                   # Scored results
│   ├── result_*.txt
│   ├── scores.csv
│   └── scores.xlsx
├── app.py                    # Backend resume scoring logic
├── web_app.py                # Streamlit-based web UI
├── prompt.txt                # LLM scoring prompt
├── chat.html                 # ChatGPT project archive
├── credentials.json          # Optional API tokens (Notion, etc.)
```

---

## 🚀 Features

- Upload JD + resumes via browser
- Local scoring using `ollama run llama3`
- Output:
  - Score (0–100)
  - Reason for match
- Exports:
  - CSV / Excel
  - Text summary per resume

---

## 🛠 Setup Instructions

1. **Install dependencies:**

```bash
pip install streamlit python-docx pandas fpdf
```

2. **Install and run Ollama:**

```bash
brew install ollama
ollama run llama3
```

3. **Launch the app:**

```bash
streamlit run web_app.py
```

---

## 🔄 Extensible Ideas

- Auto-run via cron or shortcuts
- Pull resumes from Gmail, Drive, or Airtable
- Export results to Notion, GSheets, or Slack
- Add Firebase login for recruiter access
- Build MVP-style SaaS dashboard

---

## 🙌 Built by Anil V  
Using 100% local, open-source tools. Ready to share, deploy, or expand into a recruiter toolkit!
