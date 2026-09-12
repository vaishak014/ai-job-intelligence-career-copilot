from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.schemas import (
    JobResponse,
    CandidateProfileResponse,
    CandidateSkillResponse,
    MatchResponse,
    RecommendationResponse,
    SkillGapResponse,
    SkillPriorityResponse,
    MarketSkillDemandResponse,
    ApplicationStatisticsResponse,
    CandidateIntelligenceResponse,
    ApplicationStatusRequest,
    ApplicationNotesRequest
)

from app.database_jobs import (
    get_all_jobs,
    search_jobs
)

from app.services import (
    get_job_by_id,
    get_candidate_by_id,
    get_candidate_skill_data,
    get_candidate_match_data,
    get_candidate_intelligence_data,
    get_candidate_recommendation_data,
    get_candidate_skill_gap_data,
    get_market_skill_data,
    get_application_statistics_data,
    change_application_status,
    change_application_notes
)


app = FastAPI(
    title="AI Job Intelligence & Career Copilot",
    description=(
        "API for job search, candidate matching, "
        "career recommendations and skill intelligence."
    ),
    version="1.0.0"
)


# Dashboard assets are served locally with the API.
STATIC_DIRECTORY = Path(__file__).parent / "static"

app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIRECTORY),
    name="static"
)


@app.get("/", include_in_schema=False)
def get_dashboard():
    return FileResponse(STATIC_DIRECTORY / "index.html")


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "AI Job Intelligence & Career Copilot"
    }


@app.get(
    "/jobs",
    response_model=list[JobResponse]
)
def get_jobs():
    return get_all_jobs()


@app.get(
    "/jobs/search",
    response_model=list[JobResponse]
)
def search_job_listings(
    title: str | None = None,
    location: str | None = None,
    minimum_salary: float | None = None
):
    return search_jobs(
        title_keyword=title,
        location=location,
        minimum_salary=minimum_salary
    )


@app.get(
    "/jobs/{job_id}",
    response_model=JobResponse
)
def get_job(job_id: int):

    job = get_job_by_id(job_id)

    if job is None:
        raise HTTPException(
            status_code=404,
            detail="Job not found."
        )

    return job


@app.get(
    "/candidates/{candidate_id}",
    response_model=CandidateProfileResponse
)
def get_candidate(candidate_id: int):

    profile = get_candidate_by_id(
        candidate_id
    )

    if profile is None:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found."
        )

    return profile


@app.get(
    "/candidates/{candidate_id}/skills",
    response_model=list[CandidateSkillResponse]
)
def get_candidate_skill_list(
    candidate_id: int
):

    skills = get_candidate_skill_data(
        candidate_id
    )

    if skills is None:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found."
        )

    return skills


@app.get(
    "/candidates/{candidate_id}/matches",
    response_model=list[MatchResponse]
)
def get_candidate_matches(
    candidate_id: int
):

    matches = get_candidate_match_data(
        candidate_id
    )

    if matches is None:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found."
        )

    return matches


@app.get(
    "/candidates/{candidate_id}/intelligence",
    response_model=CandidateIntelligenceResponse
)
def get_candidate_intelligence(
    candidate_id: int
):

    intelligence = get_candidate_intelligence_data(
        candidate_id
    )

    if intelligence is None:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found."
        )

    return intelligence


@app.get(
    "/candidates/{candidate_id}/recommendations",
    response_model=list[RecommendationResponse]
)
def get_candidate_recommendations(
    candidate_id: int
):

    recommendations = get_candidate_recommendation_data(
        candidate_id
    )

    if recommendations is None:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found."
        )

    return recommendations


@app.get(
    "/candidates/{candidate_id}/skill-gaps"
)
def get_candidate_skill_gaps(
    candidate_id: int
):

    skill_gap_data = get_candidate_skill_gap_data(
        candidate_id
    )

    if skill_gap_data is None:
        raise HTTPException(
            status_code=404,
            detail="Candidate not found."
        )

    return skill_gap_data


@app.get(
    "/market/skills",
    response_model=list[MarketSkillDemandResponse]
)
def get_market_skills():

    return get_market_skill_data()


@app.get(
    "/applications/statistics",
    response_model=ApplicationStatisticsResponse
)
def get_application_stats():

    return get_application_statistics_data()


@app.put(
    "/jobs/{job_id}/application-status"
)
def update_job_application_status(
    job_id: int,
    request: ApplicationStatusRequest
):

    updated = change_application_status(
        job_id,
        request.status
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Job not found."
        )

    return {
        "success": True,
        "job_id": job_id,
        "application_status": request.status
    }


@app.put(
    "/jobs/{job_id}/application-notes"
)
def update_job_application_notes(
    job_id: int,
    request: ApplicationNotesRequest
):

    updated = change_application_notes(
        job_id,
        request.notes
    )

    if not updated:
        raise HTTPException(
            status_code=404,
            detail="Job not found."
        )

    return {
        "success": True,
        "job_id": job_id,
        "application_notes": request.notes
    }
