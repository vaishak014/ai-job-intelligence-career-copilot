import ast

from app.llm_provider import LLMProvider
from app.llm_config import get_llm_config


class MockLLMProvider(LLMProvider):
    """
    Development provider that generates a deterministic
    career response from the supplied Copilot prompt.
    """

    def generate(
        self,
        system_prompt,
        candidate_prompt
    ):
        return generate_mock_response(
            candidate_prompt
        )


class LLMClient:
    """
    Unified interface for interacting with LLM providers.
    """

    def __init__(
        self,
        provider="mock",
        model="local-development"
    ):
        self.provider = provider
        self.model = model
        self.provider_instance = self._create_provider()

    def _create_provider(self):
        if self.provider == "mock":
            return MockLLMProvider()

        return None

    def generate(
        self,
        system_prompt,
        candidate_prompt
    ):
        if not system_prompt:
            raise ValueError(
                "System prompt cannot be empty."
            )

        if not candidate_prompt:
            raise ValueError(
                "Candidate prompt cannot be empty."
            )

        if self.provider_instance is None:
            return {
                "provider": self.provider,
                "model": self.model,
                "system_prompt": system_prompt,
                "candidate_prompt": candidate_prompt,
                "response": None,
                "status": "not_configured"
            }

        response = self.provider_instance.generate(
            system_prompt,
            candidate_prompt
        )

        return {
            "provider": self.provider,
            "model": self.model,
            "system_prompt": system_prompt,
            "candidate_prompt": candidate_prompt,
            "response": response,
            "status": "success"
        }


def extract_context_value(
    candidate_prompt,
    label,
    default="Unknown"
):
    """
    Extract a simple value from the structured
    Copilot candidate prompt.
    """

    if not candidate_prompt:
        return default

    prefix = f"{label}:"

    for line in candidate_prompt.splitlines():
        stripped_line = line.strip()

        if stripped_line.startswith(prefix):
            value = stripped_line[len(prefix):].strip()

            if value:
                return value

    return default


def extract_section(
    candidate_prompt,
    section_name
):
    """
    Extract a named section from the structured
    Copilot prompt.

    Sections end when another known section header
    is reached.
    """

    if not candidate_prompt:
        return []

    lines = candidate_prompt.splitlines()

    section_headers = {
        "CANDIDATE",
        "CURRENT SKILLS",
        "READINESS",
        "CANDIDATE SEGMENT",
        "STRENGTHS",
        "MARKET STRENGTHS",
        "CRITICAL SKILL GAPS",
        "COMPETITIVE ADVANTAGES",
        "CAREER STRATEGY",
        "CAREER ACTION PLAN",
        "SKILL PRIORITIES",
        "TOP JOB MATCHES",
        "MARKET SKILL DEMAND",
        "CAREER READINESS EXPLANATION"
    }

    target = section_name.strip().upper()
    start_index = None

    for index, line in enumerate(lines):
        if line.strip().upper() == target:
            start_index = index + 1
            break

    if start_index is None:
        return []

    results = []

    for line in lines[start_index:]:
        stripped_line = line.strip()

        if (
            stripped_line.upper() in section_headers
            and stripped_line.upper() != target
        ):
            break

        if stripped_line:
            results.append(stripped_line)

    return results


def parse_structured_value(value):
    """
    Convert a string representation of a Python list/dictionary
    into its actual Python object.

    Returns None if parsing is not possible.
    """

    if not value:
        return None

    value = value.strip()

    if not value.startswith(("[", "{")):
        return None

    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return None


def extract_structured_items(section_lines):
    """
    Convert section lines containing Python-style lists/dictionaries
    into a list of structured objects.

    Example:

    [
        "{'skill': 'Python', 'proficiency': 'Intermediate'}"
    ]

    becomes:

    [
        {
            "skill": "Python",
            "proficiency": "Intermediate"
        }
    ]
    """

    if not section_lines:
        return []

    combined = " ".join(section_lines).strip()

    parsed = parse_structured_value(combined)

    if isinstance(parsed, list):
        return parsed

    if isinstance(parsed, dict):
        return [parsed]

    return []


