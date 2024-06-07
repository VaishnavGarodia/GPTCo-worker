import threading
import uuid

class LeadsWorkflow:
    def __init__(self):
        self.lock = threading.Lock()

    def process(self, lead, task_id):
        with self.lock:
            actions = self.classify_lead(lead, task_id)
            return actions

    def classify_lead(self, lead, task_id):
        # Simplified classification
        actions = {}

        if lead.get("type") == "new_lead":
            action1_id = str(uuid.uuid4())
            action2_id = str(uuid.uuid4())
            actions = {
                action1_id: {
                    'type': 'check_inventory',
                    'action': 'Check if item is present in the inventory or not.',
                    'action_id': action1_id,
                    'data': lead,
                    'execute_now': True,
                    'dependent': False,
                    'next': action2_id,
                    'first': True
                },
                action2_id: {
                    'type': 'text',
                    'action': 'If the car being inquired about is available in the inventory, send the car details to the lead. If not, inform the lead about the same.',
                    'action_id': action2_id,
                    'data': lead,
                    'execute_now': True,
                    'dependent': False,
                    'last_action': True
                }
            }
        return {"task_id": task_id, "actions": actions}