import enum

class CaseStatus(str, enum.Enum):
    pending  = "pending"
    active   = "active"
    disposed = "disposed"
    sine_die = "sine_die"
    archived = "archived"
