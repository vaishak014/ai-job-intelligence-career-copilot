from app.candidate import (
    get_candidate_profile,
    get_candidate_skills
)

from app.database_jobs import (
    get_all_jobs,
    get_active_jobs_with_source_metadata
)

from app.job_skill_manager import (
    get_all_job_skills
)

from app.job_matcher import (
    calculate_skill_match,
    rank_jobs
)

from app.match_database import (
    save_job_match,
    get_saved_matches
)

from app.recommendation_engine import (
    generate_recommendations
)

from app.skill_gap_analyzer import (
    analyze_skill_gaps
)

from app.market_skill_analyzer import (
    analyze_skill_demand
)

from app.skill_priority_engine import (
    generate_skill_priorities
)

from app.career_explainer import (
    explain_skill_priorities,
    explain_job_matches
)

from app.career_action_planner import (
    build_career_action_plan
)

from app.career_strategy import (
    build_career_strategy
)

from app.semantic_match_engine import (
    build_embedding_matches
)

from app.candidate_readiness import (
    build_candidate_readiness_profile
)

from app.candidate_segmentation import (
    build_candidate_segmentation
)

from app.candidate_strength_gap import (
    build_candidate_strength_gap_analysis
)

from app.career_readiness_explainer import (
    build_career_readiness_explanation
)

from app.career_dashboard import (
    build_career_dashboard
)

from app.ai_career_copilot import (
    build_copilot_context
)

from app.career_advice_engine import (
    build_career_advice
)

from app.llm_copilot import (
    build_copilot_prompt
)

from app.llm_client import (
    create_llm_client
)

from app.interview_intelligence import (
    build_interview_intelligence
)


