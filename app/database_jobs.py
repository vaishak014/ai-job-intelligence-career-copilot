from app.database import get_connection
from psycopg.types.json import Jsonb


def insert_job(job):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT job_id
                FROM jobs
                WHERE job_fingerprint = %s
                """,
                (job["job_fingerprint"],)
            )

            existing_job = cursor.fetchone()

            if existing_job:
                existing_job_id = existing_job[0]

                cursor.execute(
                    """
                    UPDATE jobs
                    SET
                        title = %s,
                        company = %s,
                        location = %s,
                        salary = %s,
                        salary_lpa = %s,
                        description = %s,
                        source = %s,
                        source_url = %s,
                        last_seen_at = CURRENT_TIMESTAMP,
                        is_active = TRUE
                    WHERE job_id = %s
                    """,
                    (
                        job["title"],
                        job["company"],
                        job["location"],
                        job.get("salary"),
                        job.get("salary_lpa"),
                        job["description"],
                        job.get("source", "local_json"),
                        job.get("source_url"),
                        existing_job_id
                    )
                )

                connection.commit()

                save_source_metadata(
                    existing_job_id,
                    job
                )

                return "updated"

            if job.get("job_id") is not None:
                cursor.execute(
                    """
                    INSERT INTO jobs (
                        job_id,
                        title,
                        company,
                        location,
                        salary,
                        salary_lpa,
                        description,
                        application_status,
                        application_date,
                        application_notes,
                        extracted_skills,
                        source,
                        source_url,
                        collected_at,
                        last_seen_at,
                        is_active,
                        job_fingerprint
                    )
                    VALUES (
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s
                    )
                    """,
                    (
                        job["job_id"],
                        job["title"],
                        job["company"],
                        job["location"],
                        job.get("salary"),
                        job.get("salary_lpa"),
                        job["description"],
                        job.get(
                            "application_status",
                            "Not Applied"
                        ),
                        job.get("application_date"),
                        job.get(
                            "application_notes",
                            ""
                        ),
                        job.get(
                            "extracted_skills",
                            []
                        ),
                        job.get(
                            "source",
                            "local_json"
                        ),
                        job.get("source_url"),
                        job.get("collected_at"),
                        job.get("last_seen_at"),
                        job.get(
                            "is_active",
                            True
                        ),
                        job["job_fingerprint"]
                    )
                )

                metadata_job_id = job["job_id"]

            else:
                cursor.execute(
                    """
                    INSERT INTO jobs (
                        title,
                        company,
                        location,
                        salary,
                        salary_lpa,
                        description,
                        application_status,
                        application_date,
                        application_notes,
                        extracted_skills,
                        source,
                        source_url,
                        collected_at,
                        last_seen_at,
                        is_active,
                        job_fingerprint
                    )
                    VALUES (
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s,
                        %s, %s, %s, %s, %s, %s
                    )
                    """,
                    (
                        job["title"],
                        job["company"],
                        job["location"],
                        job.get("salary"),
                        job.get("salary_lpa"),
                        job["description"],
                        job.get(
                            "application_status",
                            "Not Applied"
                        ),
                        job.get("application_date"),
                        job.get(
                            "application_notes",
                            ""
                        ),
                        job.get(
                            "extracted_skills",
                            []
                        ),
                        job.get(
                            "source",
                            "local_json"
                        ),
                        job.get("source_url"),
                        job.get("collected_at"),
                        job.get("last_seen_at"),
                        job.get(
                            "is_active",
                            True
                        ),
                        job["job_fingerprint"]
                    )
                )

                cursor.execute(
                    """
                    SELECT job_id
                    FROM jobs
                    WHERE job_fingerprint = %s
                    """,
                    (job["job_fingerprint"],)
                )

                metadata_job_id = cursor.fetchone()[0]

        connection.commit()

        save_source_metadata(
            metadata_job_id,
            job
        )

        return "inserted"

    except Exception as error:
        connection.rollback()

        print(
            "Error inserting/updating job:",
            error
        )

        return "failed"

    finally:
        connection.close()


def insert_jobs(jobs):
    results = {
        "inserted": 0,
        "updated": 0,
        "skipped": 0,
        "failed": 0
    }

    for job in jobs:
        result = insert_job(job)
        results[result] += 1

    return results


def mark_missing_jobs_inactive(jobs, source=None):
    connection = get_connection()

    try:
        current_fingerprints = {
            job["job_fingerprint"]
            for job in jobs
            if job.get("job_fingerprint")
        }

        with connection.cursor() as cursor:

            if source is None:
                cursor.execute(
                    """
                    SELECT job_id, job_fingerprint
                    FROM jobs
                    WHERE is_active = TRUE
                    """
                )
            else:
                cursor.execute(
                    """
                    SELECT job_id, job_fingerprint
                    FROM jobs
                    WHERE is_active = TRUE
                    AND source = %s
                    """,
                    (source,)
                )

            active_jobs = cursor.fetchall()

            deactivated = 0

            for job_id, fingerprint in active_jobs:

                if fingerprint not in current_fingerprints:
                    cursor.execute(
                        """
                        UPDATE jobs
                        SET is_active = FALSE
                        WHERE job_id = %s
                        """,
                        (job_id,)
                    )

                    deactivated += 1

        connection.commit()

        return deactivated

    except Exception as error:
        connection.rollback()

        print(
            "Error marking missing jobs inactive:",
            error
        )

        return 0

    finally:
        connection.close()


def get_all_jobs():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    job_id,
                    title,
                    company,
                    location,
                    salary,
                    salary_lpa,
                    description,
                    application_status,
                    application_date,
                    application_notes,
                    extracted_skills,
                    source,
                    source_url,
                    collected_at,
                    last_seen_at,
                    is_active,
                    job_fingerprint
                FROM jobs
                ORDER BY job_id
                """
            )

            rows = cursor.fetchall()

        return convert_rows_to_jobs(rows)

    except Exception as error:
        print(
            "Error retrieving jobs:",
            error
        )

        return []

    finally:
        connection.close()


