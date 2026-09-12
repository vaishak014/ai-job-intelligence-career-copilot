from datetime import datetime


def build_ingestion_report(
    source_type,
    raw_count,
    valid_count,
    results,
    deactivated
):
    invalid_count = raw_count - valid_count

    successful_records = (
        results["inserted"]
        + results["updated"]
    )

    if raw_count > 0:
        success_rate = (
            successful_records / raw_count
        ) * 100
    else:
        success_rate = 0.0

    return {
        "source_type": source_type,
        "run_at": datetime.now().isoformat(),
        "raw_jobs": raw_count,
        "valid_jobs": valid_count,
        "invalid_jobs": invalid_count,
        "inserted": results["inserted"],
        "updated": results["updated"],
        "skipped": results["skipped"],
        "deactivated": deactivated,
        "failed": results["failed"],
        "success_rate": round(success_rate, 2)
    }
