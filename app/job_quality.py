def validate_job_quality(job):
    errors = []

    title = job.get("title")
    company = job.get("company")
    location = job.get("location")
    description = job.get("description")

    if not isinstance(title, str) or not title.strip():
        errors.append("missing_title")

    if not isinstance(company, str) or not company.strip():
        errors.append("missing_company")

    if not isinstance(location, str) or not location.strip():
        errors.append("missing_location")

    if not isinstance(description, str) or not description.strip():
        errors.append("missing_description")

    return {
        "is_valid": len(errors) == 0,
        "errors": errors
    }


def calculate_quality_score(job):
    result = validate_job_quality(job)

    total_fields = 4
    valid_fields = total_fields - len(result["errors"])

    return round(
        (valid_fields / total_fields) * 100,
        2
    )


def filter_quality_jobs(jobs):
    valid_jobs = []
    rejected_jobs = []

    for job in jobs:
        result = validate_job_quality(job)

        if result["is_valid"]:
            valid_jobs.append(job)
        else:
            rejected_jobs.append({
                "job": job,
                "errors": result["errors"]
            })

    return valid_jobs, rejected_jobs
