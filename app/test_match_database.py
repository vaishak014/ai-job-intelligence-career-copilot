from candidate import get_candidate_skills

from database_jobs import get_all_jobs

from job_skill_manager import get_all_job_skills

from job_matcher import calculate_skill_match

from match_database import (
    save_job_match,
    get_saved_matches
)


candidate_id = 1


candidate_skills = get_candidate_skills(
    candidate_id
)

jobs = get_all_jobs()

job_skills_map = get_all_job_skills()


print("Saving Match Results")
print("--------------------")


for job in jobs:

    job_skills = job_skills_map.get(
        job["job_id"],
        []
    )

    match_result = calculate_skill_match(
        candidate_skills,
        job_skills
    )

    saved = save_job_match(
        candidate_id,
        job["job_id"],
        match_result
    )

    print(
        job["title"],
        "-",
        "Saved" if saved else "Failed"
    )


print()
print("Saved Job Matches")
print("-----------------")


saved_matches = get_saved_matches(
    candidate_id
)


for rank, match in enumerate(
    saved_matches,
    start=1
):

    print()

    print(
        f"{rank}. {match['title']}"
    )

    print(
        "Company:",
        match["company"]
    )

    print(
        "Required Fit:",
        match["required_fit"],
        "%"
    )

    print(
        "Preferred Fit:",
        match["preferred_fit"],
        "%"
    )

    print(
        "Overall Match:",
        match["overall_match"],
        "%"
    )

    print(
        "Category:",
        match["match_category"]
    )

    print(
        "Missing Required:",
        match["missing_required"]
    )

    print(
        "Missing Preferred:",
        match["missing_preferred"]
    )
