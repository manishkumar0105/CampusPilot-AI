import streamlit as st


st.set_page_config(
    page_title="CampusPilot AI",
    page_icon="CP",
    layout="wide",
    initial_sidebar_state="expanded",
)


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

        [data-testid="stSidebar"] * {
            color: var(--text) !important;
        }

        [data-testid="stSidebar"] a,
        [data-testid="stSidebar"] a span,
        [data-testid="stSidebar"] p {
            color: var(--text) !important;
        }

        .main .block-container {
            padding-top: 1.5rem;
            padding-bottom: 2rem;
            max-width: 1180px;
        }

        h1, h2, h3, p, label {
            color: var(--text);
            letter-spacing: 0;
        }

        .hero {
            padding: 2.35rem 2.3rem;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            box-shadow: var(--shadow);
            margin-bottom: 1.1rem;
        }

        .eyebrow {
            color: var(--primary);
            font-size: 0.9rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.08rem;
            margin-bottom: 0.8rem;
        }

        .hero-title {
            font-size: clamp(2.4rem, 5vw, 4.2rem);
            line-height: 1.02;
            font-weight: 800;
            margin: 0;
        }

        .hero-note {
            color: var(--muted);
            font-size: 0.98rem;
            line-height: 1.65;
            max-width: 780px;
            margin: 0.75rem 0 1.35rem 0;
        }

        .tagline {
            color: var(--secondary);
            font-size: 1.35rem;
            font-weight: 700;
            margin-top: 0.9rem;
            margin-bottom: 0.35rem;
        }

        .subtitle {
            color: var(--muted);
            font-size: 1.05rem;
            max-width: 720px;
            margin-bottom: 1.4rem;
        }

        .feature-card {
            min-height: 156px;
            padding: 1.25rem;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            box-shadow: var(--shadow);
        }

        .feature-icon {
            width: 44px;
            height: 44px;
            border-radius: 16px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: var(--surface-soft);
            color: var(--primary);
            font-size: 1.25rem;
            font-weight: 800;
            margin-bottom: 0.95rem;
        }

        .feature-title {
            font-size: 1.05rem;
            font-weight: 800;
            margin-bottom: 0.35rem;
        }

        .feature-copy {
            color: var(--muted);
            font-size: 0.92rem;
            line-height: 1.55;
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

        div.stButton > button {
            background: var(--primary);
            color: white;
            border: 0;
            border-radius: 16px;
            padding: 0.72rem 1.45rem;
            font-weight: 700;
            box-shadow: 0 8px 18px rgba(26, 115, 232, 0.24);
        }

        div.stButton > button:hover {
            background: var(--secondary);
            color: white;
            border: 0;
        }

        @media (max-width: 900px) {
            .hero {
                padding: 1.7rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def home() -> None:
    inject_styles()

    st.sidebar.title("CampusPilot AI")
    st.sidebar.caption("Decision intelligence for engineering campuses")

    st.markdown(
        """
        <section class="hero">
            <div class="eyebrow">Decision Intelligence Platform</div>
            <h1 class="hero-title">CampusPilot AI</h1>
            <div class="tagline">Helping Students Decide What To Do Next</div>
            <p class="subtitle">
                AI-Powered Decision Intelligence Platform for Engineering Students
            </p>
            <p class="hero-note">
                A polished decision workspace for students to understand readiness,
                identify skill gaps, and act on a clear 30-day career plan.
            </p>
        </section>
        """,
        unsafe_allow_html=True,
    )

    if st.button("Get Started", type="primary"):
        st.info("Open the Student page from the sidebar to begin.")

    st.markdown("### Platform Capabilities")

    features = [
        ("&#128218;", "Academic Guidance", "Help students connect coursework, projects, and skills to practical next steps."),
        ("&#127919;", "Placement Readiness", "Surface readiness signals from skills, project depth, and career direction."),
        ("&#128506;", "Career Roadmaps", "Show structured pathways for in-demand engineering career goals."),
        ("&#128202;", "Faculty Analytics", "Give faculty a campus-level view of readiness and skill gaps."),
    ]

    cols = st.columns(4)
    for col, (icon, title, copy) in zip(cols, features):
        with col:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="feature-icon">{icon}</div>
                    <div class="feature-title">{title}</div>
                    <div class="feature-copy">{copy}</div>
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


navigation = st.navigation(
    [
        st.Page(home, title="Home"),
        st.Page("pages/student.py", title="Student"),
        st.Page("pages/faculty.py", title="Faculty"),
        st.Page("pages/about.py", title="About"),
    ]
)
navigation.run()
