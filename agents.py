import json
import os
import re
import urllib.error
import urllib.request
from pathlib import Path


FIXED_PLATFORMS = [
    "Unstop",
    "Google for Developers",
    "LinkedIn Jobs",
    "Devpost",
]


def _career_paths_path() -> Path:
    return Path(__file__).resolve().parent / "knowledge" / "career_paths.json"


def _load_career_paths() -> dict:
    with _career_paths_path().open(encoding="utf-8") as career_file:
        return json.load(career_file)


def _parse_skills(skills: str | list[str]) -> list[str]:
    if isinstance(skills, list):
        raw_skills = skills
    else:
        raw_skills = re.split(r"[,;\n]", skills or "")

    normalized = []
    seen = set()
    for skill in raw_skills:
        clean_skill = str(skill).strip()
        key = clean_skill.casefold()
        if clean_skill and key not in seen:
            normalized.append(clean_skill)
            seen.add(key)
    return normalized


def _year_score(year: str) -> float:
    year_value = {
        "1st Year": 0.25,
        "2nd Year": 0.50,
        "3rd Year": 0.75,
        "4th Year": 1.00,
    }
    return year_value.get(year, 0.50)


def _career_alignment_score(branch: str, career_goal: str) -> float:
    branch_text = branch.casefold()
    career_text = career_goal.casefold()

    strong_matches = {
        "Data Analyst": ["computer", "information", "artificial intelligence", "data"],
        "Software Engineer": ["computer", "information", "artificial intelligence", "data"],
        "AI Engineer": ["artificial intelligence", "data", "computer", "information"],
        "Cloud Engineer": ["computer", "information", "electronics", "electrical"],
    }

    if career_goal not in strong_matches:
        return 0.55
    if any(match in branch_text for match in strong_matches[career_goal]):
        return 1.00
    if any(token in branch_text for token in career_text.split()):
        return 0.80
    return 0.65


def _confidence_label(score: int) -> str:
    if score >= 85:
        return "High"
    if score >= 70:
        return "Good"
    if score >= 55:
        return "Developing"
    return "Needs Focus"


def coordinator_agent(
    year: str,
    branch: str,
    career_goal: str,
    skills: str,
    projects_completed: int,
    description: str,
) -> dict:
    return {
        "year": year,
        "branch": branch,
        "career_goal": career_goal,
        "skills": _parse_skills(skills),
        "projects_completed": int(projects_completed or 0),
        "description": description.strip(),
    }


def academic_agent(student_profile: dict) -> dict:
    career_paths = _load_career_paths()
    career_goal = student_profile["career_goal"]
    career_data = career_paths.get(career_goal, {})
    required_skills = career_data.get("Required Skills", [])
    current_skills = {skill.casefold() for skill in student_profile["skills"]}
    missing_skills = [
        skill for skill in required_skills if skill.casefold() not in current_skills
    ]

    priority_skills = missing_skills or required_skills[:2] or ["Core technical skill"]
    first_skill = priority_skills[0]
    second_skill = priority_skills[1] if len(priority_skills) > 1 else first_skill
    recommended_project = (
        career_data.get("Recommended Projects", ["Career-focused portfolio project"])[0]
    )

    return {
        "recommended_skills": required_skills,
        "recommended_project": recommended_project,
        "recommended_certification": career_data.get(
            "Recommended Certifications", ["Foundational career certification"]
        )[0],
        "learning_roadmap": [
            {
                "week": "Week 1",
                "focus": f"Learn highest priority missing skill: {first_skill}",
            },
            {
                "week": "Week 2",
                "focus": f"Learn second priority skill: {second_skill}",
            },
            {
                "week": "Week 3",
                "focus": f"Build recommended project: {recommended_project}",
            },
            {
                "week": "Week 4",
                "focus": "Improve resume and apply for opportunities",
            },
        ],
        "recommended_platforms": FIXED_PLATFORMS,
    }


