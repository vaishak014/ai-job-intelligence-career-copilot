from app.sources.base import JobSource
from app.job_loader import load_jobs


class JSONJobSource(JobSource):

    def __init__(self, file_path):
        self.file_path = file_path

    def fetch_jobs(self):
        return load_jobs(self.file_path)
