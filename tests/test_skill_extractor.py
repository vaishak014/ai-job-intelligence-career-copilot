from app.skill_extractor import (
    extract_skills,
    normalize_text,
    get_skill_category,
    SKILL_TAXONOMY
)


def test_normalize_text():

    text = "  Python 3   PROGRAMMING!!! "

    result = normalize_text(text)

    assert result == "python 3 programming"


def test_python_variants():

    assert "Python" in extract_skills(
        "Python 3 programming"
    )

    assert "Python" in extract_skills(
        "python3 development"
    )

    assert "Python" in extract_skills(
        "Python programming"
    )


def test_database_variants():

    skills = extract_skills(
        "SQL and PostgreSQL database development"
    )

    assert "SQL" in skills
    assert "PostgreSQL" in skills


def test_framework_variants():

    skills = extract_skills(
        "Fast API and ReactJS development"
    )

    assert "FastAPI" in skills
    assert "React" in skills


def test_machine_learning_variants():

    skills = extract_skills(
        "Machine learning using sklearn"
    )

    assert "Machine Learning" in skills
    assert "scikit-learn" in skills


def test_devops_variants():

    skills = extract_skills(
        "Docker containers and Git version control"
    )

    assert "Docker" in skills
    assert "Git" in skills


def test_javascript_variants():

    skills = extract_skills(
        "JavaScript and JS development"
    )

    assert "JavaScript" in skills


def test_react_variants():

    skills = extract_skills(
        "React, ReactJS and React.js"
    )

    assert "React" in skills


def test_empty_text():

    assert extract_skills("") == []
    assert extract_skills(None) == []


def test_taxonomy_contains_core_skills():

    expected_skills = {
        "Python",
        "SQL",
        "Pandas",
        "FastAPI",
        "scikit-learn",
        "Machine Learning",
        "PostgreSQL",
        "JavaScript",
        "React",
        "Docker",
        "Git"
    }

    assert expected_skills.issubset(
        set(SKILL_TAXONOMY.keys())
    )


def test_pyspark():

    skills = extract_skills(
        "Experience with Pyspark and SQL"
    )

    assert "PySpark" in skills
    assert "SQL" in skills


def test_power_bi():

    skills = extract_skills(
        "Experience with Power BI dashboards"
    )

    assert "Power BI" in skills


def test_cloud_and_backend():

    skills = extract_skills(
        "Experience with AWS and RESTful APIs"
    )

    assert "AWS" in skills
    assert "REST APIs" in skills


def test_frontend_stack():

    skills = extract_skills(
        "HTML, CSS, JavaScript, React and Next.js"
    )

    assert "HTML" in skills
    assert "CSS" in skills
    assert "JavaScript" in skills
    assert "React" in skills
    assert "Next.js" in skills


def test_mobile_stack():

    skills = extract_skills(
        "Flutter development using Dart and Firebase"
    )

    assert "Flutter" in skills
    assert "Dart" in skills
    assert "Firebase" in skills


def test_ai_stack():

    skills = extract_skills(
        "Generative AI, LLMs and NLP"
    )

    assert "Generative AI" in skills
    assert "Large Language Models" in skills
    assert "Natural Language Processing" in skills


def test_skill_categories():

    assert get_skill_category(
        "Python"
    ) == "Programming"

    assert get_skill_category(
        "PostgreSQL"
    ) == "Data"

    assert get_skill_category(
        "FastAPI"
    ) == "Backend"

    assert get_skill_category(
        "React"
    ) == "Frontend"

    assert get_skill_category(
        "AWS"
    ) == "Cloud / DevOps"


def test_unknown_skill_category():

    assert get_skill_category(
        "Unknown Skill"
    ) is None


def test_no_false_positive_short_aliases():

    skills = extract_skills(
        "This is a normal example."
    )

    assert "Machine Learning" not in skills
    assert "JavaScript" not in skills
