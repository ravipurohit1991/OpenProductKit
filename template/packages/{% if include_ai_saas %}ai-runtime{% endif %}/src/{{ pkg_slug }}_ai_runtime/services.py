from __future__ import annotations

from .domain import GenerationJob, JobStatus


class InvalidTransitionError(ValueError):
    pass


_ALLOWED: dict[JobStatus, set[JobStatus]] = {
    JobStatus.QUEUED: {JobStatus.RUNNING, JobStatus.CANCELLED},
    JobStatus.RUNNING: {JobStatus.SUCCEEDED, JobStatus.FAILED, JobStatus.CANCELLED},
    JobStatus.SUCCEEDED: set(),
    JobStatus.FAILED: set(),
    JobStatus.CANCELLED: set(),
}


def transition(job: GenerationJob, target: JobStatus, **changes: object) -> GenerationJob:
    if target not in _ALLOWED[job.status]:
        raise InvalidTransitionError(f"Cannot transition {job.status} to {target}")
    if target is JobStatus.SUCCEEDED and not changes.get("output_url"):
        raise InvalidTransitionError("A succeeded job needs an output URL")
    return job.with_status(target, **changes)