def extract_legacy_skills(candidate_prompt):
    """
    Preserve compatibility with simple prompts such as:

    'Candidate has Python and SQL skills.'
    """

    if not candidate_prompt:
        return []

    skills = []

    known_skills = [
        "Python",
        "SQL",
        "Pandas",
        "FastAPI",
        "Git",
        "REST APIs",
        "Kotlin",
        "Java",
        "JavaScript",
        "React",
        "HTML",
        "CSS",
        "AWS",
        "MongoDB",
        "Node.js",
        "PySpark",
        "Machine Learning",
        "Android",
        "Firebase",
        "Flutter",
        "Dart",
        "Angular"
    ]

    prompt_lower = candidate_prompt.lower()

    for skill in known_skills:
        if skill.lower() in prompt_lower:
            skills.append(skill)

    return skills


def format_strengths(
    strengths,
    legacy_skills
):
    """
    Convert strength information into readable bullets.
    """

    structured_items = extract_structured_items(
        strengths
    )

    if structured_items:
        formatted = []

        for item in structured_items[:5]:
            if isinstance(item, dict):
                skill = item.get(
                    "skill",
                    "Unknown skill"
                )

                proficiency = item.get(
                    "proficiency",
                    "Unknown"
                )

                strength_score = item.get(
                    "strength_score"
                )

                if strength_score is not None:
                    formatted.append(
                        f"- {skill}: "
                        f"{proficiency} "
                        f"({strength_score}%)"
                    )
                else:
                    formatted.append(
                        f"- {skill}: "
                        f"{proficiency}"
                    )

        if formatted:
            return formatted

    formatted = []

    for item in strengths[:5]:
        if item.startswith("["):
            continue

        formatted.append(
            f"- {item}"
        )

    if formatted:
        return formatted

    if legacy_skills:
        return [
            f"- {skill}"
            for skill in legacy_skills[:5]
        ]

    return [
        "- No strength information was supplied."
    ]


def format_skill_gaps(
    critical_gaps
):
    """
    Convert skill-gap information into readable bullets.
    """

    structured_items = extract_structured_items(
        critical_gaps
    )

    if structured_items:
        formatted = []

        for item in structured_items[:5]:
            if isinstance(item, dict):
                skill = item.get(
                    "skill",
                    "Unknown skill"
                )

                priority = item.get(
                    "priority_category",
                    "Unknown priority"
                )

                formatted.append(
                    f"- {skill}: {priority}"
                )

        if formatted:
            return formatted

    formatted = []

    for item in critical_gaps[:5]:
        if item.startswith("["):
            continue

        formatted.append(
            f"- {item}"
        )

    if formatted:
        return formatted

    return [
        "- No critical skill gaps were supplied."
    ]


def format_job_matches(
    top_job_matches
):
    """
    Convert job-match information into readable bullets.
    """

    structured_items = extract_structured_items(
        top_job_matches
    )

    if structured_items:
        formatted = []

        for item in structured_items[:5]:
            if isinstance(item, dict):
                title = item.get(
                    "title",
                    "Unknown role"
                )

                company = item.get(
                    "company",
                    "Unknown company"
                )

                skill_match = item.get(
                    "skill_match_score"
                )

                semantic_similarity = item.get(
                    "semantic_similarity"
                )

                combined_match = item.get(
                    "combined_match"
                )

                opportunity_type = item.get(
                    "opportunity_type",
                    "Unknown"
                )

                formatted.append(
                    f"- {title} at {company}"
                )

                if skill_match is not None:
                    formatted.append(
                        f"  Skill Match: {skill_match}%"
                    )

                if semantic_similarity is not None:
                    formatted.append(
                        f"  Semantic Similarity: "
                        f"{semantic_similarity}%"
                    )

                if combined_match is not None:
                    formatted.append(
                        f"  Combined Match: "
                        f"{combined_match}%"
                    )

                formatted.append(
                    f"  Opportunity Type: "
                    f"{opportunity_type}"
                )

        if formatted:
            return formatted

    formatted = []

    for item in top_job_matches[:5]:
        if item.startswith("["):
            continue

        formatted.append(
            f"- {item}"
        )

    if formatted:
        return formatted

    return [
        "- No job-match information was supplied."
    ]


