import asyncio
import json
import queue
import uuid
import logging
from threading import Lock, Thread
from classes.action_executor import ActionExecutor
from modules.schedule import ScheduleModule
from modules.workflows.convsys_workflow import ConversationSystemWorkflow
from modules.workflows.leads_workflow import LeadsWorkflow

class ChangeReactor():
    """This defines the ChangeReactor class, which determines the appropriate reactions based on
    provided ChangeMonitor signals."""

    def __init__(self):
        self.lock = Lock()
        self.is_active = True
        self.schedule = ScheduleModule()
        self.action_executor = ActionExecutor()
        # create all workflows here - email, lead, inventory, etc.
        self.convsys_workflow = ConversationSystemWorkflow()
        self.leads_workflow = LeadsWorkflow()
        # creating workflows ends here.
        self.changes_in_progress = {}
        self.changes_with_errors = {}

    def enqueue_change_callback(self, msg):
        """
        Functionality if message is related to previously being executed message
        if msg.related_to_task is not None:
            if msg.related_to_task in self.changes_in_progress:
                # msg recieved is related to a task being processed. Proceed accordingly.
                pass
        """
        msg_type = msg.get("category", None)
        msg_data = msg.get("data", None)

        task_id = str(uuid.uuid4())
        self.changes_in_progress[task_id] = {"change_message": msg, "status": "classifying into workflow"}
        if msg_type == "lead":
            actions = self.leads_workflow.process(msg_data, task_id)
        elif msg_type == "inventory":
            actions = self.inventory_workflow.process(msg_data, task_id)
        elif msg_type == "convsys":
            actions = self.convsys_workflow.process(msg_data, task_id)
        else:
            print("ChangeReactor received unknown message type: " + str(msg))
            # Implement this case. Hand of task to LLM.
            self.changes_in_progress.pop(task_id)
        if not actions:
            print("ChangeReactor found no actions to take for message: " + str(msg))
            self.changes_in_progress.pop(task_id)
            return
        actions = actions["actions"]
        self.changes_in_progress[task_id]["status"] = "recieved workflow"
        self.changes_in_progress[task_id]["workflow"] = actions
        self.execute_or_schedule_actions(actions, task_id)
        
    def execute_or_schedule_actions(self, actions: dict, task_id):
        with self.lock:
            first_action = None
            for action_id in actions.keys():
                action = actions[action_id]
                if action['first']:
                    first_action = action
                    break
            result = asyncio.run(self.action_executor.execute_action(first_action, task_id))
            self.action_executed_callback(result)
            print("All executions ended for task:", task_id)
    def action_executed_callback(self, result):
        """Callback method called by the ActionExecutor when an action is finished executing.
    
        :param action: The action that was executed.
        :param task_id: The unique identifier for the task.
        :param error: An optional error message if the action resulted in an error.
        """
        
        # If there was an error while executing the action

        # Action has a result key which is dict with status and data from the actions execution.
        action = result.get("action")
        task_id = result.get("task_id")
        success = result.get("success")
        new_knowledge = result.get("new_knowledge", None)
        if not success:
            # Update the changes_in_progress dictionary to reflect the error
            if task_id in self.changes_in_progress:
                change = self.changes_in_progress[task_id]
                print(f"Error executing action for change {str(change)}. Task couldn't be performed.")
                # Escalate to manager that task couldn't be performed. 
                # TODO: make mechanism to get task back from changes_with_errors to changes_in_progress if error fixed.
                change["status"] = "error"
                self.changes_with_errors[task_id]=change
                self.changes_in_progress.pop(task_id)
            return

        # If the action was executed successfully
        change = self.changes_in_progress.get(task_id)
        workflow = change.get("workflow")
        if not change:
            print(f"No change information found for task {task_id}.")
            self.changes_in_progress.pop(task_id)
            return

        # Right now, the dependant tasks works in two ways:
        # 1. Every action has a next field which has the action_id of the next action to be executed.
        # 2. Every action has a dependant field which indicated which actions completion it depends on.
        
        # If the action has a next field, execute the next action.
        if action.get("last_action"):
            if action["last_action"] is True:
                print("Task completed successfully. Last action executed.", task_id)
                self.changes_in_progress.pop(task_id)
                return
        
        if "next" not in action:
            workflow.pop(action["action_id"])
            if len(workflow)==0:
                print("Task completed successfully. No more actions to execute", task_id)
                self.changes_in_progress.pop(task_id)
                return
            print(f"Action completed successfully {str(action)}. Waiting on actions {str(workflow)}. Task ID: {str(task_id)}")
            return
        else:
            next_action_id = action["next"] # get next action on the workflow
            next_action = workflow[next_action_id]
            workflow.pop(action["action_id"]) # remove the current successfully finished actions from workflow
            if new_knowledge is not None:
                if isinstance(new_knowledge, bytes):
                    new_knowledge = new_knowledge.decode("utf-8")
                next_action["data"].setdefault("knowledge", "")
                next_action["data"]["knowledge"] += "\n\n" + str(new_knowledge)
            action = next_action
            if action['execute_now']:
                result = asyncio.run(self.action_executor.execute_action(action, task_id))
                self.action_executed_callback(result)
