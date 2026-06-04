import enum

class CaseStatus(str, enum.Enum):
    active   = "active"
    pending  = "pending"
    disposed = "disposed"
    sine_die = "sine_die"
    archived = "archived"
