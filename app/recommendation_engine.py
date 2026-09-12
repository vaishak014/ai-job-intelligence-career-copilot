def get_recommendation(match):
    overall_match = match["overall_match"]
    missing_required = match["missing_required"]

    if missing_required:
        recommendation = "Skill Gap"

    elif overall_match >= 90:
        recommendation = "High Priority"

    elif overall_match >= 75:
        recommendation = "Recommended"

    elif overall_match >= 60:
        recommendation = "Consider"

    else:
        recommendation = "Low Priority"

    return recommendation


def generate_explanation(match):
    explanation = []

    for skill in match["matched_required"]:
        explanation.append(
            f"✓ {skill} - Required skill matched"
        )

    for skill in match["missing_required"]:
        explanation.append(
            f"✗ {skill} - Required skill missing"
        )

    for skill in match["matched_preferred"]:
        explanation.append(
            f"✓ {skill} - Preferred skill matched"
        )

    for skill in match["missing_preferred"]:
        explanation.append(
            f"⚠ {skill} - Preferred skill missing"
        )

    return explanation


def generate_recommendation(match):
    recommendation = get_recommendation(match)

    explanation = generate_explanation(match)

    return {
        "job_id": match["job_id"],
        "title": match["title"],
        "company": match["company"],
        "overall_match": match["overall_match"],
        "match_category": match["match_category"],
        "recommendation": recommendation,
        "explanation": explanation,
        "missing_required": match["missing_required"],
        "missing_preferred": match["missing_preferred"]
    }


def generate_recommendations(saved_matches):
    recommendations = []

    for match in saved_matches:

        recommendation = generate_recommendation(
            match
        )

        recommendations.append(
            recommendation
        )

    return recommendations
