# 🤖 CareerForge – Your AI Career Assistant

CareerForge is an intelligent resume assistant powered by AI that helps job seekers:
- Match their resume to job descriptions
- Get resume critique and improvement suggestions
- Generate tailored cover letters
- Simulate interviews and get feedback
- Email the full analysis in a downloadable PDF

🎯 **Perfect for:** students, professionals, or anyone applying for jobs!

---

## ✨ Features

| Feature | Description |
|--------|-------------|
| 🧠 Skill Match | Compares resume skills with job description and highlights missing skills |
| 📊 Job Fit Score | AI analyzes job relevance and generates a radar graph |
| 📋 Resume Critique | Get structured feedback on resume content and formatting |
| ✉️ Cover Letter Generator | Create a tailored cover letter instantly |
| 🎤 Interview Q&A | Practice likely interview questions with AI feedback |
| 📧 Email Results | Send your full analysis (as PDF) to your email |

---

## 🚀 How to Run Locally

### 1. Clone the Repo
```bash
git clone https://github.com/yourusername/careerforge.git
cd careerforge
```

### 2. Create & Activate Virtual Environment
```bash
python -m venv venv
# Windows
venv\Scripts\activate
# macOS/Linux
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Add Environment Variables

Create a `.env` file in the root directory with:

```
OPENROUTER_API_KEY=your-api-key-here
```

> ⚠️ Never commit your `.env` file to GitHub. It contains sensitive keys.

### 5. Run the App
```bash
streamlit run app.py
```

---

## 📁 Project Structure

```
careerforge/
│
├── app.py                   # Main Streamlit app
├── resume_critic.py        # AI-based resume critique logic
├── resume_parser.py        # PDF resume parser
├── job_fit.py              # Radar chart & job fit scoring
├── jd_analyzer.py          # JD skill extraction & comparison
├── cover_letter_gen.py     # Cover letter generator
├── interview_bot.py        # Interview Q&A engine
├── email_utils.py          # Email PDF sending logic
├── requirements.txt        # All dependencies
├── .env.example            # Sample env file
├── data/                   # Contains temp_resume.pdf
│   └── temp_resume.pdf     # Generated at runtime
```

---

## ☁️ Deployment (Streamlit, Render, etc.)

1. Push the repo to GitHub.
2. Add environment variables (like `OPENROUTER_API_KEY`) in the deployment dashboard.
3. Your app is live! 🌐

---

## 🛡️ Security Note

- `.env` is in `.gitignore` to protect API keys.
- Make sure to configure secrets in your deployment platform.

---

## 👤 Author

**Garima Dua**  
🚀 CareerForge – Built with ❤️ in 2025

---

## 📄 License

This project is licensed under the MIT License.
## 📸 Screenshots
### 🔹 Intro & Resume & JD Upload
![Intro](https://github.com/user-attachments/assets/4bdb5f89-c940-4b33-af99-dd214a1aef69)
![Resume & JD upload](https://github.com/user-attachments/assets/81b412b8-0df7-4f53-ac5d-77947d126f5d)

### 🔹 Skill Match & Job Fit
![Skill Match](https://github.com/user-attachments/assets/0a9583c9-0f47-4fac-9135-461c56dca04a)
![Job Fit](https://github.com/user-attachments/assets/b38d7efb-9ad3-4625-9fa2-11248b687029)

### 🔹 Resume Critique & Cover Letter
![Critique](https://github.com/user-attachments/assets/04e5f34d-e1a1-4c09-ba45-e71f2ebfd463)
![Cover Letter](https://github.com/user-attachments/assets/796803c1-dca9-4eb8-905f-298d6c1c53d8)

### 🔹 Interview Q&A & Email
![Interview](https://github.com/user-attachments/assets/d04c364d-56ec-485a-82b1-27779b5754c5)
![Email](https://github.com/user-attachments/assets/75bdb516-9e52-45e7-b047-7618bc623dfa)



























