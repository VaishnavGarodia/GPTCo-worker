import threading
import uuid

class ConversationSystemWorkflow:
    def __init__(self):
        self.lock = threading.Lock()

    def process(self, message, conversation_id):
        with self.lock:
            actions = self.classify_message(message, conversation_id)
            return actions

    def classify_message(self, message, conversation_id):
        actions = []

        if message.get("type") == "return_intent":
            action1_id = str(uuid.uuid4())
            action2_id = str(uuid.uuid4())
            actions = {
                action1_id: {
                'type': 'return_intent',
                'action': 'Get the return policy from the car_return_policy.txt document to check if return is possible for the specific car or not.',
                'action_id': action1_id,
                'data': message,
                'execute_now': True,
                'dependent': False,
                'next': action2_id,
                'first':True
            }, 
            action2_id: {
                'type': 'text',
                'action': 'Inform the customer about the return policy of the car. If return possible, add car back to inventory. If not, inform customer about the same.',
                'action_id': action2_id,
                'data': message,
                'execute_now': True,
                'dependent': action1_id
            }}

        if message.get("type") == "schedule_test_drive":
            action1_id = str(uuid.uuid4())
            action2_id = str(uuid.uuid4())
            actions = {
                action1_id:{
                'type': 'schedule_test_drive',
                'action': 'Schedule a test drive for the customer at the required date and time',
                'action_id': action1_id,
                'data': message,
                'execute_now': True,
                'dependent': False,
                'next': action2_id,
                'first': True
            }, 
            action2_id: {
                'type': 'text',
                'action': 'Confirm the test drive appointment to the customer by sending them a text if the test drive was scheduled successfully.',
                'action_id': action2_id,
                'data': message,
                'execute_now': True,
                'dependent': action1_id
            }
            }

        return {"conversation_id": conversation_id, "actions": actions}

    def extract_time_info(self, message):
        # This is a simplistic method to extract time info from the message.
        words = message.split()
        for i, word in enumerate(words):
            if word == "at":
                try:
                    return words[i+1]
                except IndexError:
                    return "time not specified"
        return "time not specified"

