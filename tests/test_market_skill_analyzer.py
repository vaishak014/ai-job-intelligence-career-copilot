from app.market_skill_analyzer import (
    analyze_skill_demand
)


def test_skill_demand_uses_total_jobs_as_denominator():

    jobs = [
        {"job_id": 1},
        {"job_id": 2},
        {"job_id": 3},
        {"job_id": 4}
    ]

    job_skills_map = {
        1: [
            {
                "skill": "Python",
                "importance": "Required"
            }
        ],
        2: [
            {
                "skill": "Python",
                "importance": "Required"
            }
        ],
        3: [
            {
                "skill": "Python",
                "importance": "Preferred"
            }
        ],
        4: []
    }

    results = analyze_skill_demand(
        jobs,
        job_skills_map
    )

    assert len(results) == 1

    python = results[0]

    assert python["skill"] == "Python"
    assert python["job_count"] == 3
    assert python["required_count"] == 2
    assert python["preferred_count"] == 1

    assert python["demand_percentage"] == 75.0
    assert python["required_percentage"] == 50.0
    assert python["preferred_percentage"] == 25.0


def test_each_job_counts_only_once_per_skill():

    jobs = [
        {"job_id": 1},
        {"job_id": 2}
    ]

    job_skills_map = {
        1: [
            {
                "skill": "Python",
                "importance": "Required"
            },
            {
                "skill": "Python",
                "importance": "Preferred"
            }
        ],
        2: [
            {
                "skill": "Python",
                "importance": "Required"
            }
        ]
    }

    results = analyze_skill_demand(
        jobs,
        job_skills_map
    )

    python = results[0]

    assert python["job_count"] == 2
    assert python["demand_percentage"] == 100.0


def test_skills_are_ranked_by_job_count():

    jobs = [
        {"job_id": 1},
        {"job_id": 2},
        {"job_id": 3}
    ]

    job_skills_map = {
        1: [
            {
                "skill": "Python",
                "importance": "Required"
            },
            {
                "skill": "SQL",
                "importance": "Required"
            }
        ],
        2: [
            {
                "skill": "Python",
                "importance": "Required"
            }
        ],
        3: [
            {
                "skill": "Python",
                "importance": "Required"
            }
        ]
    }

    results = analyze_skill_demand(
        jobs,
        job_skills_map
    )

    assert results[0]["skill"] == "Python"
    assert results[0]["job_count"] == 3
    assert results[1]["skill"] == "SQL"
    assert results[1]["job_count"] == 1


def test_empty_jobs_return_empty_result():

    results = analyze_skill_demand(
        [],
        {}
    )

    assert results == []


def test_preferred_skill_percentage():

    jobs = [
        {"job_id": 1},
        {"job_id": 2},
        {"job_id": 3},
        {"job_id": 4}
    ]

    job_skills_map = {
        1: [
            {
                "skill": "Git",
                "importance": "Preferred"
            }
        ],
        2: [
            {
                "skill": "Git",
                "importance": "Preferred"
            }
        ],
        3: [],
        4: []
    }

    results = analyze_skill_demand(
        jobs,
        job_skills_map
    )

    git = results[0]

    assert git["job_count"] == 2
    assert git["required_count"] == 0
    assert git["preferred_count"] == 2

    assert git["demand_percentage"] == 50.0
    assert git["required_percentage"] == 0.0
    assert git["preferred_percentage"] == 50.0
