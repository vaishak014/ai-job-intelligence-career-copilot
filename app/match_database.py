from app.database import get_connection


def save_job_match(candidate_id, job_id, match_result):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                INSERT INTO job_matches (
                    candidate_id,
                    job_id,
                    required_fit,
                    preferred_fit,
                    preferred_bonus,
                    overall_match,
                    match_category,
                    matched_required,
                    missing_required,
                    matched_preferred,
                    missing_preferred
                )
                VALUES (
                    %s, %s, %s, %s, %s,
                    %s, %s, %s, %s, %s, %s
                )
                ON CONFLICT (candidate_id, job_id)
                DO UPDATE SET
                    required_fit = EXCLUDED.required_fit,
                    preferred_fit = EXCLUDED.preferred_fit,
                    preferred_bonus = EXCLUDED.preferred_bonus,
                    overall_match = EXCLUDED.overall_match,
                    match_category = EXCLUDED.match_category,
                    matched_required = EXCLUDED.matched_required,
                    missing_required = EXCLUDED.missing_required,
                    matched_preferred = EXCLUDED.matched_preferred,
                    missing_preferred = EXCLUDED.missing_preferred,
                    created_at = CURRENT_TIMESTAMP
                """,
                (
                    candidate_id,
                    job_id,
                    match_result["required_fit"],
                    match_result["preferred_fit"],
                    match_result["preferred_bonus"],
                    match_result["overall_match"],
                    match_result["match_category"],
                    match_result["matched_required"],
                    match_result["missing_required"],
                    match_result["matched_preferred"],
                    match_result["missing_preferred"]
                )
            )

        connection.commit()

        return True

    except Exception as error:
        connection.rollback()
        print("Error saving job match:", error)
        return False

    finally:
        connection.close()


def get_saved_matches(candidate_id):
    connection = get_connection()

    try:
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT
                    jm.candidate_id,
                    jm.job_id,
                    j.title,
                    j.company,
                    jm.required_fit,
                    jm.preferred_fit,
                    jm.preferred_bonus,
                    jm.overall_match,
                    jm.match_category,
                    jm.matched_required,
                    jm.missing_required,
                    jm.matched_preferred,
                    jm.missing_preferred,
                    jm.created_at
                FROM job_matches jm
                JOIN jobs j
                    ON jm.job_id = j.job_id
                WHERE jm.candidate_id = %s
                ORDER BY jm.overall_match DESC
                """,
                (candidate_id,)
            )

            rows = cursor.fetchall()

        matches = []

        for row in rows:
            matches.append({
                "candidate_id": row[0],
                "job_id": row[1],
                "title": row[2],
                "company": row[3],
                "required_fit": float(row[4]),
                "preferred_fit": float(row[5]),
                "preferred_bonus": float(row[6]),
                "overall_match": float(row[7]),
                "match_category": row[8],
                "matched_required": row[9] or [],
                "missing_required": row[10] or [],
                "matched_preferred": row[11] or [],
                "missing_preferred": row[12] or [],
                "created_at": row[13]
            })

        return matches

    except Exception as error:
        print("Error retrieving saved matches:", error)
        return []

    finally:
        connection.close()
