import random
from env.environment import CustomerSupportEnv
from env.models import Action, ToolCall

def run_baseline():
    random.seed(42)
    env = CustomerSupportEnv()
    obs = env.reset()

    total_reward = 0

    for _ in range(10):
        action = Action(
            action_type="tool_call",
            tool_call=ToolCall(
                tool_name="check_order_status",
                tool_input={"order_id": 123}
            )
        )

        obs, reward, done, _ = env.step(action)
        total_reward += reward.value

        if done:
            break

    return total_reward