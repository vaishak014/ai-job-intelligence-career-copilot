from app.embedding_matcher import (
    calculate_embedding_similarity,
    generate_embedding,
    load_embedding_model
)
from app.embedding_job_matcher import (
    generate_candidate_embedding,
    generate_job_embeddings
)


SEMANTIC_WEIGHT = 0.30
SKILL_MATCH_WEIGHT = 0.70


def calculate_combined_match(
    skill_match_score,
    semantic_similarity
):
    combined_score = (
        skill_match_score * SKILL_MATCH_WEIGHT
        + semantic_similarity * SEMANTIC_WEIGHT
    )

    return round(
        min(combined_score, 100.0),
        2
    )


def build_embedding_matches(
    candidate_profile,
    candidate_skills,
    job_matches,
    jobs,
    model=None
):
    if model is None:
        model = load_embedding_model()

    candidate_embedding = generate_candidate_embedding(
        candidate_profile,
        candidate_skills,
        model
    )

    job_embeddings = generate_job_embeddings(
        jobs,
        model
    )

    combined_matches = []

    for job_match in job_matches:
        job_id = job_match["job_id"]

        job_embedding = job_embeddings.get(
            job_id
        )

        semantic_similarity = (
            calculate_embedding_similarity(
                candidate_embedding,
                job_embedding
            )
        )

        combined_score = calculate_combined_match(
            job_match["overall_match"],
            semantic_similarity
        )

        combined_match = dict(job_match)

        combined_match["skill_match_score"] = (
            job_match["overall_match"]
        )

        combined_match["semantic_similarity"] = (
            semantic_similarity
        )

        combined_match["combined_match"] = (
            combined_score
        )

        combined_matches.append(
            combined_match
        )

    combined_matches.sort(
        key=lambda item: item["combined_match"],
        reverse=True
    )

    return combined_matches
