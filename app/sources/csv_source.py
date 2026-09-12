import csv

from app.sources.base import JobSource


class CSVJobSource(JobSource):

    def __init__(self, file_path):
        self.file_path = file_path

    def fetch_jobs(self):
        jobs = []

        try:
            with open(
                self.file_path,
                "r",
                encoding="utf-8",
                newline=""
            ) as file:
                reader = csv.DictReader(file)

                for row in reader:
                    jobs.append(dict(row))

            return jobs

        except FileNotFoundError:
            print("Error: CSV job data file not found.")
            return []

        except OSError:
            print("Error: Unable to read CSV job data.")
            return []
