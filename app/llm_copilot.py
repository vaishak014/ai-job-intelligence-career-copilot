def build_system_prompt():
    return """
You are an AI Career Copilot.

Your role is to help a candidate understand their
career position and make practical decisions based
on the career intelligence provided to you.

Important rules:

1. Use only the information provided in the candidate
   intelligence context.

2. Do not invent candidate skills, experience,
   qualifications, jobs, companies, salaries, or
   market statistics.

3. Do not change or recalculate the supplied scores.

4. Clearly distinguish between:
   - observed facts from the candidate data
   - reasonable career recommendations

5. Prioritize practical and achievable actions.

6. When discussing skill gaps, prioritize the gaps
   according to their supplied priority and market
   relevance.

7. When discussing jobs, use the supplied job matches
   and explain why they may or may not be suitable.

8. For semantic opportunities, explain that semantic
   relevance does not necessarily mean the candidate
   satisfies the required skills.

9. The candidate may be a fresher, so recommendations
   should be realistic for an early-career candidate.

10. Do not claim that the candidate is guaranteed to
    get a job.

11. Do not provide fabricated interview questions,
    company information, or job requirements unless
    they are explicitly present in the supplied context.

12. Give clear, concise, actionable career guidance.
""".strip()


def build_candidate_context_prompt(copilot_context):
    if copilot_context is None:
        return ""

    candidate = copilot_context.get(
        "candidate",
        {}
    )

    current_skills = copilot_context.get(
        "current_skills",
        []
    )

    readiness = copilot_context.get(
        "readiness",
        {}
    )

    candidate_segment = copilot_context.get(
        "candidate_segment",
        {}
    )

    strengths = copilot_context.get(
        "strengths",
        []
    )

    market_strengths = copilot_context.get(
        "market_strengths",
        []
    )

    critical_gaps = copilot_context.get(
        "critical_gaps",
        []
    )

    competitive_advantages = copilot_context.get(
        "competitive_advantages",
        []
    )

    career_strategy = copilot_context.get(
        "career_strategy",
        {}
    )

    career_action_plan = copilot_context.get(
        "career_action_plan",
        []
    )

    skill_priorities = copilot_context.get(
        "skill_priorities",
        []
    )

    top_job_matches = copilot_context.get(
        "top_job_matches",
        []
    )

    market_skill_demand = copilot_context.get(
        "market_skill_demand",
        []
    )

    readiness_explanation = copilot_context.get(
        "readiness_explanation",
        {}
    )

    prompt = f"""
CANDIDATE CAREER INTELLIGENCE

CANDIDATE
Name: {candidate.get("name", "Unknown")}
Education: {candidate.get("education", "Unknown")}
Experience: {candidate.get("experience_years", 0.0)} years

CURRENT SKILLS
{current_skills}

READINESS
Score: {readiness.get("score", 0.0)}%
Level: {readiness.get("level", "Unknown")}
Skill Strength: {readiness.get("skill_strength", 0.0)}%
Job Fit: {readiness.get("job_fit", 0.0)}%
Market Alignment: {readiness.get("market_alignment", 0.0)}%
Semantic Opportunities: {
    readiness.get("semantic_opportunities", 0)
}

CANDIDATE SEGMENT
Type: {candidate_segment.get("type", "Unknown")}
Reason: {candidate_segment.get("reason", "")}

STRENGTHS
{strengths}

MARKET STRENGTHS
{market_strengths}

CRITICAL SKILL GAPS
{critical_gaps}

COMPETITIVE ADVANTAGES
{competitive_advantages}

CAREER STRATEGY
Strongest Skill: {
    career_strategy.get("strongest_skill", None)
}

Best Job Match: {
    career_strategy.get("best_job_match", None)
}

Top Improvements: {
    career_strategy.get("top_improvements", [])
}

Strategy Direction: {
    career_strategy.get("strategy_direction", "")
}

CAREER ACTION PLAN
{career_action_plan}

SKILL PRIORITIES
{skill_priorities}

TOP JOB MATCHES
{top_job_matches}

MARKET SKILL DEMAND
{market_skill_demand}

CAREER READINESS EXPLANATION
{readiness_explanation}

Based only on the information above, provide
career guidance for this candidate.

Cover these areas:

1. Current career position
2. Strongest skills
3. Most important skill gaps
4. Best current job opportunities
5. What the candidate should learn next
6. How the candidate should approach the job search
7. A practical short-term action plan

Do not invent information that is not present
in the supplied career intelligence.
""".strip()

    return prompt


def build_copilot_prompt(copilot_context):
    if copilot_context is None:
        return None

    return {
        "system_prompt": build_system_prompt(),
        "candidate_prompt": build_candidate_context_prompt(
            copilot_context
        )
    }
