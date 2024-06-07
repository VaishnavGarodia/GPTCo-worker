import json
import time
import uuid
import pprint
from concurrent.futures import ThreadPoolExecutor
from threading import Thread
import logging
from services.engine.abilities.registry import AbilityRegister
from services.engine.modules.llm import chat_completion_request
from services.engine.modules.prompting import PromptEngine


class ActionExecutor():
    """This defines the ActionExecutor class, which executes the appropriate calls based on
    provided ExecuteEventMessage signals."""

    def __init__(self):
        self.abilities = AbilityRegister(self)
        self.prompt_engine = PromptEngine("gpt-4")
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.futures = []

    async def execute_action(self, action, task_id):
        system_prompt = self.prompt_engine.load_prompt("system-format")

        action_kwargs = {
            "task": action["action"],
            "data": action["data"],
            "abilities": self.abilities.list_abilities_for_prompt(),
        }
        
        action_prompt = self.prompt_engine.load_prompt("task-step", **action_kwargs)
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": action_prompt},
        ]
        answer = None
        print("LLM Input: ", messages)
        try:
            # Define the parameters for the chat completion request
            chat_completion_kwargs = {
                "messages": messages,
                "model": "gpt-4",
            }
            chat_response = await chat_completion_request(**chat_completion_kwargs)
            answer = json.loads(chat_response["choices"][0]["message"]["content"])

        except json.JSONDecodeError as e:
            # Handle JSON decoding errors
            logging.error(f"Unable to decode chat response: {chat_response}")
            action_result = {
            "action": action,
            "task_id": task_id,
            "success": False,
             }
            return action_result
        except Exception as e:
            # Handle other exceptions
            logging.error(f"Unable to generate chat response: {e}")
        # Engine will have its own memory. It's where experiences, learnings, and other crucial data get stored. 
        # Execute the action
        ability = answer["ability"]

        # Run the ability and get the output
        output = await self.abilities.run_ability(
            task_id, ability["name"], **ability["args"]
        )

        print(f"ability executed by agent {ability} OUTPUT: {output}")
        action_result = {
            "action": action,
            "task_id": task_id,
            "success": True,
            "new_knowledge": output,
        }
        return action_result