import random
from env.models import Observation, Action
from env.tasks import TASKS
from env.tools import TOOLS
from env.customer_simulator import generate_customer_reply
from env.logger import log_step


class CustomerSupportEnv:

    def __init__(self):
        random.seed(42)
        self.task_index = 0
        self.reset()

    def reset(self):
        self.tasks = TASKS.copy()
        self.current_task = self.tasks[self.task_index % len(self.tasks)]
        self.task_index += 1

        self.history = []
        self.tool_results = []
        self.step_count = 0

        # 🔥 STATE VARIABLES
        self.customer_satisfaction = 0.7
        self.user_emotion = self.current_task.get("sentiment", "neutral")
        self.issue_resolved = False
        self.requires_escalation = self.current_task.get("requires_escalation", False)
        self.hidden_required_tool = self.current_task.get("hidden_tool", None)

        return self._get_obs()

    def step(self, action: Action):

        # ==============================
        # 🔥 ACTION VALIDATION (NEW)
        # ==============================
        valid_actions = ["classify", "respond", "tool_call", "resolve", "escalate"]

        if action.action_type not in valid_actions:
            return self._get_obs(), {"value": -1.0, "reason": "invalid_action"}, False, {}

        self.step_count += 1

        # 🔥 Store structured history
        self.history.append({
            "step": self.step_count,
            "action": action.action_type,
            "content": action.content
        })

        # 🔥 Customer response (multi-agent)
        customer_reply = generate_customer_reply(self, action)

        # ==============================
        # 🔥 TOOL EXECUTION (UPDATED)
        # ==============================
        if action.action_type == "tool_call" and action.tool_call:
            tool_name = action.tool_call.tool_name
            tool = TOOLS.get(tool_name)

            if not tool:
                self.customer_satisfaction -= 0.3
                self.tool_results.append("invalid_tool")

            else:
                try:
                    result = tool(**action.tool_call.tool_input)
                    self.tool_results.append(result)

                    if self.hidden_required_tool and tool_name == self.hidden_required_tool:
                        self.customer_satisfaction += 0.2
                    else:
                        self.customer_satisfaction -= 0.1

                except Exception as e:
                    self.tool_results.append(f"error: {str(e)}")
                    self.customer_satisfaction -= 0.2

        # ==============================
        # 🔥 RESPONSE EFFECT + SHAPING
        # ==============================
        if action.action_type == "respond":
            if self.user_emotion == "angry":
                self.customer_satisfaction += 0.05
            elif self.user_emotion == "neutral":
                self.customer_satisfaction += 0.03

        # 🔥 CLASSIFY SHAPING
        if action.action_type == "classify":
            self.customer_satisfaction += 0.02

        # 🔥 MULTI-INTENT BONUS
        task_text = self.current_task["text"].lower()
        if "refund" in task_text and "late" in task_text:
            self.customer_satisfaction += 0.05

        # ==============================
        # RESOLUTION LOGIC
        # ==============================
        if action.action_type == "resolve":
            if self.requires_escalation:
                self.customer_satisfaction -= 0.5
            elif self.customer_satisfaction > 0.75:
                self.issue_resolved = True
            else:
                self.customer_satisfaction -= 0.3

        # ==============================
        # 🔥 ESCALATION FIX
        # ==============================
        if action.action_type == "escalate":
            if self.requires_escalation:
                self.issue_resolved = True
                self.customer_satisfaction += 0.2
            else:
                self.customer_satisfaction -= 0.3  # penalty

        # 🔥 stochastic behavior
        if random.random() < 0.1:
            self.customer_satisfaction -= 0.1

        # ==============================
        # REWARD
        # ==============================
        reward_value = self._compute_reward(action)

        log_step(self.state(), action.action_type, reward_value)

        # ==============================
        # 🔥 DONE CONDITION (UPDATED)
        # ==============================
        done = (
            self.issue_resolved or
            self.step_count >= 10 or
            self.customer_satisfaction < 0.2
        )

        return self._get_obs(customer_reply), {
            "value": reward_value,
            "reason": "dynamic_reward"
        }, done, {}

    def _compute_reward(self, action):
        reward = 0.0

        # repetition penalty
        if len(self.history) > 1:
            if self.history[-1]["action"] == self.history[-2]["action"]:
                reward -= 0.2

        # 🔥 STRONG TOOL MATCH
        if action.action_type == "tool_call":
            if self.hidden_required_tool:
                if action.tool_call and action.tool_call.tool_name == self.hidden_required_tool:
                    reward += 0.5
                else:
                    reward -= 0.3

        # 🔥 SHAPING
        if action.action_type == "classify":
            reward += 0.1

        if action.action_type == "respond":
            reward += 0.1

        # resolution
        if action.action_type == "resolve":
            if self.customer_satisfaction > 0.75:
                reward += 1.0
            else:
                reward -= 0.5

        reward -= 0.05 * self.step_count

        return float(max(min(reward, 1.0), -1.0))

    # ==============================
    # OBSERVATION
    # ==============================
    def _get_obs(self, customer_message=None):
        return Observation(
            ticket_id=self.current_task["id"],
            ticket_text=self.current_task["text"],
            priority=self.current_task.get("priority", "medium"),
            sentiment=self.user_emotion,
            history=[h["action"] for h in self.history],
            tool_results=self.tool_results,
            step_count=self.step_count,
            customer_satisfaction=self.customer_satisfaction,
            customer_message=customer_message
        )

    def state(self):
        return {
            "task": self.current_task,
            "history": self.history,
            "tool_results": self.tool_results,
            "satisfaction": self.customer_satisfaction,
            "resolved": self.issue_resolved
        }