def search_jobs(
    title_keyword=None,
    location=None,
    minimum_salary=None
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            query = """
                SELECT
                    job_id,
                    title,
                    company,
                    location,
                    salary,
                    salary_lpa,
                    description,
                    application_status,
                    application_date,
                    application_notes,
                    extracted_skills,
                    source,
                    source_url,
                    collected_at,
                    last_seen_at,
                    is_active,
                    job_fingerprint
                FROM jobs
                WHERE 1 = 1
            """

            parameters = []

            if title_keyword is not None:
                query += " AND title ILIKE %s"
                parameters.append(
                    f"%{title_keyword}%"
                )

            if location is not None:
                query += " AND location ILIKE %s"
                parameters.append(location)

            if minimum_salary is not None:
                query += " AND salary_lpa >= %s"
                parameters.append(
                    minimum_salary
                )

            query += (
                " ORDER BY salary_lpa DESC NULLS LAST"
            )

            cursor.execute(
                query,
                parameters
            )

            rows = cursor.fetchall()

        return convert_rows_to_jobs(rows)

    except Exception as error:
        print(
            "Error searching jobs:",
            error
        )

        return []

    finally:
        connection.close()


def update_job_skills(job_id, skills):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE jobs
                SET extracted_skills = %s
                WHERE job_id = %s
                """,
                (skills, job_id)
            )

            updated = cursor.rowcount > 0

        connection.commit()

        return updated

    except Exception as error:
        connection.rollback()

        print(
            "Error updating job skills:",
            error
        )

        return False

    finally:
        connection.close()


def update_application_status(
    job_id,
    new_status
):
    valid_statuses = [
        "Not Applied",
        "Applied",
        "Interview",
        "Rejected",
        "Offer"
    ]

    if new_status not in valid_statuses:
        return False

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            if new_status == "Applied":
                cursor.execute(
                    """
                    UPDATE jobs
                    SET
                        application_status = %s,
                        application_date = COALESCE(
                            application_date,
                            CURRENT_DATE
                        )
                    WHERE job_id = %s
                    """,
                    (
                        new_status,
                        job_id
                    )
                )

            else:
                cursor.execute(
                    """
                    UPDATE jobs
                    SET application_status = %s
                    WHERE job_id = %s
                    """,
                    (
                        new_status,
                        job_id
                    )
                )

            updated = cursor.rowcount > 0

        connection.commit()

        return updated

    except Exception as error:
        connection.rollback()

        print(
            "Error updating application status:",
            error
        )

        return False

    finally:
        connection.close()


def update_application_notes(
    job_id,
    notes
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                UPDATE jobs
                SET application_notes = %s
                WHERE job_id = %s
                """,
                (
                    notes,
                    job_id
                )
            )

            updated = cursor.rowcount > 0

        connection.commit()

        return updated

    except Exception as error:
        connection.rollback()

        print(
            "Error updating application notes:",
            error
        )

        return False

    finally:
        connection.close()


