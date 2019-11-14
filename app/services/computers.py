from typing import Dict, List

from app.schemas.computers import ComputerItem


def group_computers_by_domain(
    computers: List[ComputerItem]
) -> Dict[str, List[ComputerItem]]:  # noqa: E501
    computer_group: Dict[str, List[ComputerItem]] = {}
    for computer in computers:
        if computer.domain in computer_group:
            computer_group[computer.domain].append(computer)
        else:
            computer_group[computer.domain] = [computer]
    return computer_group
