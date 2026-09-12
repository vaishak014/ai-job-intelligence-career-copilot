from app.job_skill_manager import add_job_skill


JOB_SKILLS = {
    1: {
        "required": [
            "Python",
            "FastAPI"
        ],
        "preferred": [
            "Git"
        ]
    },

    2: {
        "required": [
            "Python",
            "SQL",
            "Pandas"
        ],
        "preferred": [
            "Git"
        ]
    },

    3: {
        "required": [
            "Python",
            "Machine Learning",
            "scikit-learn"
        ],
        "preferred": [
            "Git"
        ]
    }
}


def setup_job_skills():
    total_added = 0

    for job_id, skill_groups in JOB_SKILLS.items():

        for skill in skill_groups["required"]:
            if add_job_skill(
                job_id,
                skill,
                "Required"
            ):
                total_added += 1

        for skill in skill_groups["preferred"]:
            if add_job_skill(
                job_id,
                skill,
                "Preferred"
            ):
                total_added += 1

    print(
        "Job-skill relationships processed:",
        total_added
    )


if __name__ == "__main__":
    setup_job_skills()
