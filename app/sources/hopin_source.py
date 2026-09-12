import requests

from app.sources.base import JobSource
from app.sources.hopin_normalizer import normalize_hopin_jobs


class HopinSource(JobSource):

    BASE_URL = "https://api.hopinjobs.com/api/jobs"

    def __init__(
        self,
        industry=None,
        location=None,
        work_type=None,
        role_type=None,
        is_unofficial=True
    ):
        self.industry = industry
        self.location = location
        self.work_type = work_type
        self.role_type = role_type
        self.is_unofficial = is_unofficial

    def fetch_jobs(self):
        params = {
            "industry": self.industry,
            "location": self.location,
            "work_type": self.work_type,
            "role_type": self.role_type,
            "is_unofficial": str(
                self.is_unofficial
            ).lower()
        }

        params = {
            key: value
            for key, value in params.items()
            if value is not None
        }

        try:
            response = requests.get(
                self.BASE_URL,
                params=params,
                timeout=30
            )

            response.raise_for_status()

            data = response.json()

            jobs = data.get("jobs", [])

            if not isinstance(jobs, list):
                print(
                    "Error: Invalid Hopin jobs response."
                )
                return []

            return normalize_hopin_jobs(jobs)

        except requests.RequestException as error:
            print(
                "Error fetching jobs from Hopin:",
                error
            )
            return []

        except ValueError:
            print(
                "Error: Hopin returned invalid JSON."
            )
            return []
