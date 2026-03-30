from pydantic import BaseModel
from typing import List, Optional, Dict, Any


class ToolCall(BaseModel):
    tool_name: str
    tool_input: Dict

    class Config:
        json_schema_extra = {
            "example": {
                "tool_name": "refund_api",
                "tool_input": {"order_id": 123}
            }
        }


class Action(BaseModel):
    action_type: str
    content: Optional[str] = None
    tool_call: Optional[ToolCall] = None

    class Config:
        json_schema_extra = {
            "example": {
                "action_type": "tool_call",
                "content": "Processing refund",
                "tool_call": {
                    "tool_name": "refund_api",
                    "tool_input": {"order_id": 123}
                }
            }
        }


class Observation(BaseModel):
    ticket_id: int
    ticket_text: str
    priority: str
    sentiment: str
    history: List[str]
    tool_results: List[str]
    step_count: int
    customer_satisfaction: float

    class Config:
        json_schema_extra = {
            "example": {
                "ticket_id": 1,
                "ticket_text": "Reset my password",
                "priority": "medium",
                "sentiment": "neutral",
                "history": ["classify"],
                "tool_results": [],
                "step_count": 1,
                "customer_satisfaction": 0.8
            }
        }


class Reward(BaseModel):
    value: float
    reason: str

    class Config:
        json_schema_extra = {
            "example": {
                "value": 0.75,
                "reason": "Good response"
            }
        }


class StepResponse(BaseModel):
    observation: Observation
    reward: Reward
    done: bool
    info: Dict[str, Any]

    class Config:
        json_schema_extra = {
            "example": {
                "observation": {
                    "ticket_id": 1,
                    "ticket_text": "Reset my password",
                    "priority": "medium",
                    "sentiment": "neutral",
                    "history": ["classify"],
                    "tool_results": [],
                    "step_count": 1,
                    "customer_satisfaction": 0.8
                },
                "reward": {
                    "value": 0.75,
                    "reason": "Good response"
                },
                "done": False,
                "info": {}
            }
        }