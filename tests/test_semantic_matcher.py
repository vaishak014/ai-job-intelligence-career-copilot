from app.semantic_matcher import (
    build_candidate_text,
    build_job_text,
    calculate_semantic_similarity,
    calculate_semantic_matches
)


def test_build_candidate_text():
    profile = {
        "education": "Computer Science",
        "experience_years": 0.0
    }

    skills = [
        {
            "skill": "Python",
            "proficiency": "Intermediate"
        },
        {
            "skill": "SQL",
            "proficiency": "Intermediate"
        }
    ]

    result = build_candidate_text(
        profile,
        skills
    )

    assert "Python" in result
    assert "SQL" in result
    assert "Computer Science" in result
    assert "0.0" in result


def test_build_job_text():
    job = {
        "title": "Python Developer",
        "company": "Cognizant",
        "description": "Backend development using Python",
        "source_criteria": [
            "Proficiency in Python programming",
            "Knowledge of SQL"
        ]
    }

    result = build_job_text(job)

    assert "Python Developer" in result
    assert "Cognizant" in result
    assert "Backend development using Python" in result
    assert "Knowledge of SQL" in result


def test_semantic_similarity_identical_text():
    text = "Python SQL backend development"

    result = calculate_semantic_similarity(
        text,
        text
    )

    assert result == 100.0


def test_semantic_similarity_empty_text():
    result = calculate_semantic_similarity(
        "",
        "Python developer"
    )

    assert result == 0.0


def test_semantic_matches_are_ranked():
    profile = {
        "education": "Computer Science",
        "experience_years": 0.0
    }

    skills = [
        {
            "skill": "Python",
            "proficiency": "Intermediate"
        },
        {
            "skill": "SQL",
            "proficiency": "Intermediate"
        }
    ]

    jobs = [
        {
            "job_id": 1,
            "title": "Python Developer",
            "company": "Company A",
            "description": "Python SQL backend development",
            "source_criteria": [
                "Python programming",
                "SQL"
            ]
        },
        {
            "job_id": 2,
            "title": "Graphic Designer",
            "company": "Company B",
            "description": "Graphic design and illustration",
            "source_criteria": [
                "Photoshop",
                "Illustration"
            ]
        }
    ]

    results = calculate_semantic_matches(
        profile,
        skills,
        jobs
    )

    assert len(results) == 2
    assert results[0]["job_id"] == 1
    assert (
        results[0]["semantic_similarity"]
        >= results[1]["semantic_similarity"]
    )