def build_candidate_intelligence(
    candidate_id,
    target_role_type=None
):
    """
    Build the complete candidate intelligence profile.

    Pipeline:

    Candidate
        ↓
    Skills
        ↓
    Job Matching
        ↓
    Semantic / Embedding Matching
        ↓
    Skill Gap Analysis
        ↓
    Market Demand
        ↓
    Skill Priorities
        ↓
    Career Strategy
        ↓
    Candidate Readiness
        ↓
    Candidate Segmentation
        ↓
    Career Dashboard
        ↓
    Career Copilot
        ↓
    Career Advice
        ↓
    Interview Intelligence
    """

    # ---------------------------------------------------------
    # 1. Load candidate
    # ---------------------------------------------------------

    profile = get_candidate_profile(
        candidate_id
    )

    if profile is None:
        return None

    candidate_skills = get_candidate_skills(
        candidate_id
    )

    # ---------------------------------------------------------
    # 2. Load target jobs
    # ---------------------------------------------------------

    if target_role_type:

        jobs = get_active_jobs_with_source_metadata(
            source="hopin",
            role_type=target_role_type
        )

    else:

        jobs = get_all_jobs()

    # ---------------------------------------------------------
    # 3. Load job skills
    # ---------------------------------------------------------

    job_skills_map = get_all_job_skills()

    # ---------------------------------------------------------
    # 4. Traditional skill matching
    # ---------------------------------------------------------

    ranked_jobs = rank_jobs(
        candidate_skills,
        jobs,
        job_skills_map
    )

    # ---------------------------------------------------------
    # 5. Semantic + embedding matching
    # ---------------------------------------------------------

    combined_job_matches = build_embedding_matches(
        profile,
        candidate_skills,
        ranked_jobs,
        jobs
    )

    # ---------------------------------------------------------
    # 6. Interview intelligence
    #
    # Use the strongest current job opportunity
    # as the default interview-preparation target.
    # ---------------------------------------------------------

    interview_intelligence = None

    if combined_job_matches:

        interview_intelligence = build_interview_intelligence(
            candidate_skills,
            combined_job_matches[0]
        )

    # ---------------------------------------------------------
    # 7. Save traditional matches
    # ---------------------------------------------------------

    for job in jobs:

        job_skills = job_skills_map.get(
            job["job_id"],
            []
        )

        match_result = calculate_skill_match(
            candidate_skills,
            job_skills
        )

        save_job_match(
            candidate_id,
            job["job_id"],
            match_result
        )

    # ---------------------------------------------------------
    # 8. Saved matches
    # ---------------------------------------------------------

    saved_matches = get_saved_matches(
        candidate_id
    )

    # ---------------------------------------------------------
    # 9. Recommendations
    # ---------------------------------------------------------

    recommendations = generate_recommendations(
        saved_matches
    )

    # ---------------------------------------------------------
    # 10. Skill gaps
    # ---------------------------------------------------------

    skill_gaps = analyze_skill_gaps(
        candidate_skills,
        jobs,
        job_skills_map
    )

    # ---------------------------------------------------------
    # 11. Market skill demand
    # ---------------------------------------------------------

    market_skill_demand = analyze_skill_demand(
        jobs,
        job_skills_map
    )

    # ---------------------------------------------------------
    # 12. Skill priorities
    # ---------------------------------------------------------

    skill_priorities = generate_skill_priorities(
        skill_gaps,
        len(jobs),
        market_skill_demand
    )

    # ---------------------------------------------------------
    # 13. Explain skill priorities
    # ---------------------------------------------------------

    skill_priority_explanations = explain_skill_priorities(
        skill_priorities,
        len(jobs)
    )

    # ---------------------------------------------------------
    # 14. Explain job matches
    # ---------------------------------------------------------

    job_match_explanations = explain_job_matches(
        combined_job_matches
    )

    # ---------------------------------------------------------
    # 15. Career action plan
    # ---------------------------------------------------------

    career_action_plan = build_career_action_plan(
        skill_priorities
    )

    # ---------------------------------------------------------
    # 16. Career strategy
    # ---------------------------------------------------------

    career_strategy = build_career_strategy(
        candidate_skills,
        combined_job_matches,
        career_action_plan,
        market_skill_demand
    )

    # ---------------------------------------------------------
    # 17. Candidate readiness
    # ---------------------------------------------------------

    candidate_readiness = build_candidate_readiness_profile(
        candidate_skills,
        combined_job_matches,
        skill_priorities,
        market_skill_demand
    )

    # ---------------------------------------------------------
    # 18. Candidate segmentation
    # ---------------------------------------------------------

    candidate_segmentation = build_candidate_segmentation(
        candidate_readiness
    )

    # ---------------------------------------------------------
    # 19. Strength and gap analysis
    # ---------------------------------------------------------

    candidate_strength_gap = (
        build_candidate_strength_gap_analysis(
            candidate_skills,
            combined_job_matches,
            skill_priorities,
            market_skill_demand
        )
    )

    # ---------------------------------------------------------
    # 20. Career readiness explanation
    # ---------------------------------------------------------

    career_readiness_explanation = (
        build_career_readiness_explanation(
            candidate_readiness,
            candidate_segmentation,
            candidate_strength_gap,
            combined_job_matches
        )
    )

    # ---------------------------------------------------------
    # 21. Build complete intelligence object
    # ---------------------------------------------------------

    intelligence = {

        "profile": profile,

        "candidate_skills": candidate_skills,

        "job_matches": combined_job_matches,

        "saved_matches": saved_matches,

        "recommendations": recommendations,

        "skill_gaps": skill_gaps,

        "skill_priorities": skill_priorities,

        "skill_priority_explanations":
            skill_priority_explanations,

        "job_match_explanations":
            job_match_explanations,

        "career_action_plan":
            career_action_plan,

        "career_strategy":
            career_strategy,

        "market_skill_demand":
            market_skill_demand,

        "candidate_readiness":
            candidate_readiness,

        "candidate_segmentation":
            candidate_segmentation,

        "candidate_strength_gap":
            candidate_strength_gap,

        "career_readiness_explanation":
            career_readiness_explanation,

        "interview_intelligence":
            interview_intelligence
    }

    # ---------------------------------------------------------
    # 22. Career dashboard
    # ---------------------------------------------------------

    intelligence["career_dashboard"] = (
        build_career_dashboard(
            intelligence
        )
    )

    # ---------------------------------------------------------
    # 23. Copilot context
    # ---------------------------------------------------------

    intelligence["copilot_context"] = (
        build_copilot_context(
            intelligence
        )
    )

    # ---------------------------------------------------------
    # 24. Deterministic career advice
    # ---------------------------------------------------------

    intelligence["career_advice"] = (
        build_career_advice(
            intelligence["copilot_context"]
        )
    )

    # ---------------------------------------------------------
    # 25. LLM prompt
    # ---------------------------------------------------------

    intelligence["llm_copilot"] = (
        build_copilot_prompt(
            intelligence["copilot_context"]
        )
    )

    return intelligence