def generate_mock_response(
    candidate_prompt
):
    """
    Generate a deterministic, human-readable response
    using information from the Copilot candidate context.
    """

    if not candidate_prompt:
        return ""

    readiness_score = extract_context_value(
        candidate_prompt,
        "Score",
        "0.0%"
    )

    readiness_level = extract_context_value(
        candidate_prompt,
        "Level",
        "Unknown"
    )

    skill_strength = extract_context_value(
        candidate_prompt,
        "Skill Strength",
        "0.0%"
    )

    job_fit = extract_context_value(
        candidate_prompt,
        "Job Fit",
        "0.0%"
    )

    market_alignment = extract_context_value(
        candidate_prompt,
        "Market Alignment",
        "0.0%"
    )

    semantic_opportunities = extract_context_value(
        candidate_prompt,
        "Semantic Opportunities",
        "0"
    )

    strengths = extract_section(
        candidate_prompt,
        "STRENGTHS"
    )

    critical_gaps = extract_section(
        candidate_prompt,
        "CRITICAL SKILL GAPS"
    )

    top_job_matches = extract_section(
        candidate_prompt,
        "TOP JOB MATCHES"
    )

    career_strategy = extract_context_value(
        candidate_prompt,
        "Strategy Direction",
        "Continue improving alignment with relevant opportunities."
    )

    is_structured_prompt = (
        "CANDIDATE CAREER INTELLIGENCE"
        in candidate_prompt
    )

    if is_structured_prompt:
        legacy_skills = []
    else:
        legacy_skills = extract_legacy_skills(
            candidate_prompt
        )

    formatted_strengths = format_strengths(
        strengths,
        legacy_skills
    )

    formatted_gaps = format_skill_gaps(
        critical_gaps
    )

    formatted_jobs = format_job_matches(
        top_job_matches
    )

    response_lines = [
        "Career Copilot Development Response",
        "",
        "CURRENT CAREER POSITION",
        (
            f"The candidate has a readiness score of "
            f"{readiness_score} and is currently classified "
            f"as {readiness_level}."
        ),
        (
            f"Skill strength is {skill_strength}, job fit is "
            f"{job_fit}, and market alignment is "
            f"{market_alignment}."
        ),
        "",
        "STRONGEST SKILLS"
    ]

    response_lines.extend(
        formatted_strengths
    )

    response_lines.extend([
        "",
        "IMPORTANT SKILL GAPS"
    ])

    response_lines.extend(
        formatted_gaps
    )

    response_lines.extend([
        "",
        "JOB OPPORTUNITIES"
    ])

    response_lines.extend(
        formatted_jobs
    )

    response_lines.extend([
        "",
        "CAREER DIRECTION",
        career_strategy,
        "",
        "SEMANTIC OPPORTUNITIES",
        (
            f"The supplied intelligence identifies "
            f"{semantic_opportunities} semantic opportunities. "
            "These should be evaluated alongside direct skill fit."
        ),
        "",
        "NEXT STEP",
        (
            "Prioritize the highest-impact skill gaps while "
            "continuing to target opportunities that align "
            "with the candidate's strongest existing skills."
        ),
        "",
        (
            "This is a development-mode response generated "
            "without an external LLM API."
        )
    ])

    return "\n".join(response_lines)


def create_llm_client(
    provider=None,
    model=None
):
    config = get_llm_config()

    if provider is None:
        provider = config["provider"]

    if model is None:
        model = config["model"]

    return LLMClient(
        provider=provider,
        model=model
    )
