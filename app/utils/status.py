from app.enums import CaseStatus


def normalize_status(value: str) -> CaseStatus:
    if not value:
        return CaseStatus.pending

    v = str(value).lower().strip()

    if v in ["allowed", "active"]:
        return CaseStatus.active

    if v in ["pending", "open", "in progress"]:
        return CaseStatus.pending

    if v in ["dismissed", "disposed", "rejected", "closed"]:
        return CaseStatus.disposed

    if v in ["sine die", "sine-die", "sign die"]:
        return CaseStatus.sine_die

    if v in ["archived", "archieve", "archieved"]:
        return CaseStatus.archived

    return CaseStatus.pending
