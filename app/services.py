from app.candidate import (
    get_candidate_profile,
    get_candidate_skills
)

from app.database_jobs import (
    get_all_jobs,
    search_jobs,
    update_application_status,
    update_application_notes,
    get_application_statistics
)

from app.match_database import (
    get_saved_matches
)

from app.candidate_intelligence import (
    build_candidate_intelligence
)

from app.job_skill_manager import (
    get_all_job_skills
)

from app.market_skill_analyzer import (
    analyze_skill_demand
)


def get_job_by_id(job_id):
    jobs = get_all_jobs()

    for job in jobs:
        if job["job_id"] == job_id:
            return job

    return None


def get_candidate_by_id(candidate_id):
    return get_candidate_profile(candidate_id)


def get_candidate_skill_data(candidate_id):
    profile = get_candidate_profile(candidate_id)

    if profile is None:
        return None

    return get_candidate_skills(candidate_id)


def get_candidate_match_data(candidate_id):
    profile = get_candidate_profile(candidate_id)

    if profile is None:
        return None

    return get_saved_matches(candidate_id)


def get_candidate_intelligence_data(candidate_id):
    return build_candidate_intelligence(candidate_id)


def get_candidate_recommendation_data(candidate_id):
    intelligence = build_candidate_intelligence(candidate_id)

    if intelligence is None:
        return None

    return intelligence["recommendations"]


def get_candidate_skill_gap_data(candidate_id):
    intelligence = build_candidate_intelligence(candidate_id)

    if intelligence is None:
        return None

    return {
        "skill_gaps": intelligence["skill_gaps"],
        "skill_priorities": intelligence["skill_priorities"]
    }


def get_market_skill_data():
    jobs = get_all_jobs()

    job_skills_map = get_all_job_skills()

    return analyze_skill_demand(
        jobs,
        job_skills_map
    )


def get_application_statistics_data():
    statistics = get_application_statistics()

    return {
        "not_applied": statistics.get(
            "Not Applied",
            0
        ),
        "applied": statistics.get(
            "Applied",
            0
        ),
        "interview": statistics.get(
            "Interview",
            0
        ),
        "rejected": statistics.get(
            "Rejected",
            0
        ),
        "offer": statistics.get(
            "Offer",
            0
        )
    }


def change_application_status(
    job_id,
    status
):
    return update_application_status(
        job_id,
        status
    )


def change_application_notes(
    job_id,
    notes
):
    return update_application_notes(
        job_id,
        notes
    )
