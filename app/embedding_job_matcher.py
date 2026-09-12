from app.semantic_matcher import (
    build_candidate_text,
    build_job_text
)
from app.embedding_matcher import (
    generate_embedding
)


def generate_candidate_embedding(
    candidate_profile,
    candidate_skills,
    model
):
    candidate_text = build_candidate_text(
        candidate_profile,
        candidate_skills
    )

    return generate_embedding(
        candidate_text,
        model
    )


def generate_job_embedding(
    job,
    model
):
    job_text = build_job_text(job)

    return generate_embedding(
        job_text,
        model
    )


def generate_job_embeddings(
    jobs,
    model
):
    embeddings = {}

    for job in jobs:
        embeddings[job["job_id"]] = (
            generate_job_embedding(
                job,
                model
            )
        )

    return embeddings
