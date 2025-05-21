from typing import Annotated, Dict, TypedDict, Literal, Optional, Union, List
from langgraph.graph.message import AnyMessage, add_messages


def update_dialog_stack(left: list[str], right: Optional[str]) -> list[str]:
    """Push or pop the state."""
    if right is None:
        return left
    if right == "pop":
        return left[:-1]
    return left + [right]


class State(TypedDict):
    """
    Represents the state of our graph.

    Attributes:
        keys: A dictionary where each key is a string.
    """
    messages: Annotated[list[AnyMessage], add_messages]
    name: str
    profile: List[str]
    dialog_state: Annotated[
        list[
            Literal[
                "assistant",
                "update_loan"
            ]
        ],
        update_dialog_stack,
    ]
