from html import escape

import plotly.graph_objects as go
import streamlit as st

from agents import (
    academic_agent,
    career_agent,
    coordinator_agent,
    decision_agent,
    generate_gemini_decision_summary,
)


STUDENT_FORM_DEFAULTS = {
    "name": "",
    "year": "1st Year",
    "branch": "Computer Science",
    "career_goal": "Data Analyst",
    "skills": "",
    "projects_completed": 0,
    "short_description": "",
}


def load_student_form_state() -> None:
    st.session_state.setdefault("student_form_data", STUDENT_FORM_DEFAULTS.copy())
    form_data = st.session_state["student_form_data"]
    for field, value in form_data.items():
        widget_key = f"student_form_{field}"
        default_value = STUDENT_FORM_DEFAULTS[field]
        current_value = st.session_state.get(widget_key, default_value)
        if widget_key not in st.session_state or (
            value != default_value and current_value == default_value
        ):
            st.session_state[widget_key] = value


def save_student_form_state(
    name: str,
    year: str,
    branch: str,
    career_goal: str,
    skills: str,
    projects_completed: int,
    short_description: str,
) -> None:
    st.session_state["student_form_data"] = {
        "name": name,
        "year": year,
        "branch": branch,
        "career_goal": career_goal,
        "skills": skills,
        "projects_completed": projects_completed,
        "short_description": short_description,
    }


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
            max-width: 980px;
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }

        h1, h2, h3, p, label {
            color: var(--text);
            letter-spacing: 0;
        }

        .page-header {
            padding: 1.45rem 1.6rem;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            box-shadow: var(--shadow);
            margin-bottom: 1.5rem;
        }

        .page-header h1 {
            margin: 0 0 0.4rem 0;
            color: var(--text);
            letter-spacing: 0;
        }

        .page-header p {
            margin: 0;
            color: var(--muted);
        }

        [data-testid="stForm"] {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.35rem;
            box-shadow: var(--shadow);
        }

        input, textarea, [data-baseweb="select"] > div {
            border-radius: 16px !important;
        }

        input, textarea {
            color: var(--text) !important;
        }

        [data-baseweb="select"] span {
            color: var(--text) !important;
        }

        div.stButton > button, div.stFormSubmitButton > button {
            background: var(--primary);
            color: white;
            border: 0;
            border-radius: 16px;
            padding: 0.72rem 1.35rem;
            font-weight: 700;
            box-shadow: 0 8px 18px rgba(26, 115, 232, 0.24);
        }

        div.stButton > button:hover, div.stFormSubmitButton > button:hover {
            background: var(--secondary);
            color: white;
            border: 0;
        }

        .result-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.25rem;
            box-shadow: var(--shadow);
            min-height: 138px;
            margin-bottom: 1rem;
        }

        .result-card h3 {
            color: var(--text);
            font-size: 1.05rem;
            margin: 0 0 0.7rem 0;
            letter-spacing: 0;
            display: flex;
            align-items: center;
            gap: 0.45rem;
        }

        .section-icon {
            display: inline-flex;
            align-items: center;
            justify-content: center;
            width: 1.6rem;
            height: 1.6rem;
            border-radius: 10px;
            background: var(--surface-soft);
            color: var(--primary);
            font-size: 1rem;
            flex: 0 0 auto;
        }

        .result-card p, .result-card li {
            color: var(--muted);
            line-height: 1.55;
            margin-bottom: 0.35rem;
        }

        .pill {
            display: inline-block;
            background: var(--surface-soft);
            color: var(--primary);
            border-radius: 999px;
            padding: 0.38rem 0.72rem;
            margin: 0.18rem;
            font-size: 0.9rem;
            font-weight: 700;
        }

        .decision-grid {
            display: grid;
            grid-template-columns: repeat(2, minmax(0, 1fr));
            gap: 0.8rem;
            margin-bottom: 0.8rem;
        }

        .decision-item {
            background: var(--surface-soft);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 0.9rem;
        }

        .decision-label {
            color: var(--muted);
            font-size: 0.82rem;
            font-weight: 700;
            margin-bottom: 0.25rem;
        }

        .decision-value {
            color: var(--text);
            font-weight: 800;
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

        @media (max-width: 760px) {
            .decision-grid {
                grid-template-columns: 1fr;
            }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_card(title: str, body: str, icon: str = "") -> None:
    heading = (
        f'<span class="section-icon">{icon}</span>{escape(title)}'
        if icon
        else escape(title)
    )
    st.markdown(
        f"""
        <div class="result-card">
            <h3>{heading}</h3>
            {body}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_pills(items: list[str]) -> str:
    if not items:
        return "<p>No gaps detected for the selected career path.</p>"
    return "".join(f'<span class="pill">{escape(item)}</span>' for item in items)


inject_styles()
load_student_form_state()

st.markdown(
    """
    <div class="page-header">
        <h1>Student Profile Analysis</h1>
        <p>Enter academic and career details to prepare for the next decision module.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

with st.form("student_profile_form"):
    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Name", key="student_form_name")
        year = st.selectbox(
            "Year",
            ["1st Year", "2nd Year", "3rd Year", "4th Year"],
            key="student_form_year",
        )
        branch = st.selectbox(
            "Branch",
            [
                "Computer Science",
                "Information Technology",
                "Electronics and Communication",
                "Electrical Engineering",
                "Mechanical Engineering",
                "Civil Engineering",
                "Artificial Intelligence and Data Science",
            ],
            key="student_form_branch",
        )

    with col2:
        career_goal = st.selectbox(
            "Career Goal",
            ["Data Analyst", "Software Engineer", "AI Engineer", "Cloud Engineer", "Product Manager", "Cybersecurity Analyst"],
            key="student_form_career_goal",
        )
        skills = st.text_input("Skills (comma separated)", key="student_form_skills")
        projects_completed = st.number_input(
            "Projects Completed",
            min_value=0,
            max_value=30,
            step=1,
            key="student_form_projects_completed",
        )

    short_description = st.text_area(
        "Short Description",
        height=140,
        key="student_form_short_description",
    )

    submitted = st.form_submit_button("Analyze My Profile")

if submitted:
    save_student_form_state(
        name=name,
        year=year,
        branch=branch,
        career_goal=career_goal,
        skills=skills,
        projects_completed=projects_completed,
        short_description=short_description,
    )

    student_profile = coordinator_agent(
        year=year,
        branch=branch,
        career_goal=career_goal,
        skills=skills,
        projects_completed=projects_completed,
        description=short_description,
    )
    academic_output = academic_agent(student_profile)
    career_output = career_agent(student_profile)
    decision_output = decision_agent(student_profile, academic_output, career_output)
    ai_summary = generate_gemini_decision_summary(student_profile, decision_output)

    score = decision_output["placement_readiness"]
    projected_score = decision_output["estimated_readiness_after_roadmap"]

    st.markdown("### AI Decision Intelligence Results")

    gauge = go.Figure(
        go.Indicator(
            mode="gauge+number",
            value=score,
            number={"suffix": "%", "font": {"color": "#172b4d"}},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#1a73e8"},
                "steps": [
                    {"range": [0, 50], "color": "#fdecea"},
                    {"range": [50, 75], "color": "#fff7e0"},
                    {"range": [75, 100], "color": "#e6f4ea"},
                ],
            },
            title={"text": "Placement Readiness"},
        )
    )
    gauge.update_layout(height=280, margin={"t": 55, "b": 20, "l": 30, "r": 30})
    st.plotly_chart(gauge, use_container_width=True)

    col1, col2 = st.columns(2)
    with col1:
        render_card("Strengths", render_pills(decision_output["strengths"]), "&#9989;")
    with col2:
        render_card("Missing Skills", render_pills(decision_output["missing_skills"]), "&#9888;")

    col3, col4 = st.columns(2)
    with col3:
        render_card(
            "Recommended Project",
            f"<p>{escape(decision_output['recommended_project'])}</p>",
            "&#128736;",
        )
    with col4:
        render_card(
            "Recommended Certification",
            f"<p>{escape(decision_output['certification'])}</p>",
            "&#127891;",
        )

    render_card(
        "Recommended Platforms",
        render_pills(decision_output["recommended_platforms"]),
        "&#128279;",
    )

    roadmap_items = "".join(
        f"<li><strong>{escape(item['week'])}:</strong> {escape(item['focus'])}</li>"
        for item in decision_output["learning_roadmap"]
    )
    render_card("30-Day Learning Roadmap", f"<ul>{roadmap_items}</ul>", "&#128506;")

    decision_body = f"""
        <div class="decision-grid">
            <div class="decision-item">
                <div class="decision-label">Current Position</div>
                <div class="decision-value">{escape(decision_output['current_position'])}</div>
            </div>
            <div class="decision-item">
                <div class="decision-label">Career Goal</div>
                <div class="decision-value">{escape(decision_output['career_goal'])}</div>
            </div>
            <div class="decision-item">
                <div class="decision-label">Confidence Level</div>
                <div class="decision-value">{escape(decision_output['confidence_level'])}</div>
            </div>
            <div class="decision-item">
                <div class="decision-label">Immediate Next Action</div>
                <div class="decision-value">{escape(decision_output['immediate_next_action'])}</div>
            </div>
            <div class="decision-item">
                <div class="decision-label">Estimated Placement Readiness</div>
                <div class="decision-value">{score}% &rarr; {projected_score}%</div>
            </div>
        </div>
        <p><strong>Why this recommendation:</strong> {escape(decision_output['why_this_recommendation'])}</p>
        <p>{escape(ai_summary)}</p>
    """
    render_card("AI Decision Card", decision_body, "&#128161;")

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
