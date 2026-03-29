from pydantic import BaseModel
from typing import List, Optional, Dict, Any

class ToolCall(BaseModel):
    tool_name: str
    tool_input: Dict

class Action(BaseModel):
    action_type: str  
    content: Optional[str] = None
    tool_call: Optional[ToolCall] = None

class Observation(BaseModel):
    ticket_id: int
    ticket_text: str
    priority: str
    sentiment: str
    history: List[str]
    tool_results: List[str]
    step_count: int
    customer_satisfaction: float

class Reward(BaseModel):
    value: float
    reason: str


class StepResponse(BaseModel):
    observation: Observation
    reward: Reward
    done: bool
    info: Dict[str, Any]
