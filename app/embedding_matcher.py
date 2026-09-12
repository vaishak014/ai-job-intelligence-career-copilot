from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity


MODEL_NAME = "all-MiniLM-L6-v2"


def load_embedding_model():
    return SentenceTransformer(MODEL_NAME)


def generate_embedding(
    text,
    model
):
    if not text or not text.strip():
        return None

    return model.encode(
        text,
        convert_to_numpy=True
    )


def calculate_embedding_similarity(
    candidate_embedding,
    job_embedding
):
    if candidate_embedding is None:
        return 0.0

    if job_embedding is None:
        return 0.0

    similarity = cosine_similarity(
        candidate_embedding.reshape(1, -1),
        job_embedding.reshape(1, -1)
    )[0][0]

    similarity = max(
        0.0,
        float(similarity)
    )

    return round(
        similarity * 100,
        2
    )
