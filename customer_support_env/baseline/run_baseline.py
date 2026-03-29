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



def run_baseline_all_tasks():
    random.seed(42)
    env = CustomerSupportEnv()

    results = []

    for i in range(3):
        print("\n" + "=" * 60)
        print(f"🧪 BASELINE TASK {i+1}")
        print("=" * 60)

        obs = env.reset()
        total_reward = 0

        for step in range(10):
            action = Action(
                action_type="tool_call",
                tool_call=ToolCall(
                    tool_name="check_order_status",
                    tool_input={"order_id": 123}
                )
            )

            obs, reward, done, _ = env.step(action)
            total_reward += reward.value

            print(f"Step {step+1} → Reward: {reward.value:.2f}")

            if done:
                print("✅ Episode Finished")
                break

        results.append(total_reward)

    return results



if __name__ == "__main__":
    print("\n🚀 Running Baseline on All Tasks...\n")

    results = run_baseline_all_tasks()

    print("\n" + "=" * 60)
    print("📊 BASELINE SUMMARY")
    print("=" * 60)

    for i, reward in enumerate(results, 1):
        print(f"Task {i} → Total Reward: {round(reward, 2)}")
