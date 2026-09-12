from app.embedding_matcher import (
    calculate_embedding_similarity
)


def calculate_embedding_job_matches(
    candidate_embedding,
    jobs,
    job_embeddings
):
    results = []

    for job in jobs:
        job_id = job["job_id"]

        job_embedding = job_embeddings.get(
            job_id
        )

        similarity = calculate_embedding_similarity(
            candidate_embedding,
            job_embedding
        )

        results.append({
            "job_id": job_id,
            "title": job["title"],
            "company": job["company"],
            "embedding_similarity": similarity
        })

    results.sort(
        key=lambda item: item["embedding_similarity"],
        reverse=True
    )

    return results
