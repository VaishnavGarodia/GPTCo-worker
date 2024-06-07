from typing import List

from ..registry import AbilityCategory, ability

@ability(
    name="initiate_call_conversation",
    description="Initiate a phone call",
    parameters=[
        {
            "name": "phone_number",
            "description": "Phone number to call",
            "type": "string",
            "required": True,
        },
        {
            "name": "message",
            "description": "message to relay during the call",
            "type": "string",
            "required": True,
        },
        {
            "name": "name",
            "description": "name of the person to call",
            "type": "string",
            "required": False,
        }
    ],
    output_type="string",
    category={AbilityCategory.CONVERSATION_SYSTEM},
)
async def initiate_call_conversation(agent, task_id: str, phone_number: str, message: str = None, name: str = "") -> str:
    """
    Initiate a phone call to the specified number
    """
    # Placeholder logic for initiating a call
    # return AbilityResult 
    return f"Call conversation happened with {phone_number} with message: {message}"


@ability(
    name="initiate_sms_conversation",
    description="Initiate a text message conversation",
    parameters=[
        {
            "name": "phone_number",
            "description": "Phone number to initate SMS conversation with",
            "type": "string",
            "required": True,
        },
        {
            "name": "motive",
            "description": "The motive of the SMS conversation",
            "type": "string",
            "required": True,
        }
    ],
    output_type="string",
    category={AbilityCategory.CONVERSATION_SYSTEM},
)
async def initiate_sms_conversation(agent, task_id: str, phone_number: str, motive: str) -> str:
    """
    Initiate an SMS message to the specified number
    """
    # Placeholder logic for initiating an SMS
    # Depending on your backend, you might integrate with SMS gateways here.
    return f"SMS conversation initiated with {phone_number} with motive: {motive}"