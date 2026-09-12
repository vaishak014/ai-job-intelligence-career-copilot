from app.job_loader import process_jobs_with_quality_report
from app.database_jobs import (
    insert_jobs,
    mark_missing_jobs_inactive
)
from app.sources.factory import create_job_source
from app.ingestion_metrics import build_ingestion_report
from app.quality_metrics import build_quality_report


SOURCE_TYPE = "json"
RAW_DATA_PATH = "data/jobs.json"


def ingest_jobs(source, source_type=SOURCE_TYPE):
    print("Starting job ingestion...")

    raw_jobs = source.fetch_jobs()

    print("Raw jobs loaded:", len(raw_jobs))

    processed_jobs, rejected_jobs = (
        process_jobs_with_quality_report(
            raw_jobs
        )
    )

    print(
        "Valid jobs processed:",
        len(processed_jobs)
    )

    print(
        "Invalid jobs rejected:",
        len(rejected_jobs)
    )

    results = insert_jobs(
        processed_jobs
    )

    deactivated = mark_missing_jobs_inactive(
        processed_jobs,
        source=source_type
    )

    ingestion_report = build_ingestion_report(
        source_type,
        len(raw_jobs),
        len(processed_jobs),
        results,
        deactivated
    )

    quality_report = build_quality_report(
        raw_jobs,
        processed_jobs,
        rejected_jobs
    )

    print(
        "New jobs inserted:",
        results["inserted"]
    )

    print(
        "Existing jobs updated:",
        results["updated"]
    )

    print(
        "Existing jobs skipped:",
        results["skipped"]
    )

    print(
        "Jobs marked inactive:",
        deactivated
    )

    print(
        "Failed jobs:",
        results["failed"]
    )

    print(
        "Ingestion success rate:",
        ingestion_report["success_rate"],
        "%"
    )

    print(
        "Data quality rate:",
        quality_report["quality_rate"],
        "%"
    )

    results["deactivated"] = deactivated
    results["report"] = ingestion_report
    results["quality_report"] = quality_report
    results["rejected_jobs"] = rejected_jobs

    return results


def create_ingestion_source():
    if SOURCE_TYPE == "json":
        return create_job_source(
            "json",
            file_path=RAW_DATA_PATH
        )

    if SOURCE_TYPE == "hopin":
        return create_job_source(
            "hopin",
            industry="Technology",
            is_unofficial=True
        )

    raise ValueError(
        f"Unsupported ingestion source: {SOURCE_TYPE}"
    )


if __name__ == "__main__":
    source = create_ingestion_source()

    ingest_jobs(
        source,
        SOURCE_TYPE
    )
