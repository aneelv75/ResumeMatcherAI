
# 🧠 ResumeMatcherAI

![Python](https://img.shields.io/badge/python-3.9+-blue.svg)
![Streamlit](https://img.shields.io/badge/built%20with-Streamlit-orange)
![License](https://img.shields.io/badge/license-MIT-green)
![Status](https://img.shields.io/badge/status-active-brightgreen)

> **AI-powered Resume Matcher using LLaMA 3 + Streamlit**  
> 100% local, private, recruiter-ready. Built with Python, Ollama, and open-source tools.

---

## 📌 Project Overview

**ResumeMatcherAI** allows recruiters or hiring managers to:
- Upload a Job Description (JD)
- Upload one or more candidate resumes
- Get an instant **score out of 100** + explanation
- Download results as CSV or Excel

All powered locally via **Ollama** + **LLaMA 3**, ensuring privacy and speed — no cloud required.

---

## 🛠 Stack

- 🐍 Python
- 🧠 Ollama (LLaMA 3)
- 🌐 Streamlit
- 📄 PDF / DOCX parser
- 🗂 Notion / Airtable-ready output (optional)

---

## 🚀 Features

- Upload JD (.txt) + Resumes (.pdf, .docx)
- Score resumes using local LLM
- View results in a browser UI
- Download CSV/Excel with Score + Reason
- Fully offline-capable
- Extensible: Notion, Airtable, Email

---

## 🖥️ Demo

![Demo](https://github.com/aneelv75/ResumeMatcherAI/assets/demo-screenshot.png)  
> Replace this with a screenshot or demo GIF of your Streamlit UI

---

## 📂 Project Structure

```
ResumeMatcherAI/
├── input/
│   ├── jd.txt
│   └── resumes/
├── output/
│   ├── scores.csv / scores.xlsx
├── web_app.py          # Streamlit UI
├── app.py              # Backend logic
├── prompt.txt          # LLM scoring prompt
├── README.md
```

---

## ⚙️ Installation

1. Clone the repository

```bash
git clone https://github.com/aneelv75/ResumeMatcherAI.git
cd ResumeMatcherAI
```

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Install & run Ollama + LLaMA 3

```bash
brew install ollama
ollama run llama3
```

4. Launch the web app

```bash
streamlit run web_app.py
```

---

## ✨ Sample Output

| Resume           | Score | Reason                                       |
|------------------|-------|----------------------------------------------|
| john_doe.pdf     | 86    | Matches Python + NLP, lacks domain exposure |
| jane_smith.docx  | 65    | Good experience but not JD-aligned          |

---

## 🔧 Roadmap

- [ ] Add multi-JD matching
- [ ] Auto-email shortlists to hiring managers
- [ ] Integrate Notion & Airtable dashboards
- [ ] Schedule auto-runs (daily/weekly)

---

## 🙌 Author

Built with ❤️ by [Anil V](https://github.com/aneelv75)

---

## 📄 License

This project is licensed under the [MIT License](LICENSE)
