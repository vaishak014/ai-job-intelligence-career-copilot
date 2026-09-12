def normalize_location(location):
    if not location:
        return ""

    location = str(location).strip()

    # Normalize Bengaluru/Bangalore naming
    location = location.replace("Bengaluru", "Bangalore")

    return location


def normalize_salary(job):
    salary = job.get("salary")

    if salary:
        return str(salary).strip()

    ctc_amount = job.get("ctc_amount")

    if ctc_amount:
        return str(ctc_amount).strip()

    ctc = job.get("ctc")

    if ctc:
        return str(ctc).strip()

    return None


def normalize_description(job):
    description = job.get("description")

    if description:
        return str(description).strip()

    parts = []

    if job.get("your_impact"):
        parts.append(
            str(job["your_impact"]).strip()
        )

    if job.get("company_description"):
        parts.append(
            str(job["company_description"]).strip()
        )

    if job.get("preferred_qualifications"):
        qualifications = job["preferred_qualifications"]

        if isinstance(qualifications, list):
            parts.extend(
                str(item).strip()
                for item in qualifications
                if item
            )

    return "\n\n".join(parts)


def normalize_hopin_job(job):
    """
    Convert a raw Hopin job record into the
    internal job schema used by the project.
    """

    normalized_job = {
        # Internal database ID must remain None.
        # PostgreSQL will generate it.
        "job_id": None,

        "title": str(
            job.get("title_clean")
            or job.get("clean_title")
            or job.get("title")
            or ""
        ).strip(),

        "company": str(
            job.get("company")
            or ""
        ).strip(),

        "location": normalize_location(
            job.get("location")
        ),

        "description": normalize_description(
            job
        ),

        "salary": normalize_salary(
            job
        ),

        "source": "hopin",

        "source_url": (
            job.get("apply_url")
            or job.get("apply_form_url")
        ),

        "application_status": "Not Applied",
        "application_date": None,
        "application_notes": "",
        "extracted_skills": [],

        # Preserve the external source identity
        # without using it as our internal job_id.
        "source_job_id": job.get("id"),

        # Useful provenance metadata
        "source_is_unofficial": job.get(
            "is_unofficial",
            False
        ),

        "source_posted_at": job.get(
            "posted_at"
        ),

        "source_posted_days": job.get(
            "posted_days"
        ),

        "source_industry": job.get(
            "industry"
        ),

        "source_role_type": job.get(
            "role_type"
        ),

        "source_work_type": job.get(
            "work_type"
        ),

        "source_criteria": job.get(
            "criteria",
            []
        )
    }

    return normalized_job


def normalize_hopin_jobs(jobs):
    """
    Normalize multiple raw Hopin job records.
    """

    normalized_jobs = []

    for job in jobs:
        normalized_jobs.append(
            normalize_hopin_job(job)
        )

    return normalized_jobs
