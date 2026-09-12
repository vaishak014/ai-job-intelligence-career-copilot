from candidate import get_candidate_skills

from database_jobs import get_all_jobs

from job_skill_manager import get_all_job_skills

from skill_gap_analyzer import analyze_skill_gaps


candidate_id = 1


candidate_skills = get_candidate_skills(
    candidate_id
)

jobs = get_all_jobs()

job_skills_map = get_all_job_skills()


skill_gaps = analyze_skill_gaps(
    candidate_skills,
    jobs,
    job_skills_map
)


print("Skill Gap Intelligence")
print("=======================")


for rank, gap in enumerate(
    skill_gaps,
    start=1
):

    print()

    print(
        f"{rank}. {gap['skill']}"
    )

    print(
        "Required In:",
        gap["required_count"],
        "job(s)"
    )

    print(
        "Preferred In:",
        gap["preferred_count"],
        "job(s)"
    )

    print(
        "Opportunity Count:",
        gap["opportunity_count"]
    )

    print(
        "Priority Score:",
        gap["priority_score"]
    )

    print(
        "Jobs:",
        gap["job_titles"]
    )
