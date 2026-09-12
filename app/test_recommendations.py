from match_database import get_saved_matches

from recommendation_engine import (
    generate_recommendations
)


candidate_id = 1


saved_matches = get_saved_matches(
    candidate_id
)


recommendations = generate_recommendations(
    saved_matches
)


print("Career Recommendations")
print("=======================")


for rank, recommendation in enumerate(
    recommendations,
    start=1
):

    print()

    print(
        f"{rank}. {recommendation['title']}"
    )

    print(
        "Company:",
        recommendation["company"]
    )

    print(
        "Overall Match:",
        recommendation["overall_match"],
        "%"
    )

    print(
        "Match Category:",
        recommendation["match_category"]
    )

    print(
        "Recommendation:",
        recommendation["recommendation"]
    )

    print("Why:")

    for explanation in recommendation[
        "explanation"
    ]:

        print(
            " ",
            explanation
        )
