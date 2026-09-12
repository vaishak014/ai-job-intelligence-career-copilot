from app.semantic_match_engine import (
    calculate_combined_match
)


def test_high_semantic_low_skill_disagreement():
    skill_match = 25.0
    semantic_similarity = 60.0

    combined_match = calculate_combined_match(
        skill_match,
        semantic_similarity
    )

    assert semantic_similarity > skill_match
    assert combined_match > skill_match
    assert combined_match < semantic_similarity


def test_high_skill_low_semantic_disagreement():
    skill_match = 80.0
    semantic_similarity = 20.0

    combined_match = calculate_combined_match(
        skill_match,
        semantic_similarity
    )

    assert skill_match > semantic_similarity
    assert combined_match < skill_match
    assert combined_match > semantic_similarity


def test_balanced_semantic_and_skill_scores():
    skill_match = 60.0
    semantic_similarity = 60.0

    combined_match = calculate_combined_match(
        skill_match,
        semantic_similarity
    )

    assert combined_match == 60.0
