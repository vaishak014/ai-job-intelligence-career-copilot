import requests

from app.sources.base import JobSource


class APIJobSource(JobSource):

    def __init__(self, url, headers=None, params=None):
        self.url = url
        self.headers = headers or {}
        self.params = params or {}

    def fetch_jobs(self):
        try:
            response = requests.get(
                self.url,
                headers=self.headers,
                params=self.params,
                timeout=10
            )

            response.raise_for_status()

            data = response.json()

            if isinstance(data, list):
                return data

            if isinstance(data, dict):
                jobs = data.get("jobs", [])

                if isinstance(jobs, list):
                    return jobs

            return []

        except requests.RequestException as error:
            print("Error fetching jobs from API:", error)
            return []

        except ValueError:
            print("Error: API returned invalid JSON.")
            return []
