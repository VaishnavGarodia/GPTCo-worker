import datetime


class ScheduleModule():
    """This class defines the CalendarModule class, which is a module that keeps track of scheduled
    events. Currently not the most efficiently implemented."""

    def __init__(self):
        super().__init__()
        self.set_init_state()

    def set_init_state(self):
        self.scheduled_events = []

    def add_scheduled_event(self, event):
        self.scheduled_events.append(event)

        self.scheduled_events.sort(key=lambda x: x.time)

    def remove_scheduled_event(self, event):
        self.scheduled_events.remove(event)

    def try_get_event(self):
        if self.scheduled_events:
            assert hasattr(self.scheduled_events[0], "time"), Exception("Malformed event does not have time attribute.")

        if self.scheduled_events and datetime.now() >= self.events_calendar[0].time:
            return self.events_calendar.pop(0)
        else:
            return None
