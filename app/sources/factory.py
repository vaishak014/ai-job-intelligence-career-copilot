from app.sources.json_source import JSONJobSource
from app.sources.csv_source import CSVJobSource
from app.sources.api_source import APIJobSource
from app.sources.hopin_source import HopinSource


def create_job_source(source_type, **kwargs):

    if source_type == "json":
        return JSONJobSource(
            kwargs["file_path"]
        )

    if source_type == "csv":
        return CSVJobSource(
            kwargs["file_path"]
        )

    if source_type == "api":
        return APIJobSource(
            kwargs["url"],
            headers=kwargs.get("headers"),
            params=kwargs.get("params")
        )

    if source_type == "hopin":
        return HopinSource(
            industry=kwargs.get("industry"),
            location=kwargs.get("location"),
            work_type=kwargs.get("work_type"),
            role_type=kwargs.get("role_type"),
            is_unofficial=kwargs.get(
                "is_unofficial",
                True
            )
        )

    raise ValueError(
        f"Unsupported job source: {source_type}"
    )
