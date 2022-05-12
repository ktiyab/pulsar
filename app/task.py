import calendar
import time

class Task(object):

    def __init__(self):
        self.task_id = None
        self.task_state = None
        self.task_notifier = None
        self.task_owners = None
        self.task_project_id = None
        self.task_region = None
        self.task_parameters = None
        self.task_timestamp = str(calendar.timegm(time.gmtime()))
        self.task_success = False
        self.task_message = None

    def to_dict(self):

        return {
            "task_id": str(self.task_id) if self.task_id else "",
            "task_state": str(self.task_state) if self.task_state else "",
            "task_notifier": str(self.task_notifier) if self.task_notifier else "",
            "task_owners": str(self.task_owners) if self.task_owners else "",
            "task_project_id": str(self.task_project_id) if self.task_project_id else "",
            "task_region": str(self.task_region) if self.task_region else "",
            "task_parameters": str(self.task_parameters) if self.task_parameters else "",
            "task_timestamp": str(self.task_timestamp) if self.task_timestamp else "",
            "task_success": str(self.task_success) if self.task_success else "",
            "task_message": str(self.task_message) if self.task_message else ""
        }