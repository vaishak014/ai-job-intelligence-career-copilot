from app.database import get_connection
from app.database_jobs import (
    get_job_source_metadata
)
from app.job_skill_manager import (
    get_job_skills,
    sync_job_extracted_skills
)
from app.skill_extractor import (
    extract_skills,
    get_skill_category
)


def test_hopin_metadata_contains_technical_criteria():
    metadata = get_job_source_metadata(
        7,
        "hopin"
    )

    assert metadata

    criteria = metadata[0]["criteria"]

    assert "Proficiency in Python programming" in criteria
    assert "Experience with Pyspark" in criteria
    assert "Knowledge of SQL" in criteria


def test_skill_extraction_from_hopin_criteria():
    criteria = [
        "Proficiency in Python programming",
        "Experience with Pyspark",
        "Knowledge of SQL",
        "Strong problem-solving skills",
        "Ability to work in a team",
        "Good communication skills"
    ]

    text = "\n".join(criteria)

    skills = extract_skills(text)

    assert skills == [
        "Python",
        "SQL",
        "PySpark"
    ]


def test_soft_requirements_are_not_extracted_as_technical_skills():
    text = """
    Strong communication skills.
    Good communication skills.
    Strong problem-solving skills.
    Ability to work in a team.
    """

    skills = extract_skills(text)

    assert skills == []


def test_skill_categories_are_from_taxonomy():
    skills = [
        "Python",
        "SQL",
        "PySpark"
    ]

    categories = {
        skill: get_skill_category(skill)
        for skill in skills
    }

    assert categories["Python"] == "Programming"
    assert categories["SQL"] == "Data"
    assert categories["PySpark"] == "Data"


def test_job_7_has_relational_skills():
    skills = get_job_skills(7)

    skill_names = [
        skill["skill"]
        for skill in skills
    ]

    assert "Python" in skill_names
    assert "SQL" in skill_names
    assert "PySpark" in skill_names


def test_job_7_skill_categories_are_persisted():
    skills = get_job_skills(7)

    skills_by_name = {
        skill["skill"]: skill
        for skill in skills
    }

    assert skills_by_name["Python"]["category"] == "Programming"
    assert skills_by_name["PySpark"]["category"] == "Data"

    # Existing database category is intentionally preserved.
    assert skills_by_name["SQL"]["category"] == "Database"


def test_job_7_skills_are_required():
    skills = get_job_skills(7)

    for skill in skills:
        assert skill["importance"] == "Required"


def test_skill_sync_is_idempotent():
    skills = [
        "Python",
        "SQL",
        "PySpark"
    ]

    categories = {
        skill: get_skill_category(skill)
        for skill in skills
    }

    before = get_job_skills(7)

    sync_job_extracted_skills(
        7,
        skills,
        categories
    )

    middle = get_job_skills(7)

    sync_job_extracted_skills(
        7,
        skills,
        categories
    )

    after = get_job_skills(7)

    assert len(middle) == len(before)
    assert len(after) == len(before)

    before_names = {
        skill["skill"]
        for skill in before
    }

    after_names = {
        skill["skill"]
        for skill in after
    }

    assert before_names == after_names


def test_skill_sync_does_not_create_duplicate_relationships():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    job_id,
                    skill_id,
                    COUNT(*)
                FROM job_skills
                WHERE job_id = 7
                GROUP BY
                    job_id,
                    skill_id
                HAVING COUNT(*) > 1
                """
            )

            duplicates = cursor.fetchall()

        assert duplicates == []

    finally:
        connection.close()
