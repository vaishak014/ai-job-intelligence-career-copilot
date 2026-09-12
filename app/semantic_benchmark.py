from app.candidate import (
    get_candidate_profile,
    get_candidate_skills
)
from app.database_jobs import (
    get_active_jobs_with_source_metadata
)
from app.semantic_matcher import (
    build_candidate_text,
    build_job_text,
    calculate_semantic_similarity
)
from app.embedding_matcher import (
    load_embedding_model,
    generate_embedding,
    calculate_embedding_similarity
)


def benchmark_semantic_methods(
    candidate_id,
    target_role_type=None
):
    profile = get_candidate_profile(
        candidate_id
    )

    if profile is None:
        return []

    candidate_skills = get_candidate_skills(
        candidate_id
    )

    if target_role_type:
        jobs = get_active_jobs_with_source_metadata(
            source="hopin",
            role_type=target_role_type
        )
    else:
        jobs = get_active_jobs_with_source_metadata(
            source="hopin"
        )

    candidate_text = build_candidate_text(
        profile,
        candidate_skills
    )

    model = load_embedding_model()

    candidate_embedding = generate_embedding(
        candidate_text,
        model
    )

    results = []

    for job in jobs:
        job_text = build_job_text(job)

        tfidf_similarity = calculate_semantic_similarity(
            candidate_text,
            job_text
        )

        job_embedding = generate_embedding(
            job_text,
            model
        )

        embedding_similarity = (
            calculate_embedding_similarity(
                candidate_embedding,
                job_embedding
            )
        )

        results.append({
            "job_id": job["job_id"],
            "title": job["title"],
            "company": job["company"],
            "tfidf_similarity": tfidf_similarity,
            "embedding_similarity": embedding_similarity
        })

    results.sort(
        key=lambda item: item["embedding_similarity"],
        reverse=True
    )

    return results
