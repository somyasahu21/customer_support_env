import random
from env.models import Observation, Action
from env.tasks import TASKS
from env.tools import TOOLS
from .rewards import compute_reward


class CustomerSupportEnv:

    def __init__(self):
        random.seed(42)
        self.task_index = 0
        self.reset()

    def reset(self):
        self.tasks = TASKS.copy()

        # Sequential tasks
        self.current_task = self.tasks[self.task_index % len(self.tasks)]
        self.task_index += 1

        self.history = []
        self.tool_results = []
        self.step_count = 0

        self.customer_satisfaction = 0.8
        self.resolved = False

        return self._get_obs()

    def step(self, action: Action):
        self.step_count += 1
        self.history.append(action.action_type)

        # ==============================
        # TOOL EXECUTION
        # ==============================
        if action.action_type == "tool_call" and action.tool_call:
            tool = TOOLS.get(action.tool_call.tool_name)
            if tool:
                try:
                    result = tool(**action.tool_call.tool_input)
                    self.tool_results.append(result)
                except Exception as e:
                    self.tool_results.append(f"error: {str(e)}")

        # ==============================
        # RESOLUTION
        # ==============================
        if action.action_type == "resolve":
            self.resolved = True

        # ==============================
        # REWARD FIX (FINAL CORRECT)
        # ==============================
        try:
            reward_raw = compute_reward(self, action)

            if isinstance(reward_raw, dict):
                reward_value = float(reward_raw.get("value", 0))
            else:
                reward_value = float(reward_raw)

        except Exception as e:
            print("🔥 REWARD ERROR:", str(e))
            reward_value = 0.0

        reward = {
            "value": reward_value,
            "reason": "computed"
        }

        # ==============================
        # DONE CONDITION
        # ==============================
        done = (
            self.resolved or
            action.action_type == "escalate" or
            self.step_count >= 12
        )

        return self._get_obs(), reward, done, {}

    def state(self):
        return {
            "task": self.current_task,
            "history": self.history,
            "tool_results": self.tool_results,
            "satisfaction": self.customer_satisfaction,
            "resolved": self.resolved
        }

    def _get_obs(self):
        return Observation(
            ticket_id=self.current_task["id"],
            ticket_text=self.current_task["text"],
            priority=self.current_task.get("priority", "medium"),
            sentiment=self.current_task.get("sentiment", "neutral"),
            history=self.history,
            tool_results=self.tool_results,
            step_count=self.step_count,
            customer_satisfaction=self.customer_satisfaction
        )