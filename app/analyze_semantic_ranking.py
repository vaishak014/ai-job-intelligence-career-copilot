from app.candidate import (
    get_candidate_profile,
    get_candidate_skills
)
from app.database_jobs import (
    get_active_jobs_with_source_metadata
)
from app.job_skill_manager import (
    get_all_job_skills
)
from app.job_matcher import (
    rank_jobs
)
from app.semantic_match_engine import (
    build_embedding_matches
)


candidate_id = 1
target_role_type = "Software Engineering"


profile = get_candidate_profile(
    candidate_id
)

candidate_skills = get_candidate_skills(
    candidate_id
)

jobs = get_active_jobs_with_source_metadata(
    source="hopin",
    role_type=target_role_type
)

job_skills_map = get_all_job_skills()

ranked_jobs = rank_jobs(
    candidate_skills,
    jobs,
    job_skills_map
)

combined_jobs = build_embedding_matches(
    profile,
    candidate_skills,
    ranked_jobs,
    jobs
)


print("SEMANTIC RANKING ANALYSIS")
print("=========================")

print()
print("Target Role:", target_role_type)
print("Jobs Retrieved:", len(jobs))


skill_ranked = sorted(
    combined_jobs,
    key=lambda item: item.get(
        "skill_match_score",
        0.0
    ),
    reverse=True
)

semantic_ranked = sorted(
    combined_jobs,
    key=lambda item: item.get(
        "semantic_similarity",
        0.0
    ),
    reverse=True
)

combined_ranked = sorted(
    combined_jobs,
    key=lambda item: item.get(
        "combined_match",
        0.0
    ),
    reverse=True
)


skill_ranks = {
    job["job_id"]: rank
    for rank, job in enumerate(
        skill_ranked,
        start=1
    )
}

semantic_ranks = {
    job["job_id"]: rank
    for rank, job in enumerate(
        semantic_ranked,
        start=1
    )
}

combined_ranks = {
    job["job_id"]: rank
    for rank, job in enumerate(
        combined_ranked,
        start=1
    )
}


print()
print("COMBINED RANKING")
print("----------------")

for rank, job in enumerate(
    combined_ranked,
    start=1
):
    job_id = job["job_id"]

    skill_rank = skill_ranks[job_id]
    semantic_rank = semantic_ranks[job_id]

    movement = (
        skill_rank
        - rank
    )

    print(
        f"{rank}. "
        f"{job['title']} | "
        f"{job['company']} | "
        f"Skill: {job['skill_match_score']}% | "
        f"Semantic: {job['semantic_similarity']}% | "
        f"Combined: {job['combined_match']}% | "
        f"Skill Rank: {skill_rank} | "
        f"Semantic Rank: {semantic_rank} | "
        f"Movement: {movement:+d} | "
        f"Signal: {job['semantic_signal']}"
    )


print()
print("SEMANTIC IMPACT")
print("---------------")

for job in combined_ranked:
    job_id = job["job_id"]

    skill_rank = skill_ranks[job_id]
    combined_rank = combined_ranks[job_id]

    movement = (
        skill_rank
        - combined_rank
    )

    if movement != 0:
        print(
            f"{job['title']} | "
            f"{job['company']} | "
            f"Skill Rank: {skill_rank} | "
            f"Combined Rank: {combined_rank} | "
            f"Movement: {movement:+d}"
        )