def get_application_statistics():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    application_status,
                    COUNT(*)
                FROM jobs
                GROUP BY application_status
                """
            )

            rows = cursor.fetchall()

        statistics = {
            "Not Applied": 0,
            "Applied": 0,
            "Interview": 0,
            "Rejected": 0,
            "Offer": 0
        }

        for status, count in rows:
            if status in statistics:
                statistics[status] = count

        return statistics

    except Exception as error:
        print(
            "Error retrieving statistics:",
            error
        )

        return {}

    finally:
        connection.close()


def convert_rows_to_jobs(rows):
    jobs = []

    for row in rows:
        jobs.append({
            "job_id": row[0],
            "title": row[1],
            "company": row[2],
            "location": row[3],
            "salary": row[4],
            "salary_lpa": (
                float(row[5])
                if row[5] is not None
                else None
            ),
            "description": row[6],
            "application_status": row[7],
            "application_date": (
                row[8].isoformat()
                if row[8] is not None
                else None
            ),
            "application_notes": row[9] or "",
            "extracted_skills": row[10] or [],
            "source": row[11] or "local_json",
            "source_url": row[12],
            "collected_at": (
                row[13].isoformat()
                if row[13] is not None
                else None
            ),
            "last_seen_at": (
                row[14].isoformat()
                if row[14] is not None
                else None
            ),
            "is_active": row[15],
            "job_fingerprint": row[16]
        })

    return jobs


def save_source_metadata(job_id, job):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO job_source_metadata (
                    job_id,
                    source,
                    source_job_id,
                    is_unofficial,
                    posted_at,
                    posted_days,
                    industry,
                    role_type,
                    work_type,
                    criteria,
                    updated_at
                )
                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s,
                    CURRENT_TIMESTAMP
                )
                ON CONFLICT (job_id, source)
                DO UPDATE SET
                    source_job_id = EXCLUDED.source_job_id,
                    is_unofficial = EXCLUDED.is_unofficial,
                    posted_at = EXCLUDED.posted_at,
                    posted_days = EXCLUDED.posted_days,
                    industry = EXCLUDED.industry,
                    role_type = EXCLUDED.role_type,
                    work_type = EXCLUDED.work_type,
                    criteria = EXCLUDED.criteria,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (
                    job_id,
                    job.get(
                        "source",
                        "unknown"
                    ),
                    job.get(
                        "source_job_id"
                    ),
                    job.get(
                        "source_is_unofficial"
                    ),
                    job.get(
                        "source_posted_at"
                    ),
                    job.get(
                        "source_posted_days"
                    ),
                    job.get(
                        "source_industry"
                    ),
                    job.get(
                        "source_role_type"
                    ),
                    job.get(
                        "source_work_type"
                    ),
                    Jsonb(job.get("source_criteria", []))
                )
            )

        connection.commit()

        return True

    except Exception as error:
        connection.rollback()

        print(
            "Error saving source metadata:",
            error
        )

        return False

    finally:
        connection.close()


def get_job_source_metadata(job_id, source=None):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            if source is None:
                cursor.execute(
                    """
                    SELECT
                        source,
                        source_job_id,
                        is_unofficial,
                        posted_at,
                        posted_days,
                        industry,
                        role_type,
                        work_type,
                        criteria
                    FROM job_source_metadata
                    WHERE job_id = %s
                    ORDER BY source
                    """,
                    (job_id,)
                )
            else:
                cursor.execute(
                    """
                    SELECT
                        source,
                        source_job_id,
                        is_unofficial,
                        posted_at,
                        posted_days,
                        industry,
                        role_type,
                        work_type,
                        criteria
                    FROM job_source_metadata
                    WHERE job_id = %s
                    AND source = %s
                    """,
                    (
                        job_id,
                        source
                    )
                )

            rows = cursor.fetchall()

        metadata = []

        for row in rows:
            metadata.append({
                "source": row[0],
                "source_job_id": row[1],
                "is_unofficial": row[2],
                "posted_at": row[3],
                "posted_days": row[4],
                "industry": row[5],
                "role_type": row[6],
                "work_type": row[7],
                "criteria": row[8] or []
            })

        return metadata

    except Exception as error:
        print(
            "Error retrieving job source metadata:",
            error
        )
        return []

    finally:
        connection.close()


def get_active_jobs_with_source_metadata(
    source=None,
    role_type=None,
    industry=None,
    work_type=None
):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            query = """
                SELECT
                    j.job_id,
                    j.title,
                    j.company,
                    j.location,
                    j.salary,
                    j.salary_lpa,
                    j.description,
                    j.extracted_skills,
                    j.source,
                    j.source_url,
                    j.is_active,
                    m.source_job_id,
                    m.is_unofficial,
                    m.posted_at,
                    m.posted_days,
                    m.industry,
                    m.role_type,
                    m.work_type,
                    m.criteria
                FROM jobs j
                LEFT JOIN job_source_metadata m
                    ON j.job_id = m.job_id
                    AND j.source = m.source
                WHERE j.is_active = TRUE
            """

            parameters = []

            if source is not None:
                query += """
                    AND j.source = %s
                """
                parameters.append(source)

            if role_type is not None:
                query += """
                    AND m.role_type = %s
                """
                parameters.append(role_type)

            if industry is not None:
                query += """
                    AND m.industry = %s
                """
                parameters.append(industry)

            if work_type is not None:
                query += """
                    AND m.work_type = %s
                """
                parameters.append(work_type)

            query += """
                ORDER BY j.job_id
            """

            cursor.execute(
                query,
                parameters
            )

            rows = cursor.fetchall()

        jobs = []

        for row in rows:
            jobs.append({
                "job_id": row[0],
                "title": row[1],
                "company": row[2],
                "location": row[3],
                "salary": row[4],
                "salary_lpa": (
                    float(row[5])
                    if row[5] is not None
                    else None
                ),
                "description": row[6],
                "extracted_skills": row[7] or [],
                "source": row[8],
                "source_url": row[9],
                "is_active": row[10],
                "source_job_id": row[11],
                "source_is_unofficial": row[12],
                "source_posted_at": (
                    row[13].isoformat()
                    if row[13] is not None
                    else None
                ),
                "source_posted_days": row[14],
                "source_industry": row[15],
                "source_role_type": row[16],
                "source_work_type": row[17],
                "source_criteria": row[18] or []
            })

        return jobs

    except Exception as error:
        print(
            "Error retrieving jobs with source metadata:",
            error
        )
        return []

    finally:
        connection.close()
