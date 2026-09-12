import json
import re
import hashlib
from datetime import date

from app.job_quality import validate_job_quality


def load_jobs(file_path):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            jobs = json.load(file)

        return jobs

    except FileNotFoundError:
        print("Error: Job data file not found.")
        return []

    except json.JSONDecodeError:
        print("Error: Invalid JSON format.")
        return []


def validate_job(job):
    required_fields = [
        "title",
        "company",
        "location",
        "description"
    ]

    for field in required_fields:
        if field not in job or not job[field]:
            return False

    return True


def normalize_text(text):
    if text is None:
        return ""

    text = str(text).strip().lower()
    text = re.sub(r"\s+", " ", text)

    return text


def clean_job(job):
    cleaned_job = job.copy()

    cleaned_job["title"] = cleaned_job["title"].strip()
    cleaned_job["company"] = cleaned_job["company"].strip()
    cleaned_job["location"] = cleaned_job["location"].strip()
    cleaned_job["description"] = cleaned_job["description"].strip()

    return cleaned_job


def generate_job_fingerprint(job):
    identity_fields = [
        normalize_text(job["title"]),
        normalize_text(job["company"]),
        normalize_text(job["location"]),
        normalize_text(job["description"])
    ]

    identity_string = "|".join(identity_fields)

    return hashlib.sha256(
        identity_string.encode("utf-8")
    ).hexdigest()


def extract_salary_lpa(salary):
    if not salary:
        return None

    match = re.search(r"\d+(?:\.\d+)?", salary)

    if match:
        return float(match.group())

    return None


def process_jobs(jobs):
    processed_jobs = []

    for index, job in enumerate(jobs, start=1):
        quality_result = validate_job_quality(job)

        if not quality_result["is_valid"]:
            continue

        if validate_job(job):
            cleaned_job = clean_job(job)

            if "job_id" in cleaned_job:
                cleaned_job["job_id"] = cleaned_job["job_id"]
            else:
                cleaned_job["job_id"] = index

            cleaned_job["salary_lpa"] = extract_salary_lpa(
                cleaned_job.get("salary")
            )

            cleaned_job["job_fingerprint"] = generate_job_fingerprint(
                cleaned_job
            )

            if "application_status" not in cleaned_job:
                cleaned_job["application_status"] = "Not Applied"

            if "application_date" not in cleaned_job:
                cleaned_job["application_date"] = None

            if "application_notes" not in cleaned_job:
                cleaned_job["application_notes"] = ""

            if "extracted_skills" not in cleaned_job:
                cleaned_job["extracted_skills"] = []

            processed_jobs.append(cleaned_job)

    return processed_jobs


def process_jobs_with_quality_report(jobs):
    processed_jobs = []
    rejected_jobs = []

    for index, job in enumerate(jobs, start=1):
        quality_result = validate_job_quality(job)

        if not quality_result["is_valid"]:
            rejected_jobs.append({
                "job": job,
                "errors": quality_result["errors"]
            })
            continue

        cleaned_job = clean_job(job)

        if "job_id" in cleaned_job:
            cleaned_job["job_id"] = cleaned_job["job_id"]
        else:
            cleaned_job["job_id"] = index

        cleaned_job["salary_lpa"] = extract_salary_lpa(
            cleaned_job.get("salary")
        )

        cleaned_job["job_fingerprint"] = generate_job_fingerprint(
            cleaned_job
        )

        if "application_status" not in cleaned_job:
            cleaned_job["application_status"] = "Not Applied"

        if "application_date" not in cleaned_job:
            cleaned_job["application_date"] = None

        if "application_notes" not in cleaned_job:
            cleaned_job["application_notes"] = ""

        if "extracted_skills" not in cleaned_job:
            cleaned_job["extracted_skills"] = []

        processed_jobs.append(cleaned_job)

    return processed_jobs, rejected_jobs


def find_duplicate_jobs(jobs):
    seen_fingerprints = set()
    duplicates = []

    for job in jobs:
        fingerprint = job.get("job_fingerprint")

        if fingerprint is None:
            fingerprint = generate_job_fingerprint(job)

        if fingerprint in seen_fingerprints:
            duplicates.append(job)
        else:
            seen_fingerprints.add(fingerprint)

    return duplicates


def get_unique_jobs(jobs):
    seen_fingerprints = set()
    unique_jobs = []

    for job in jobs:
        fingerprint = job.get("job_fingerprint")

        if fingerprint is None:
            fingerprint = generate_job_fingerprint(job)

        if fingerprint not in seen_fingerprints:
            seen_fingerprints.add(fingerprint)
            unique_jobs.append(job)

    return unique_jobs


def filter_jobs_by_location(jobs, location):
    filtered_jobs = []

    for job in jobs:
        if job["location"].lower() == location.lower():
            filtered_jobs.append(job)

    return filtered_jobs


def filter_jobs_by_title(jobs, keyword):
    filtered_jobs = []

    for job in jobs:
        if keyword.lower() in job["title"].lower():
            filtered_jobs.append(job)

    return filtered_jobs


def search_jobs(jobs, title_keyword=None, location=None):
    filtered_jobs = []

    for job in jobs:
        title_matches = (
            title_keyword is None
            or title_keyword.lower() in job["title"].lower()
        )

        location_matches = (
            location is None
            or location.lower() == job["location"].lower()
        )

        if title_matches and location_matches:
            filtered_jobs.append(job)

    return filtered_jobs


def advanced_search_jobs(
    jobs,
    title_keyword=None,
    location=None,
    minimum_salary=None
):
    filtered_jobs = []

    for job in jobs:
        title_matches = (
            title_keyword is None
            or title_keyword.lower() in job["title"].lower()
        )

        location_matches = (
            location is None
            or location.lower() == job["location"].lower()
        )

        salary_matches = (
            minimum_salary is None
            or (
                job["salary_lpa"] is not None
                and job["salary_lpa"] >= minimum_salary
            )
        )

        if title_matches and location_matches and salary_matches:
            filtered_jobs.append(job)

    return filtered_jobs


def sort_jobs_by_salary(jobs, descending=True):
    return sorted(
        jobs,
        key=lambda job: job["salary_lpa"] or 0,
        reverse=descending
    )


def update_application_status(jobs, job_id, new_status):
    valid_statuses = [
        "Not Applied",
        "Applied",
        "Interview",
        "Rejected",
        "Offer"
    ]

    if new_status not in valid_statuses:
        return False

    for job in jobs:
        if job["job_id"] == job_id:
            previous_status = job["application_status"]

            job["application_status"] = new_status

            if new_status == "Applied" and previous_status != "Applied":
                job["application_date"] = date.today().isoformat()

            return True

    return False


def update_application_notes(jobs, job_id, notes):
    for job in jobs:
        if job["job_id"] == job_id:
            job["application_notes"] = notes
            return True

    return False


def save_jobs(file_path, jobs):
    try:
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(jobs, file, indent=4)

        return True

    except OSError:
        return False


def get_application_statistics(jobs):
    statistics = {
        "Not Applied": 0,
        "Applied": 0,
        "Interview": 0,
        "Rejected": 0,
        "Offer": 0
    }

    for job in jobs:
        status = job.get("application_status", "Not Applied")

        if status in statistics:
            statistics[status] += 1

    return statistics
