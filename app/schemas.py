from typing import Any, Optional

from pydantic import BaseModel, Field, field_validator


class JobResponse(BaseModel):
    job_id: int
    title: str
    company: str
    location: str
    salary: Optional[str] = None
    salary_lpa: Optional[float] = None
    description: str
    application_status: str
    application_date: Optional[str] = None
    application_notes: str = ""
    extracted_skills: list[str] = Field(default_factory=list)
    source: str = "local_json"
    source_url: Optional[str] = None
    collected_at: Optional[str] = None
    last_seen_at: Optional[str] = None
    is_active: bool = True


class CandidateProfileResponse(BaseModel):
    candidate_id: int
    name: str
    education: Optional[str] = None
    experience_years: float


class CandidateSkillResponse(BaseModel):
    skill: str
    proficiency: Optional[str] = None


class MatchResponse(BaseModel):
    candidate_id: int
    job_id: int
    title: str
    company: str
    required_fit: float
    preferred_fit: float
    preferred_bonus: float
    overall_match: float
    match_category: str
    matched_required: list[str]
    missing_required: list[str]
    matched_preferred: list[str]
    missing_preferred: list[str]


class RecommendationResponse(BaseModel):
    job_id: int
    title: str
    company: str
    overall_match: float
    match_category: str
    recommendation: str
    explanation: list[str]
    missing_required: list[str]
    missing_preferred: list[str]


class SkillGapResponse(BaseModel):
    skill: str
    required_count: int
    preferred_count: int
    opportunity_count: int
    job_ids: list[int]
    job_titles: list[str]


class SkillPriorityResponse(BaseModel):
    skill: str
    required_count: int
    preferred_count: int
    opportunity_count: int
    market_coverage: float
    priority_score: float
    priority_category: str
    job_ids: list[int]
    job_titles: list[str]


class MarketSkillDemandResponse(BaseModel):
    skill: str
    job_count: int
    required_count: int
    preferred_count: int
    demand_percentage: float


class ApplicationStatisticsResponse(BaseModel):
    not_applied: int
    applied: int
    interview: int
    rejected: int
    offer: int


class CandidateReadinessResponse(BaseModel):
    readiness_score: float
    readiness_level: str
    skill_strength: float
    job_fit: float
    market_alignment: float
    strongest_skills: list[dict[str, Any]] = Field(
        default_factory=list
    )
    market_relevant_skills: list[dict[str, Any]] = Field(
        default_factory=list
    )
    major_blockers: list[dict[str, Any]] = Field(
        default_factory=list
    )
    semantic_opportunity_count: int


class CandidateIntelligenceResponse(BaseModel):
    profile: CandidateProfileResponse

    candidate_skills: list[CandidateSkillResponse]

    job_matches: list[dict[str, Any]]

    saved_matches: list[MatchResponse]

    recommendations: list[RecommendationResponse]

    skill_gaps: list[SkillGapResponse]

    skill_priorities: list[SkillPriorityResponse]

    market_skill_demand: list[MarketSkillDemandResponse]

    candidate_readiness: CandidateReadinessResponse

    candidate_segmentation: dict[str, Any] = Field(
        default_factory=dict
    )

    candidate_strength_gap: dict[str, Any] = Field(
        default_factory=dict
    )

    career_readiness_explanation: dict[str, Any] = Field(
        default_factory=dict
    )

    interview_intelligence: Optional[dict[str, Any]] = None

    career_dashboard: dict[str, Any] = Field(
        default_factory=dict
    )

    copilot_context: dict[str, Any] = Field(
        default_factory=dict
    )

    career_advice: dict[str, Any] = Field(
        default_factory=dict
    )

    career_action_plan: list[dict[str, Any]] = Field(
        default_factory=list
    )

    career_strategy: dict[str, Any] = Field(
        default_factory=dict
    )

    skill_priority_explanations: list[dict[str, Any]] = Field(
        default_factory=list
    )

    job_match_explanations: list[dict[str, Any]] = Field(
        default_factory=list
    )

    llm_copilot: dict[str, Any] = Field(
        default_factory=dict
    )


class ApplicationStatusRequest(BaseModel):
    status: str = Field(
        ...,
        min_length=1,
        description="Application status"
    )

    @field_validator("status")
    @classmethod
    def validate_status(cls, value: str) -> str:
        valid_statuses = {
            "Not Applied",
            "Applied",
            "Interview",
            "Rejected",
            "Offer"
        }

        normalized_value = value.strip().title()

        if normalized_value not in valid_statuses:
            raise ValueError(
                "Status must be one of: "
                "Not Applied, Applied, Interview, "
                "Rejected, Offer"
            )

        return normalized_value


class ApplicationNotesRequest(BaseModel):
    notes: str = Field(
        default="",
        max_length=2000,
        description="Notes about the job application"
    )
