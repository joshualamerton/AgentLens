events = []

def publish_event(event):
    events.append(event)
    print("EVENT:", event)

def get_events():
    return events
