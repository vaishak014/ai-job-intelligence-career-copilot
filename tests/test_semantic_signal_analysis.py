def classify_semantic_signal(
    skill_match,
    semantic_similarity
):
    difference = semantic_similarity - skill_match

    if difference >= 20:
        return "Semantic Advantage"

    if difference <= -20:
        return "Skill Advantage"

    return "Balanced"


def test_semantic_advantage():
    result = classify_semantic_signal(
        skill_match=25.0,
        semantic_similarity=60.0
    )

    assert result == "Semantic Advantage"


def test_skill_advantage():
    result = classify_semantic_signal(
        skill_match=80.0,
        semantic_similarity=50.0
    )

    assert result == "Skill Advantage"


def test_balanced_signal():
    result = classify_semantic_signal(
        skill_match=60.0,
        semantic_similarity=65.0
    )

    assert result == "Balanced"
