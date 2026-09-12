from candidate import get_candidate_skills

from database_jobs import get_all_jobs

from job_skill_manager import get_all_job_skills

from skill_gap_analyzer import analyze_skill_gaps

from skill_priority_engine import (
    generate_skill_priorities
)


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


priorities = generate_skill_priorities(
    skill_gaps,
    len(jobs)
)


print("Personalized Skill Priorities")
print("=============================")


for rank, priority in enumerate(
    priorities,
    start=1
):

    print()

    print(
        f"{rank}. {priority['skill']}"
    )

    print(
        "Required In:",
        priority["required_count"],
        "job(s)"
    )

    print(
        "Preferred In:",
        priority["preferred_count"],
        "job(s)"
    )

    print(
        "Opportunity Count:",
        priority["opportunity_count"]
    )

    print(
        "Market Coverage:",
        priority["market_coverage"],
        "%"
    )

    print(
        "Priority Score:",
        priority["priority_score"]
    )

    print(
        "Priority:",
        priority["priority_category"]
    )

    print(
        "Jobs:",
        priority["job_titles"]
    )
