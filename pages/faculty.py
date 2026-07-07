from collections import Counter
from pathlib import Path

import pandas as pd
import plotly.express as px
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
            max-width: 1180px;
            padding-top: 1.5rem;
            padding-bottom: 2rem;
        }

        .page-header {
            padding: 1.45rem 1.6rem;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            box-shadow: var(--shadow);
            margin-bottom: 1.4rem;
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

        .metric-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1.2rem;
            box-shadow: var(--shadow);
            min-height: 122px;
        }

        .metric-label {
            color: var(--muted);
            font-size: 0.9rem;
            font-weight: 700;
            margin-bottom: 0.55rem;
        }

        .metric-value {
            color: var(--primary);
            font-size: 2.2rem;
            font-weight: 850;
            line-height: 1;
        }

        .metric-note {
            color: var(--muted);
            font-size: 0.82rem;
            margin-top: 0.6rem;
        }

        .chart-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 1rem;
            box-shadow: var(--shadow);
        }

        h1, h2, h3 {
            color: var(--text);
            letter-spacing: 0;
        }

        p, label {
            color: var(--text);
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
        </style>
        """,
        unsafe_allow_html=True,
    )


def split_skills(value: str) -> list[str]:
    return [skill.strip() for skill in str(value).split(",") if skill.strip()]


inject_styles()

st.markdown(
    """
    <div class="page-header">
        <h1>Faculty Analytics</h1>
        <p>Mock student insights for readiness, goals, and campus skill gaps.</p>
    </div>
    """,
    unsafe_allow_html=True,
)

project_root = Path(__file__).resolve().parents[1]
students = pd.read_csv(project_root / "data" / "students.csv")

total_students = len(students)
placement_ready = int((students["Placement Readiness"] == "Ready").sum())
need_resume_training = int(students["Missing Skills"].str.contains("Resume", case=False, na=False).sum())
need_communication_skills = int(students["Missing Skills"].str.contains("Communication", case=False, na=False).sum())

metrics = [
    ("Total Students", total_students, "Mock profiles in the current dataset"),
    ("Placement Ready", placement_ready, "Students marked ready for placements"),
    ("Need Resume Training", need_resume_training, "Students missing resume preparation"),
    ("Need Communication Skills", need_communication_skills, "Students missing communication skills"),
]

metric_cols = st.columns(4)
for col, (label, value, note) in zip(metric_cols, metrics):
    with col:
        st.markdown(
            f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-note">{note}</div>
            </div>
            """,
            unsafe_allow_html=True,
        )

st.markdown("### Skill Gap and Readiness Overview")

missing_skill_counts = Counter()
for missing_skills in students["Missing Skills"]:
    missing_skill_counts.update(split_skills(missing_skills))

missing_skills_df = (
    pd.DataFrame(missing_skill_counts.items(), columns=["Skill", "Students"])
    .sort_values("Students", ascending=False)
    .head(10)
)

goal_distribution = students["Career Goal"].value_counts().reset_index()
goal_distribution.columns = ["Career Goal", "Students"]

readiness_distribution = students["Placement Readiness"].value_counts().reset_index()
readiness_distribution.columns = ["Placement Readiness", "Students"]

plot_template = "plotly_white"
blue_palette = ["#1a73e8", "#34a853", "#fbbc04", "#ea4335", "#5f6c7b", "#46bdc6"]

fig_missing = px.bar(
    missing_skills_df,
    x="Students",
    y="Skill",
    orientation="h",
    title="Top Missing Skills",
    color="Students",
    color_continuous_scale=["#dce7f7", "#1a73e8"],
    template=plot_template,
)
fig_missing.update_layout(yaxis={"categoryorder": "total ascending"}, coloraxis_showscale=False)

fig_goals = px.pie(
    goal_distribution,
    names="Career Goal",
    values="Students",
    title="Career Goal Distribution",
    color_discrete_sequence=blue_palette,
    hole=0.42,
    template=plot_template,
)

fig_readiness = px.bar(
    readiness_distribution,
    x="Placement Readiness",
    y="Students",
    title="Placement Readiness Distribution",
    color="Placement Readiness",
    color_discrete_sequence=blue_palette,
    template=plot_template,
)

chart_col1, chart_col2 = st.columns([1.1, 0.9])
with chart_col1:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_missing, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with chart_col2:
    st.markdown('<div class="chart-card">', unsafe_allow_html=True)
    st.plotly_chart(fig_goals, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

st.markdown('<div class="chart-card">', unsafe_allow_html=True)
st.plotly_chart(fig_readiness, use_container_width=True)
st.markdown("</div>", unsafe_allow_html=True)

with st.expander("View mock student data"):
    st.dataframe(students, use_container_width=True, hide_index=True)

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
