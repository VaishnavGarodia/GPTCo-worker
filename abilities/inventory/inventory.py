from typing import List, Optional

from ..registry import AbilityCategory, ability

@ability(
    name="list_inventory( ",
    description="List the current inventory",
    parameters=[],
    output_type="list",
    category={AbilityCategory.INVENTORY_MANAGEMENT},
)
async def check_inventory(agent, task_id: str) -> List[dict]:
    """
    Check the current inventory
    """
    # Placeholder logic for checking the inventory
    inventory = [
        {
            "item_id": "1",
            "name": "Toyota Corolla",
            "price": "$18,000",
            "car_details": "2019 model, white, 30,000 miles, 1 previous owner, excellent condition, regularly serviced, includes backup camera and Bluetooth connectivity"
        },
        {
            "item_id": "2",
            "name": "Honda Civic",
            "price": "$20,000",
            "car_details": "2020 model, black, 20,000 miles, 1 previous owner, very good condition, all scheduled maintenance performed, includes sunroof and heated seats"
        },
        {
            "item_id": "3",
            "name": "Ford Mustang",
            "price": "$25,000",
            "car_details": "2018 model, red, 25,000 miles, 2 previous owners, good condition, last serviced 3 months ago, includes premium sound system and leather seats"
        },
        {
            "item_id": "4",
            "name": "Chevrolet Malibu",
            "price": "$15,000",
            "car_details": "2017 model, blue, 40,000 miles, 2 previous owners, fair condition, regularly serviced, includes navigation system and rear parking sensors"
        },
        {
            "item_id": "5",
            "name": "BMW 3 Series",
            "price": "$35,000",
            "car_details": "2021 model, silver, 10,000 miles, 1 previous owner, excellent condition, fully serviced, includes adaptive cruise control and panoramic sunroof"
        },
    ]

    return inventory


@ability(
    name="add_item_to_inventory",
    description="Add an item to the inventory",
    parameters=[
        {
            "name": "name",
            "description": "Name of the car",
            "type": "string",
            "required": True,
        },
        {
            "name": "price",
            "description": "Price of the car",
            "type": "integer",
            "required": True,
        },
        {
            "name": "car_details",
            "description": "Details of the car",
            "type": "string",
            "required": True,
        }
    ],
    output_type="string",
    category={AbilityCategory.INVENTORY_MANAGEMENT},
)
async def add_item_to_inventory(agent, task_id: str, name: str, price: int, car_details: str) -> str:
    """
    Add an item to the inventory
    """
    # Placeholder logic for adding an item to the inventory
    return f"Item '{name}' added to inventory with price {price} and details: {car_details}."


@ability(
    name="mark_item_as_sold",
    description="Mark an item as sold",
    parameters=[
        {
            "name": "item_id",
            "description": "ID of the item to mark as sold",
            "type": "string",
            "required": True,
        },
    ],
    output_type="string",
    category={AbilityCategory.INVENTORY_MANAGEMENT},
)
async def mark_item_as_sold(agent, task_id: str, item_id: str) -> str:
    """
    Mark an item as sold
    """
    # Placeholder logic for marking an item as sold
    return f"Item with ID '{item_id}' marked as sold"


@ability(
    name="find_item_in_inventory",
    description="Find an item in the inventory",
    parameters=[
        {
            "name": "name",
            "description": "Name of the item to find",
            "type": "string",
            "required": True,
        }
    ],
    output_type="dict",
    category={AbilityCategory.INVENTORY_MANAGEMENT},
)
async def find_item_in_inventory(agent, task_id: str, name: str) -> Optional[dict]:
    """
    Find an item in the inventory
    """
    # Placeholder logic for finding an item in the inventory
    inventory = [
        {
            "item_id": "1",
            "name": "Toyota Corolla",
            "price": "$18,000",
            "car_details": "2019 model, white, 30,000 miles, 1 previous owner, excellent condition, regularly serviced, includes backup camera and Bluetooth connectivity"
        },
        {
            "item_id": "2",
            "name": "Honda Civic",
            "price": "$20,000",
            "car_details": "2020 model, black, 20,000 miles, 1 previous owner, very good condition, all scheduled maintenance performed, includes sunroof and heated seats"
        },
        {
            "item_id": "3",
            "name": "Ford Mustang",
            "price": "$25,000",
            "car_details": "2018 model, red, 25,000 miles, 2 previous owners, good condition, last serviced 3 months ago, includes premium sound system and leather seats"
        },
        {
            "item_id": "4",
            "name": "Chevrolet Malibu",
            "price": "$15,000",
            "car_details": "2017 model, blue, 40,000 miles, 2 previous owners, fair condition, regularly serviced, includes navigation system and rear parking sensors"
        },
        {
            "item_id": "5",
            "name": "BMW 3 Series",
            "price": "$35,000",
            "car_details": "2021 model, silver, 10,000 miles, 1 previous owner, excellent condition, fully serviced, includes adaptive cruise control and panoramic sunroof"
        },
    ]
    for item in inventory:
        if item["name"].lower() == name.lower():
            return "Item found in inventory: " + str(item)
    return "Item not found in inventory"
