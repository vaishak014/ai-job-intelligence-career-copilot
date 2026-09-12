from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def build_candidate_text(candidate_profile, candidate_skills):
    skill_parts = []

    for skill in candidate_skills:
        skill_name = skill["skill"]
        proficiency = skill.get("proficiency", "")

        skill_parts.append(
            f"{skill_name} {proficiency}"
        )

    education = candidate_profile.get(
        "education",
        ""
    )

    experience = str(
        candidate_profile.get(
            "experience_years",
            ""
        )
    )

    return " ".join(
        part
        for part in [
            "Skills",
            " ".join(skill_parts),
            "Education",
            education,
            "Experience",
            experience
        ]
        if part
    )


def build_job_text(job):
    title = job.get(
        "title",
        ""
    )

    company = job.get(
        "company",
        ""
    )

    extracted_skills = job.get(
        "extracted_skills",
        []
    )

    criteria = job.get(
        "source_criteria",
        []
    )

    description = job.get(
        "description",
        ""
    )

    skills_text = " ".join(
        extracted_skills
    )

    criteria_text = " ".join(
        criteria
    )

    return " ".join(
        part
        for part in [
            "Job Title",
            title,
            "Company",
            company,
            "Skills",
            skills_text,
            "Requirements",
            criteria_text,
            "Description",
            description
        ]
        if part
    )


def calculate_semantic_similarity(
    candidate_text,
    job_text
):
    if not candidate_text.strip():
        return 0.0

    if not job_text.strip():
        return 0.0

    vectorizer = TfidfVectorizer()

    vectors = vectorizer.fit_transform(
        [candidate_text, job_text]
    )

    similarity = cosine_similarity(
        vectors[0:1],
        vectors[1:2]
    )[0][0]

    return round(
        float(similarity * 100),
        2
    )


def calculate_semantic_matches(
    candidate_profile,
    candidate_skills,
    jobs
):
    candidate_text = build_candidate_text(
        candidate_profile,
        candidate_skills
    )

    results = []

    for job in jobs:
        job_text = build_job_text(
            job
        )

        semantic_similarity = (
            calculate_semantic_similarity(
                candidate_text,
                job_text
            )
        )

        results.append({
            "job_id": job["job_id"],
            "title": job["title"],
            "company": job["company"],
            "semantic_similarity": semantic_similarity
        })

    results.sort(
        key=lambda item: item["semantic_similarity"],
        reverse=True
    )

    return results
