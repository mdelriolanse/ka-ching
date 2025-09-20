from icalendar import Calendar

def parse_ical(file_path):
    with open(file_path, 'rb') as f:
        gcal = Calendar.from_ical(f.read())

    events = []
    for component in gcal.walk():
        if component.name == "VEVENT":
            event = {
                "title": str(component.get('summary')),
                "description": str(component.get('description') or ""),
                "location": str(component.get('location') or ""),
                "start": component.get('dtstart').dt.isoformat(),
                "end": component.get('dtend').dt.isoformat()
            }
            events.append(event)
    return events