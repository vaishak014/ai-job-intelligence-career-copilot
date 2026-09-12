def build_career_dashboard(
    intelligence
):
    if intelligence is None:
        return None

    profile = intelligence.get(
        "profile",
        {}
    )

    readiness = intelligence.get(
        "candidate_readiness",
        {}
    )

    segmentation = intelligence.get(
        "candidate_segmentation",
        {}
    )

    strength_gap = intelligence.get(
        "candidate_strength_gap",
        {}
    )

    readiness_explanation = intelligence.get(
        "career_readiness_explanation",
        {}
    )

    job_matches = intelligence.get(
        "job_matches",
        []
    )

    skill_priorities = intelligence.get(
        "skill_priorities",
        []
    )

    career_action_plan = intelligence.get(
        "career_action_plan",
        []
    )

    career_strategy = intelligence.get(
        "career_strategy",
        {}
    )

    market_skill_demand = intelligence.get(
        "market_skill_demand",
        []
    )

    return {
        "candidate": {
            "name": profile.get(
                "name",
                "Unknown"
            ),
            "education": profile.get(
                "education",
                ""
            ),
            "experience_years": profile.get(
                "experience_years",
                0.0
            )
        },

        "readiness": {
            "score": readiness.get(
                "readiness_score",
                0.0
            ),
            "level": readiness.get(
                "readiness_level",
                "Unknown"
            ),
            "skill_strength": readiness.get(
                "skill_strength",
                0.0
            ),
            "job_fit": readiness.get(
                "job_fit",
                0.0
            ),
            "market_alignment": readiness.get(
                "market_alignment",
                0.0
            ),
            "semantic_opportunities": readiness.get(
                "semantic_opportunity_count",
                0
            )
        },

        "candidate_segment": {
            "type": segmentation.get(
                "profile_type",
                "Unknown"
            ),
            "reason": segmentation.get(
                "reason",
                ""
            )
        },

        "readiness_explanation": {
            "summary": readiness_explanation.get(
                "summary",
                {}
            ),
            "what_is_helping": readiness_explanation.get(
                "what_is_helping",
                []
            ),
            "what_is_holding_back": readiness_explanation.get(
                "what_is_holding_back",
                []
            ),
            "priority_actions": readiness_explanation.get(
                "priority_actions",
                []
            ),
            "realistic_opportunities": readiness_explanation.get(
                "realistic_opportunities",
                []
            ),
            "career_direction": readiness_explanation.get(
                "career_direction",
                ""
            )
        },

        "top_job_matches": job_matches[:5],

        "top_skill_priorities": skill_priorities[:5],

        "career_action_plan": career_action_plan[:5],

        "career_strategy": {
            "strongest_skill": career_strategy.get(
                "strongest_skill",
                None
            ),
            "best_job_match": career_strategy.get(
                "best_job_match",
                None
            ),
            "top_improvements": career_strategy.get(
                "top_improvements",
                []
            ),
            "strategy_direction": career_strategy.get(
                "strategy_direction",
                ""
            )
        },

        "strengths": strength_gap.get(
            "strengths",
            []
        )[:5],

        "market_strengths": strength_gap.get(
            "market_strengths",
            []
        )[:5],

        "critical_gaps": strength_gap.get(
            "critical_gaps",
            []
        )[:5],

        "competitive_advantages": strength_gap.get(
            "competitive_advantages",
            []
        )[:5],

        "market_skill_demand": market_skill_demand[:10]
    }