def career_agent(student_profile: dict) -> dict:
    career_paths = _load_career_paths()
    career_goal = student_profile["career_goal"]
    career_data = career_paths.get(career_goal, {})
    required_skills = career_data.get("Required Skills", [])
    current_skills = student_profile["skills"]
    current_skill_keys = {skill.casefold() for skill in current_skills}

    matched_skills = [
        skill for skill in required_skills if skill.casefold() in current_skill_keys
    ]
    missing_skills = [
        skill for skill in required_skills if skill.casefold() not in current_skill_keys
    ]

    technical_score = (
        len(matched_skills) / len(required_skills) if required_skills else 0.0
    )
    project_score = min(student_profile["projects_completed"] / 4, 1.0)
    year_progress_score = _year_score(student_profile["year"])
    alignment_score = _career_alignment_score(student_profile["branch"], career_goal)

    readiness_score = round(
        (technical_score * 60)
        + (project_score * 20)
        + (year_progress_score * 10)
        + (alignment_score * 10)
    )

    strengths = matched_skills[:]
    if student_profile["projects_completed"] >= 2:
        strengths.append("Project experience")
    if alignment_score >= 0.80:
        strengths.append("Career goal alignment")
    if not strengths:
        strengths.append("Clear career intent")

    return {
        "placement_readiness_score": max(0, min(readiness_score, 100)),
        "strengths": strengths,
        "missing_skills": missing_skills,
    }


def decision_agent(
    student_profile: dict,
    academic_output: dict,
    career_output: dict,
) -> dict:
    score = career_output["placement_readiness_score"]
    projected_score = min(score + 15, 95)
    missing_skills = career_output["missing_skills"]
    immediate_skill = missing_skills[0] if missing_skills else "portfolio refinement"

    return {
        "placement_readiness": score,
        "strengths": career_output["strengths"],
        "missing_skills": missing_skills,
        "recommended_project": academic_output["recommended_project"],
        "certification": academic_output["recommended_certification"],
        "learning_roadmap": academic_output["learning_roadmap"],
        "recommended_platforms": academic_output["recommended_platforms"],
        "current_position": f"{student_profile['year']} {student_profile['branch']} student",
        "career_goal": student_profile["career_goal"],
        "confidence_level": _confidence_label(score),
        "immediate_next_action": f"Start with {immediate_skill} this week.",
        "why_this_recommendation": (
            "The recommendation prioritizes missing role skills, project proof, "
            "and placement actions that can improve readiness within 30 days."
        ),
        "estimated_readiness_after_roadmap": projected_score,
    }


def generate_gemini_decision_summary(
    student_profile: dict,
    decision_output: dict,
) -> str:
    api_key = os.getenv("GEMINI_API_KEY")
    fallback = (
        "Your profile has a clear direction. Focus first on the highest priority "
        "missing skills, then build the recommended project as portfolio proof. "
        "Complete the certification alongside the roadmap, polish your resume, "
        "and start applying through the recommended platforms. Consistent weekly "
        "progress should improve your placement readiness."
    )

    if not api_key:
        return fallback

    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "text": (
                            "Generate a concise AI decision card in maximum 200 words. "
                            "Include personalized explanation, why these recommendations "
                            "were selected, career guidance, and motivation. Use only "
                            "the data below.\n\n"
                            f"Career Goal: {student_profile['career_goal']}\n"
                            f"Current Skills: {', '.join(student_profile['skills']) or 'None provided'}\n"
                            f"Missing Skills: {', '.join(decision_output['missing_skills']) or 'None'}\n"
                            f"Placement Readiness: {decision_output['placement_readiness']}%\n"
                            f"Recommended Project: {decision_output['recommended_project']}\n"
                            f"Certification: {decision_output['certification']}\n"
                            f"Roadmap: {decision_output['learning_roadmap']}"
                        )
                    }
                ]
            }
        ],
        "generationConfig": {
            "maxOutputTokens": 260,
            "temperature": 0.5,
        },
    }

    request = urllib.request.Request(
        "https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent"
        f"?key={api_key}",
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=12) as response:
            result = json.loads(response.read().decode("utf-8"))
        text = result["candidates"][0]["content"]["parts"][0]["text"].strip()
        words = text.split()
        return " ".join(words[:200])
    except (KeyError, IndexError, TimeoutError, urllib.error.URLError, json.JSONDecodeError):
        return fallback
