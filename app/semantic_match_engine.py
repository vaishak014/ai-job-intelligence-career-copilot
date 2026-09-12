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


def classify_semantic_signal(
    skill_match,
    semantic_similarity
):
    difference = (
        semantic_similarity
        - skill_match
    )

    if difference >= 20:
        return "Semantic Advantage"

    if difference <= -20:
        return "Skill Advantage"

    return "Balanced"


def classify_opportunity_type(
    skill_match,
    semantic_similarity
):
    if (
        skill_match >= 50
        and semantic_similarity >= 40
    ):
        return "Strong Match"

    if (
        skill_match < 30
        and semantic_similarity >= 35
    ):
        return "Semantic Opportunity"

    if (
        skill_match >= 40
        and semantic_similarity < 35
    ):
        return "Skill Match"

    return "Low Relevance"


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

        skill_match_score = (
            job_match["overall_match"]
        )

        combined_score = calculate_combined_match(
            skill_match_score,
            semantic_similarity
        )

        semantic_signal = classify_semantic_signal(
            skill_match_score,
            semantic_similarity
        )

        opportunity_type = classify_opportunity_type(
            skill_match_score,
            semantic_similarity
        )

        combined_match = dict(job_match)

        combined_match["skill_match_score"] = (
            skill_match_score
        )

        combined_match["semantic_similarity"] = (
            semantic_similarity
        )

        combined_match["combined_match"] = (
            combined_score
        )

        combined_match["semantic_signal"] = (
            semantic_signal
        )

        combined_match["opportunity_type"] = (
            opportunity_type
        )

        combined_matches.append(
            combined_match
        )

    combined_matches.sort(
        key=lambda item: item["combined_match"],
        reverse=True
    )

    return combined_matches
