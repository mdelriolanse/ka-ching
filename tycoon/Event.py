import uuid
from datetime import datetime

class Event:
    def __init__(self, title: str, start: datetime = datetime.now(), end: datetime = datetime.now(), full_day: bool = False):
        self.id = str(uuid.uuid4())
        self.title = title
        self.end = end
        self.start = start
        self.full_day = full_day

    def summary(self):
        # Ensure start/end are ISO strings
        start = self.start.isoformat() if hasattr(self.start, "isoformat") else str(self.start)
        end = self.end.isoformat() if hasattr(self.end, "isoformat") else str(self.end)
        return {
            "id": self.id,
            "title": self.title,
            "start": self.start,
            "end": self.end,
            "full_day": self.full_day
        }