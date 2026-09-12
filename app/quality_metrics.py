def build_quality_report(raw_jobs, processed_jobs, rejected_jobs):
    rejection_reasons = {}

    for rejected in rejected_jobs:
        for error in rejected["errors"]:
            rejection_reasons[error] = (
                rejection_reasons.get(error, 0) + 1
            )

    raw_count = len(raw_jobs)
    valid_count = len(processed_jobs)
    rejected_count = len(rejected_jobs)

    if raw_count > 0:
        quality_rate = (
            valid_count / raw_count
        ) * 100
    else:
        quality_rate = 0.0

    return {
        "raw_jobs": raw_count,
        "valid_jobs": valid_count,
        "rejected_jobs": rejected_count,
        "quality_rate": round(quality_rate, 2),
        "rejection_reasons": rejection_reasons
    }
