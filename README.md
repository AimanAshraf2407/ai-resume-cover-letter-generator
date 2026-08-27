# AI Resume & Cover Letter Generator (BIT4543 Group Project)

## 📌 Project Overview
An AI-powered system designed to generate tailored resumes and cover letters by matching user profiles against target job descriptions.

## 👥 Team Members & Roles
- **Person 1 (AI / Backend Lead):** Prompt engineering, API integration, and AI generation pipelines.
- **Person 2 (Frontend Lead):** User interface, form handling, and document export features.
- **Person 3 (Testing & Documentation Lead):** Evaluation datasets, quality metrics, testing, and GitHub management.

## 🛠️ Project Structure
- `data/`: Sample user profiles and target job postings.
- `notebooks/`: Prompt experimentation and evaluation notebooks.
- `src/` & `models/`: LLM client handlers, prompt templates, and core logic.
- `app/`: Web frontend and API routing.
- `docs/`: Proposal, progress reports, and architectural diagrams.
- `results/`: Evaluation benchmark results and match rate logs.
- `tests/`: Automated unit and integration tests.

## 🚀 Getting Started
1. Clone the repo: `git clone <repo-url>`
2. Install Python dependencies: `pip install -r requirements.txt`
3. Set environment variables: Copy `.env.example` to `.env` and insert your API key.
4. Run the server: `uvicorn app.main:app --reload`