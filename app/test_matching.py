from candidate import (
    get_candidate_profile,
    get_candidate_skills
)

from database_jobs import get_all_jobs

from job_skill_manager import get_all_job_skills

from job_matcher import rank_jobs


candidate_id = 1


profile = get_candidate_profile(
    candidate_id
)


candidate_skills = get_candidate_skills(
    candidate_id
)


jobs = get_all_jobs()


job_skills_map = get_all_job_skills()


ranked_jobs = rank_jobs(
    candidate_skills,
    jobs,
    job_skills_map
)


print("Candidate Profile")
print("-----------------")

print(
    "Name:",
    profile["name"]
)

print(
    "Education:",
    profile["education"]
)

print(
    "Experience:",
    profile["experience_years"],
    "years"
)


print()
print("Candidate Skills")
print("----------------")

for skill in candidate_skills:

    print(
        skill["skill"],
        "-",
        skill["proficiency"]
    )


print()
print("Ranked Job Matches")
print("------------------")


for rank, job in enumerate(
    ranked_jobs,
    start=1
):

    print()
    print(
        f"{rank}. {job['title']}"
    )

    print(
        "Company:",
        job["company"]
    )

    print(
        "Required Fit:",
        job["required_fit"],
        "%"
    )

    print(
        "Preferred Fit:",
        job["preferred_fit"],
        "%"
    )

    print(
        "Preferred Bonus:",
        job["preferred_bonus"],
        "points"
    )

    print(
        "Overall Match:",
        job["overall_match"],
        "%"
    )

    print(
        "Match Category:",
        job["match_category"]
    )

    print(
        "Matched Required:",
        job["matched_required"]
    )

    print(
        "Missing Required:",
        job["missing_required"]
    )

    print(
        "Matched Preferred:",
        job["matched_preferred"]
    )

    print(
        "Missing Preferred:",
        job["missing_preferred"]
    )

    print("Skill Details:")

    for detail in job["skill_details"]:

        print(
            " ",
            detail["skill"],
            "|",
            detail["importance"],
            "|",
            detail["status"],
            "|",
            "Proficiency:",
            detail["proficiency"],
            "|",
            "Contribution:",
            detail["contribution"]
        )
