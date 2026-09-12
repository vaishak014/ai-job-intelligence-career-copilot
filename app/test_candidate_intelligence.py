from app.candidate import (
    get_candidate_profile,
    get_connection
)

from app.candidate_intelligence import (
    build_candidate_intelligence
)


def print_section(title):
    print()
    print("=" * 70)
    print(title)
    print("=" * 70)


def get_first_candidate_id():
    """
    Find the first candidate from the project's
    existing candidate_profiles table.
    """

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            cursor.execute(
                """
                SELECT candidate_id
                FROM candidate_profiles
                ORDER BY candidate_id
                LIMIT 1
                """
            )

            row = cursor.fetchone()

        if row is None:
            return None

        return row[0]

    finally:
        connection.close()


def main():

    # ---------------------------------------------------------
    # 1. Find an existing candidate automatically
    # ---------------------------------------------------------

    candidate_id = get_first_candidate_id()

    if candidate_id is None:

        print()
        print(
            "No candidate profiles were found "
            "in the database."
        )

        print()
        print(
            "The candidate intelligence pipeline needs "
            "at least one candidate profile."
        )

        return

    print()
    print(
        f"Using Candidate ID: {candidate_id}"
    )

    # ---------------------------------------------------------
    # 2. Build candidate intelligence
    # ---------------------------------------------------------

    intelligence = build_candidate_intelligence(
        candidate_id,
        target_role_type="Software Engineering"
    )

    if intelligence is None:

        print(
            "Candidate could not be loaded."
        )

        return

    profile = intelligence[
        "profile"
    ]

    readiness = intelligence[
        "candidate_readiness"
    ]

    segmentation = intelligence[
        "candidate_segmentation"
    ]

    strength_gap = intelligence[
        "candidate_strength_gap"
    ]

    strategy = intelligence[
        "career_strategy"
    ]

    dashboard = intelligence[
        "career_dashboard"
    ]

    career_advice = intelligence[
        "career_advice"
    ]

    copilot_response = intelligence[
        "copilot_response"
    ]

    interview_intelligence = intelligence.get(
        "interview_intelligence"
    )

    # ---------------------------------------------------------
    # 3. Candidate information
    # ---------------------------------------------------------

    print_section(
        "CANDIDATE INTELLIGENCE"
    )

    print(
        f"Candidate: "
        f"{profile.get('name', 'Unknown')}"
    )

    print(
        f"Education: "
        f"{profile.get('education', 'Unknown')}"
    )

    print(
        f"Experience: "
        f"{profile.get('experience_years', 0.0)} years"
    )

    # ---------------------------------------------------------
    # 4. Readiness
    # ---------------------------------------------------------

    print_section(
        "READINESS"
    )

    print(
        f"Readiness Score: "
        f"{readiness.get('readiness_score', 0.0)}%"
    )

    print(
        f"Readiness Level: "
        f"{readiness.get('readiness_level', 'Unknown')}"
    )

    print(
        f"Skill Strength: "
        f"{readiness.get('skill_strength', 0.0)}%"
    )

    print(
        f"Job Fit: "
        f"{readiness.get('job_fit', 0.0)}%"
    )

    print(
        f"Market Alignment: "
        f"{readiness.get('market_alignment', 0.0)}%"
    )

    print(
        f"Semantic Opportunities: "
        f"{readiness.get('semantic_opportunity_count', 0)}"
    )

    # ---------------------------------------------------------
    # 5. Candidate segmentation
    # ---------------------------------------------------------

    print_section(
        "CANDIDATE SEGMENT"
    )

    segment_type = segmentation.get(
        "type"
    )

    if not segment_type:

        segment_type = segmentation.get(
            "segment_type",
            "Unknown"
        )

    print(
        f"Type: "
        f"{segment_type}"
    )

    print(
        f"Reason: "
        f"{segmentation.get('reason', '')}"
    )

    # ---------------------------------------------------------
    # 6. Strongest skills
    # ---------------------------------------------------------

    print_section(
        "STRONGEST SKILLS"
    )

    strongest_skills = readiness.get(
        "strongest_skills",
        []
    )

    if not strongest_skills:

        print("None")

    else:

        for skill in strongest_skills:

            print(
                f"- {skill.get('skill', 'Unknown')}: "
                f"{skill.get('proficiency', 'Unknown')} "
                f"({skill.get('strength_score', 0.0)}%)"
            )

    # ---------------------------------------------------------
    # 7. Critical skill gaps
    # ---------------------------------------------------------

    print_section(
        "CRITICAL SKILL GAPS"
    )

    critical_gaps = strength_gap.get(
        "critical_gaps",
        strength_gap.get(
            "major_gaps",
            []
        )
    )

    if not critical_gaps:

        print("None")

    else:

        for gap in critical_gaps:

            if isinstance(
                gap,
                dict
            ):

                print(
                    f"- {gap.get('skill', 'Unknown')}: "
                    f"{gap.get('priority', gap.get('priority_category', 'Unknown'))}"
                )

            else:

                print(
                    f"- {gap}"
                )

    # ---------------------------------------------------------
    # 8. Top job matches
    # ---------------------------------------------------------

    print_section(
        "TOP JOB MATCHES"
    )

    top_job_matches = dashboard.get(
        "top_job_matches",
        intelligence.get(
            "job_matches",
            []
        )
    )

    if not top_job_matches:

        print("None")

    else:

        for job in top_job_matches[:5]:

            print(
                f"- {job.get('title', 'Unknown')} "
                f"at {job.get('company', 'Unknown')}"
            )

            print(
                f"  Skill Match: "
                f"{job.get('skill_match_score', job.get('overall_match', 0.0))}%"
            )

            print(
                f"  Semantic Similarity: "
                f"{job.get('semantic_similarity', 0.0)}%"
            )

            print(
                f"  Combined Match: "
                f"{job.get('combined_match', 0.0)}%"
            )

            print(
                f"  Opportunity Type: "
                f"{job.get('opportunity_type', 'Unknown')}"
            )

    # ---------------------------------------------------------
    # 9. Career strategy
    # ---------------------------------------------------------

    print_section(
        "CAREER STRATEGY"
    )

    print(
        f"Strongest Skill: "
        f"{strategy.get('strongest_skill', None)}"
    )

    print(
        f"Best Job Match: "
        f"{strategy.get('best_job_match', None)}"
    )

    print(
        f"Strategy Direction: "
        f"{strategy.get('strategy_direction', '')}"
    )

    print(
        f"Top Improvements: "
        f"{strategy.get('top_improvements', [])}"
    )

    # ---------------------------------------------------------
    # 10. Career dashboard
    # ---------------------------------------------------------

    print_section(
        "CAREER DASHBOARD"
    )

    if isinstance(
        dashboard,
        dict
    ):

        for key, value in dashboard.items():

            if key not in {
                "top_job_matches"
            }:

                print(
                    f"{key}: {value}"
                )

    # ---------------------------------------------------------
    # 11. AI Career Advice
    # ---------------------------------------------------------

    print_section(
        "AI CAREER ADVICE"
    )

    if isinstance(
        career_advice,
        dict
    ):

        for key, value in career_advice.items():

            print()

            print(
                key.upper()
            )

            print(
                "-" * len(key)
            )

            if isinstance(
                value,
                list
            ):

                for item in value:

                    print(
                        f"- {item}"
                    )

            else:

                print(
                    value
                )

    else:

        print(
            career_advice
        )

    # ---------------------------------------------------------
    # 12. AI Career Copilot
    # ---------------------------------------------------------

    print_section(
        "AI CAREER COPILOT RESPONSE"
    )

    print(
        copilot_response.get(
            "response",
            ""
        )
    )

    print()

    print(
        f"Provider: "
        f"{copilot_response.get('provider', 'Unknown')}"
    )

    print(
        f"Model: "
        f"{copilot_response.get('model', 'Unknown')}"
    )

    print(
        f"Status: "
        f"{copilot_response.get('status', 'Unknown')}"
    )

    # ---------------------------------------------------------
    # 13. Interview Intelligence
    # ---------------------------------------------------------

    print_section(
        "INTERVIEW INTELLIGENCE"
    )

    if interview_intelligence is None:

        print(
            "No interview intelligence available."
        )

    else:

        print(
            f"Target Job: "
            f"{interview_intelligence.get('job_title', 'Unknown')}"
        )

        print(
            f"Company: "
            f"{interview_intelligence.get('company', 'Unknown')}"
        )

        print(
            f"Interview Readiness: "
            f"{interview_intelligence.get('interview_readiness', 'Unknown')}"
        )

        print(
            f"Combined Match: "
            f"{interview_intelligence.get('combined_match', 0.0)}%"
        )

        # -----------------------------------------------------
        # Required skills
        # -----------------------------------------------------

        print()

        print(
            "REQUIRED SKILLS"
        )

        print(
            "-" * 16
        )

        required_skills = interview_intelligence.get(
            "required_skills",
            []
        )

        if required_skills:

            for skill in required_skills:

                print(
                    f"- {skill}"
                )

        else:

            print("None")

        # -----------------------------------------------------
        # Missing required skills
        # -----------------------------------------------------

        print()

        print(
            "MISSING REQUIRED SKILLS"
        )

        print(
            "-" * 24
        )

        missing_required = interview_intelligence.get(
            "missing_required",
            []
        )

        if missing_required:

            for skill in missing_required:

                print(
                    f"- {skill}"
                )

        else:

            print("None")

        # -----------------------------------------------------
        # Interview focus
        # -----------------------------------------------------

        print()

        print(
            "INTERVIEW FOCUS"
        )

        print(
            "-" * 15
        )

        interview_focus = interview_intelligence.get(
            "interview_focus",
            []
        )

        if interview_focus:

            for item in interview_focus:

                print(
                    f"- {item.get('skill', 'Unknown')} "
                    f"[{item.get('priority', 'Unknown')}]"
                )

                print(
                    f"  {item.get('reason', '')}"
                )

        else:

            print("None")

        # -----------------------------------------------------
        # Technical topics
        # -----------------------------------------------------

        print()

        print(
            "TECHNICAL TOPICS"
        )

        print(
            "-" * 16
        )

        technical_topics = interview_intelligence.get(
            "technical_topics",
            []
        )

        if technical_topics:

            for topic in technical_topics:

                print(
                    f"- {topic.get('skill', 'Unknown')}"
                )

                print(
                    f"  {topic.get('focus', '')}"
                )

        else:

            print("None")

        # -----------------------------------------------------
        # Project defense topics
        # -----------------------------------------------------

        print()

        print(
            "PROJECT DEFENSE TOPICS"
        )

        print(
            "-" * 23
        )

        project_defense_topics = interview_intelligence.get(
            "project_defense_topics",
            []
        )

        if project_defense_topics:

            for topic in project_defense_topics:

                print(
                    f"- {topic.get('topic', 'Unknown')}"
                )

                print(
                    f"  {topic.get('focus', '')}"
                )

        else:

            print("None")


if __name__ == "__main__":
    main()
