def build_interview_intelligence(
    candidate_skills,
    job_match
):
    """
    Build deterministic interview-preparation intelligence
    from the existing candidate skills and selected job match.

    This layer does not require an external LLM.
    """

    if job_match is None:
        return None

    candidate_skill_map = {
        skill.get("skill", "").lower(): skill
        for skill in candidate_skills
        if skill.get("skill")
    }

    skill_details = job_match.get(
        "skill_details",
        []
    )

    required_skills = []
    preferred_skills = []
    missing_required = []
    missing_preferred = []
    matched_required = []
    matched_preferred = []

    for detail in skill_details:

        skill = detail.get(
            "skill",
            "Unknown"
        )

        importance = detail.get(
            "importance",
            "Required"
        )

        status = detail.get(
            "status",
            "Missing"
        )

        if importance == "Required":
            required_skills.append(skill)

            if status == "Matched":
                matched_required.append(skill)
            else:
                missing_required.append(skill)

        else:
            preferred_skills.append(skill)

            if status == "Matched":
                matched_preferred.append(skill)
            else:
                missing_preferred.append(skill)

    interview_focus = []

    # Required skills should receive the highest priority.
    for skill in missing_required:
        interview_focus.append({
            "skill": skill,
            "priority": "High",
            "reason": (
                f"{skill} is a required job skill that "
                "the candidate currently lacks."
            ),
            "candidate_status": "Missing"
        })

    for skill in matched_required:
        candidate_skill = candidate_skill_map.get(
            skill.lower(),
            {}
        )

        interview_focus.append({
            "skill": skill,
            "priority": "High",
            "reason": (
                f"{skill} is a required skill and should "
                "be prepared for technical discussion."
            ),
            "candidate_status": candidate_skill.get(
                "proficiency",
                "Matched"
            )
        })

    for skill in missing_preferred:
        interview_focus.append({
            "skill": skill,
            "priority": "Medium",
            "reason": (
                f"{skill} is preferred for the role and "
                "could improve interview readiness."
            ),
            "candidate_status": "Missing"
        })

    for skill in matched_preferred:
        candidate_skill = candidate_skill_map.get(
            skill.lower(),
            {}
        )

        interview_focus.append({
            "skill": skill,
            "priority": "Medium",
            "reason": (
                f"{skill} is a preferred skill and can "
                "be used as supporting evidence."
            ),
            "candidate_status": candidate_skill.get(
                "proficiency",
                "Matched"
            )
        })

    technical_topics = []

    for skill in required_skills:
        technical_topics.append({
            "skill": skill,
            "question_type": "Technical",
            "focus": (
                f"Explain practical usage of {skill}, "
                "including concepts, implementation, "
                "and common problems."
            )
        })

    project_defense_topics = [
        {
            "topic": "Project Explanation",
            "focus": (
                "Be prepared to explain project objective, "
                "architecture, implementation, decisions, "
                "and limitations."
            )
        },
        {
            "topic": "Problem Solving",
            "focus": (
                "Be prepared to explain how technical "
                "problems were identified and solved."
            )
        },
        {
            "topic": "Technical Decisions",
            "focus": (
                "Be prepared to justify why particular "
                "technologies or approaches were selected."
            )
        }
    ]

    readiness_score = job_match.get(
        "combined_match",
        0.0
    )

    if readiness_score >= 70:
        interview_readiness = "High"
    elif readiness_score >= 50:
        interview_readiness = "Moderate"
    elif readiness_score >= 30:
        interview_readiness = "Developing"
    else:
        interview_readiness = "Low"

    return {
        "job_id": job_match.get(
            "job_id"
        ),
        "job_title": job_match.get(
            "title",
            "Unknown"
        ),
        "company": job_match.get(
            "company",
            "Unknown"
        ),
        "interview_readiness": interview_readiness,
        "combined_match": readiness_score,
        "required_skills": required_skills,
        "preferred_skills": preferred_skills,
        "matched_required": matched_required,
        "missing_required": missing_required,
        "matched_preferred": matched_preferred,
        "missing_preferred": missing_preferred,
        "interview_focus": interview_focus,
        "technical_topics": technical_topics,
        "project_defense_topics": project_defense_topics
    }
