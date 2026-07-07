import streamlit as st


def inject_styles() -> None:
    st.markdown(
        """
        <style>
        :root {
            --primary: #1A73E8;
            --secondary: #4285F4;
            --success: #34A853;
            --warning: #FBBC04;
            --error: #EA4335;
            --app-bg: #F8FAFC;
            --surface: #FFFFFF;
            --surface-soft: #EFF6FF;
            --text: #1F2937;
            --muted: #64748B;
            --border: #E5E7EB;
            --shadow: 0 8px 24px rgba(15, 23, 42, 0.08);
        }

        @media (prefers-color-scheme: dark) {
            :root {
                --app-bg: #0F172A;
                --surface: #1E293B;
                --surface-soft: #172554;
                --text: #F8FAFC;
                --muted: #CBD5E1;
                --border: #334155;
                --shadow: 0 8px 24px rgba(0, 0, 0, 0.28);
            }
        }

        .stApp {
            background: var(--app-bg);
            color: var(--text);
            font-family: "Inter", "Roboto", "Segoe UI", sans-serif;
        }

        [data-testid="stSidebar"] {
            background: var(--surface);
            border-right: 1px solid var(--border);
        }

        [data-testid="stSidebar"] *,
        [data-testid="stSidebar"] a,
        [data-testid="stSidebar"] a span,
        [data-testid="stSidebar"] p {
            color: var(--text) !important;
        }

        .main .block-container {
            max-width: 960px;
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }

        .content-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 2rem;
            box-shadow: var(--shadow);
        }

        .content-card h1, .content-card h2 {
            color: var(--text);
            letter-spacing: 0;
        }

        .content-card p, .content-card li {
            color: var(--muted);
            font-size: 1.02rem;
            line-height: 1.7;
        }

        .note {
            background: var(--surface-soft);
            color: var(--text);
            border-radius: 16px;
            padding: 1rem 1.2rem;
            font-weight: 700;
            margin-top: 1.4rem;
        }

        .flow {
            display: grid;
            grid-template-columns: repeat(4, minmax(0, 1fr));
            gap: 0.85rem;
            margin: 1rem 0 1.4rem 0;
        }

        .flow-step {
            background: var(--surface-soft);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1rem;
            color: var(--text);
            font-weight: 800;
            text-align: center;
        }

        .footer {
            margin-top: 1.6rem;
            padding: 1.1rem 1.25rem;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            box-shadow: var(--shadow);
            color: var(--muted);
            text-align: center;
            line-height: 1.55;
            font-size: 0.9rem;
        }

        .footer strong {
            color: var(--text);
        }

        @media (max-width: 780px) {
            .flow {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


inject_styles()

st.markdown(
    """
    <div class="content-card">
        <h1>About CampusPilot AI</h1>
        <p>
            CampusPilot AI is an AI-powered Decision Intelligence Platform designed
            to help engineering students make smarter academic and career decisions.
            The platform brings student profiles, career goals, skills, project
            experience, and placement readiness into one focused interface.
        </p>
        <h2>Implemented Workflow</h2>
        <div class="flow">
            <div class="flow-step">Student Profile</div>
            <div class="flow-step">AI Decision Intelligence</div>
            <div class="flow-step">Career Recommendation</div>
            <div class="flow-step">Faculty Analytics Dashboard</div>
        </div>
        <h2>How it works</h2>
        <p>
            Students enter their academic context, skills, projects, and target role.
            The decision engine compares the profile against career-path knowledge,
            estimates placement readiness, identifies missing skills, and creates a
            focused 30-day roadmap with project and certification recommendations.
        </p>
        <h2>Gemini Integration</h2>
        <p>
            Gemini integration is optional. When a Gemini API key is available, the
            app generates a personalized explanation for the student. If the key is
            unavailable, CampusPilot AI gracefully falls back to the local decision
            intelligence engine so the workflow remains fully usable.
        </p>
        <div class="note">
            Built as a polished hackathon prototype for student success and faculty insight.
        </div>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    """
    <footer class="footer">
        <strong>CampusPilot AI</strong><br>
        AI Decision Intelligence Platform for Student Success<br>
        Built for Google Cloud Gen AI APAC Hackathon 2026<br>
        Powered by Streamlit &bull; Gemini &bull; Decision Intelligence
    </footer>
    """,
    unsafe_allow_html=True,
)
