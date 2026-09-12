from app.database import get_connection


def get_candidate_profile(candidate_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    candidate_id,
                    name,
                    education,
                    experience_years
                FROM candidate_profiles
                WHERE candidate_id = %s
                """,
                (candidate_id,)
            )

            profile = cursor.fetchone()

        if profile is None:
            return None

        return {
            "candidate_id": profile[0],
            "name": profile[1],
            "education": profile[2],
            "experience_years": float(profile[3])
        }

    except Exception as error:
        print("Error retrieving candidate profile:", error)
        return None

    finally:
        connection.close()


def get_candidate_skills(candidate_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    skill,
                    proficiency
                FROM candidate_skills
                WHERE candidate_id = %s
                ORDER BY skill
                """,
                (candidate_id,)
            )

            rows = cursor.fetchall()

        return [
            {
                "skill": row[0],
                "proficiency": row[1]
            }
            for row in rows
        ]

    except Exception as error:
        print("Error retrieving candidate skills:", error)
        return []

    finally:
        connection.close()
