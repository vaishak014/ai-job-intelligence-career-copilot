from app.database_jobs import (
    get_all_jobs,
    get_job_source_metadata,
    update_job_skills
)

from app.skill_extractor import (
    extract_skills,
    get_skill_category
)

from app.job_skill_manager import (
    sync_job_extracted_skills
)


def build_job_skill_text(job):
    """
    Combine the job description with source criteria
    before skill extraction.
    """

    text_parts = []

    description = job.get(
        "description",
        ""
    )

    if description:
        text_parts.append(
            description
        )

    metadata = get_job_source_metadata(
        job["job_id"]
    )

    for source in metadata:
        criteria = source.get(
            "criteria",
            []
        )

        if isinstance(criteria, list):
            for criterion in criteria:
                if criterion:
                    text_parts.append(
                        str(criterion)
                    )

    return "\n".join(
        text_parts
    )


def build_skill_categories(skills):
    """
    Build a canonical skill-to-category mapping
    using the centralized skill taxonomy.
    """

    categories = {}

    for skill in skills:
        categories[skill] = get_skill_category(
            skill
        )

    return categories


def extract_and_store_skills():
    jobs = get_all_jobs()

    print(
        "Jobs loaded:",
        len(jobs)
    )

    total_updated = 0
    total_relationally_synced = 0

    for job in jobs:

        skill_text = build_job_skill_text(
            job
        )

        skills = extract_skills(
            skill_text
        )

        updated = update_job_skills(
            job["job_id"],
            skills
        )

        if updated:
            total_updated += 1

        categories = build_skill_categories(
            skills
        )

        relational_sync = (
            sync_job_extracted_skills(
                job["job_id"],
                skills,
                categories
            )
        )

        if relational_sync:
            total_relationally_synced += 1

        print()
        print(
            "Job ID:",
            job["job_id"]
        )

        print(
            "Title:",
            job["title"]
        )

        print(
            "Extracted Skills:",
            skills
        )

        print(
            "Skill Categories:",
            categories
        )

    print()

    print(
        "Jobs updated with skills:",
        total_updated
    )

    print(
        "Jobs synced to relational skill tables:",
        total_relationally_synced
    )


if __name__ == "__main__":
    extract_and_store_skills()
