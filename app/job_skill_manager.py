from app.database import get_connection


def get_or_create_skill(skill_name, category=None):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO skills (
                    skill_name,
                    category
                )
                VALUES (%s, %s)
                ON CONFLICT (skill_name)
                DO UPDATE SET
                    category = COALESCE(
                        skills.category,
                        EXCLUDED.category
                    )
                RETURNING skill_id
                """,
                (skill_name, category)
            )

            skill_id = cursor.fetchone()[0]

        connection.commit()

        return skill_id

    except Exception as error:
        connection.rollback()
        print("Error creating skill:", error)
        return None

    finally:
        connection.close()


def add_job_skill(
    job_id,
    skill_name,
    importance="Required",
    category=None
):
    valid_importance = [
        "Required",
        "Preferred"
    ]

    if importance not in valid_importance:
        return False

    skill_id = get_or_create_skill(
        skill_name,
        category
    )

    if skill_id is None:
        return False

    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO job_skills (
                    job_id,
                    skill_id,
                    importance
                )
                VALUES (%s, %s, %s)
                ON CONFLICT (job_id, skill_id)
                DO UPDATE SET
                    importance = EXCLUDED.importance
                """,
                (
                    job_id,
                    skill_id,
                    importance
                )
            )

        connection.commit()

        return True

    except Exception as error:
        connection.rollback()
        print("Error adding job skill:", error)
        return False

    finally:
        connection.close()


def get_job_skills(job_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    s.skill_name,
                    s.category,
                    js.importance
                FROM job_skills js
                JOIN skills s
                    ON js.skill_id = s.skill_id
                WHERE js.job_id = %s
                ORDER BY
                    CASE
                        WHEN js.importance = 'Required'
                        THEN 1
                        ELSE 2
                    END,
                    s.skill_name
                """,
                (job_id,)
            )

            rows = cursor.fetchall()

        return [
            {
                "skill": row[0],
                "category": row[1],
                "importance": row[2]
            }
            for row in rows
        ]

    except Exception as error:
        print("Error retrieving job skills:", error)
        return []

    finally:
        connection.close()


def get_all_job_skills():
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    js.job_id,
                    s.skill_name,
                    s.category,
                    js.importance
                FROM job_skills js
                JOIN skills s
                    ON js.skill_id = s.skill_id
                ORDER BY
                    js.job_id,
                    CASE
                        WHEN js.importance = 'Required'
                        THEN 1
                        ELSE 2
                    END,
                    s.skill_name
                """
            )

            rows = cursor.fetchall()

        job_skills = {}

        for job_id, skill, category, importance in rows:
            if job_id not in job_skills:
                job_skills[job_id] = []

            job_skills[job_id].append({
                "skill": skill,
                "category": category,
                "importance": importance
            })

        return job_skills

    except Exception as error:
        print("Error retrieving all job skills:", error)
        return {}

    finally:
        connection.close()


def sync_job_extracted_skills(
    job_id,
    skills,
    skill_categories
):
    """
    Synchronize extracted canonical skills for a job
    with the relational skills and job_skills tables.

    Existing job-skill relationships are preserved.
    """

    connection = get_connection()

    try:
        with connection.cursor() as cursor:

            for skill in skills:
                category = skill_categories.get(
                    skill
                )

                cursor.execute(
                    """
                    INSERT INTO skills (
                        skill_name,
                        category
                    )
                    VALUES (%s, %s)
                    ON CONFLICT (skill_name)
                    DO UPDATE SET
                        category = COALESCE(
                            skills.category,
                            EXCLUDED.category
                        )
                    RETURNING skill_id
                    """,
                    (
                        skill,
                        category
                    )
                )

                skill_id = cursor.fetchone()[0]

                cursor.execute(
                    """
                    INSERT INTO job_skills (
                        job_id,
                        skill_id,
                        importance
                    )
                    VALUES (%s, %s, %s)
                    ON CONFLICT (job_id, skill_id)
                    DO UPDATE SET
                        importance = EXCLUDED.importance
                    """,
                    (
                        job_id,
                        skill_id,
                        "Required"
                    )
                )

        connection.commit()

        return True

    except Exception as error:
        connection.rollback()
        print(
            "Error syncing job extracted skills:",
            error
        )
        return False

    finally:
        connection.close()
