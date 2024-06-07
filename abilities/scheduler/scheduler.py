from typing import Optional

from ..registry import AbilityCategory, ability

@ability(
    name="schedule_test_drive",
    description="Schedule a test drive for a car",
    parameters=[
        {
            "name": "car_name",
            "description": "Name of the car to schedule a test drive for",
            "type": "string",
            "required": True,
        },
        {
            "name": "date",
            "description": "Date for the test drive",
            "type": "string",
            "required": True,
        },
        {
            "name": "time",
            "description": "Time for the test drive",
            "type": "string",
            "required": True,
        },
        {
            "name": "customer_name",
            "description": "Name of the customer",
            "type": "string",
            "required": True,
        },
        {
            "name": "customer_contact",
            "description": "Contact information of the customer",
            "type": "string",
            "required": True,
        }
    ],
    output_type="string",
    category={AbilityCategory.SCHEDULER},
)
async def schedule_test_drive(agent, task_id: str, car_name: str, date: str, time: str, customer_name: str, customer_contact: str) -> str:
    """
    Schedule a test drive for a car
    """
    # Placeholder logic for scheduling a test drive
    return f"Test drive scheduled for {car_name} on {date} at {time} for customer {customer_name} (Contact: {customer_contact})."


@ability(
    name="cancel_test_drive",
    description="Cancel a test drive for a car",
    parameters=[
        {
            "name": "car_name",
            "description": "Name of the car to cancel the test drive for",
            "type": "string",
            "required": True,
        },
        {
            "name": "date",
            "description": "Date of the test drive to cancel",
            "type": "string",
            "required": True,
        },
        {
            "name": "time",
            "description": "Time of the test drive to cancel",
            "type": "string",
            "required": True,
        },
        {
            "name": "customer_name",
            "description": "Name of the customer who scheduled the test drive",
            "type": "string",
            "required": True,
        }
    ],
    output_type="string",
    category={AbilityCategory.SCHEDULER},
)
async def cancel_test_drive(agent, task_id: str, car_name: str, date: str, time: str, customer_name: str) -> str:
    """
    Cancel a test drive for a car
    """
    # Placeholder logic for canceling a test drive
    return f"Test drive for {car_name} on {date} at {time} for customer {customer_name} has been canceled."
