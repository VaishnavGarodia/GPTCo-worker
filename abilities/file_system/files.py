import os
from typing import List

from ..registry import AbilityCategory, ability

full_path = '/Users/vaishnavgarodia/Downloads/code/' + 'services/engine/memory'

@ability(
    name="list_files",
    description="List files in a directory",
    parameters=[
        {
            "name": "path",
            "description": "Path to the directory",
            "type": "string",
            "required": True,
        }
    ],
    output_type="list[str]",
    category={AbilityCategory.FILE_SYSTEM},
)
async def list_files(agent, task_id: str, path: str) -> List[str]:
    """
    List files in a workspace directory
    """
    dir_path = os.path.join(full_path, path)
    return os.listdir(dir_path)


@ability(
    name="write_file",
    description="Write data to a file",
    parameters=[
        {
            "name": "file_name",
            "description": "Name of the file",
            "type": "string",
            "required": True,
        },
        {
            "name": "data",
            "description": "Data to write to the file",
            "type": "bytes",
            "required": True,
        },
    ],
    output_type="None",
    category={AbilityCategory.FILE_SYSTEM},
)
async def write_file(agent, task_id: str, file_name: str, data: bytes):
    """
    Write data to a file
    """
    if isinstance(data, str):
        data = data.encode()

    new_file_path = os.path.join(full_path, file_name)
    with open(new_file_path, 'ab') as f:  # Change 'wb' to 'ab' for appending
        f.write(data)
    return "Data {data} written to file {file_name}"


@ability(
    name="read_file",
    description="Read data from a file",
    parameters=[
        {
            "name": "file_name",
            "description": "Path to the file",
            "type": "string",
            "required": True,
        },
    ],
    output_type="bytes",
    category={AbilityCategory.FILE_SYSTEM},
)
async def read_file(agent, task_id: str, file_name: str) -> bytes:
    """
    Read data from a file
    """
    new_file_path = os.path.join(full_path, file_name)
    with open(new_file_path, 'rb') as f:
        return f.read()
