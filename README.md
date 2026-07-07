# CampusPilot AI

CampusPilot AI is an AI-powered Decision Intelligence Platform foundation for engineering students and faculty.

## Scope

This version only includes the Streamlit project foundation:

- Home page
- Student profile form
- Faculty analytics dashboard with mock data
- About page
- Career path knowledge JSON
- Mock student dataset

Gemini, AI agents, and authentication are intentionally not implemented in this foundation.

## Project Structure

```text
CampusPilotAI/
├── app.py
├── pages/
│   ├── student.py
│   ├── faculty.py
│   └── about.py
├── knowledge/
│   └── career_paths.json
├── data/
│   └── students.csv
├── assets/
├── requirements.txt
└── README.md
```

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Notes

The current faculty dashboard uses mock student data from `data/students.csv`. Future modules can add AI-driven analysis, personalized recommendations, and agent workflows.
