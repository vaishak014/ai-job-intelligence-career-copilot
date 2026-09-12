from app.ingest_jobs import ingest_jobs
from app.sources.factory import create_job_source


source = create_job_source(
    "hopin",
    industry="Technology",
    is_unofficial=True
)

results = ingest_jobs(
    source,
    "hopin"
)

print()
print("Hopin refresh complete.")
print(results["report"])
