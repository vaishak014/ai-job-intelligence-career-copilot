from abc import ABC, abstractmethod


class JobSource(ABC):

    @abstractmethod
    def fetch_jobs(self):
        """
        Fetch raw jobs from a job source.

        Returns:
            list: Raw job records.
        """
        pass
