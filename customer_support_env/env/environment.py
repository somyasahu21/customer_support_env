import random
from env.models import Observation, Action, Reward
from env.tasks import TASKS
from env.tools import TOOLS
from env.rewards import compute_reward

class CustomerSupportEnv:

    def __init__(self):
        random.seed(42)
        self.reset()

    def reset(self):
        self.tasks = TASKS.copy()
        self.current_task = self.tasks.pop(0)
        self.history = []
        self.tool_results = []
        self.step_count = 0
        self.customer_satisfaction = 1.0
        return self._get_obs()

    def step(self, action: Action):
        self.step_count += 1
        self.history.append(action.action_type)

        if action.action_type == "tool_call" and action.tool_call:
            tool = TOOLS.get(action.tool_call.tool_name)
            if tool:
                result = tool(**action.tool_call.tool_input)
                self.tool_results.append(result)

        reward_value = compute_reward(self, action)
        reward = Reward(value=reward_value, reason="computed")

        done = action.action_type in ["resolve", "escalate"] or self.step_count > 10

        return self._get_obs(), reward, done, {}

    def state(self):
        return {
            "task": self.current_task,
            "history": self.history,
            "tool_results": self.tool_results,
            "satisfaction": self.customer_satisfaction
        }

    def _get_obs(self):
        return Observation(
            ticket_id=self.current_task["id"],
            ticket_text=self.current_task["text"],
            priority=self.current_task.get("priority", "medium"),
            sentiment="neutral",
            history=self.history,
            tool_results=self.tool_results,
            step_count=self.step_count,
            customer_satisfaction=self.customer_satisfaction
        )