import random
from env.environment import CustomerSupportEnv
from env.models import Action, ToolCall
from env.graders import grade_episode


def run_baseline():
    print("🤖 Running  baseline ")

    random.seed(42)
    env = CustomerSupportEnv()
    obs = env.reset()

    for step in range(10):
        text = obs.ticket_text.lower()

        if step == 0:
            action = Action(action_type="classify")

        elif step == 1:
            action = Action(action_type="respond")

        elif step == 2:
            action = Action(
                action_type="tool_call",
                tool_call=ToolCall(
                    tool_name="check_order_status",
                    tool_input={"order_id": 123}
                )
            )

        elif step == 3:
            # ❗ IMPORTANT: do NOT resolve
            action = Action(action_type="respond")

        elif step == 4:
            # ❗ Sometimes escalate instead of resolve
            action = Action(action_type="escalate")

        else:
            break

        obs, reward, done, _ = env.step(action)

        print(f"Step {step+1} → {action.action_type}")

        if done:
            break

    # FINAL SCORE
    score = grade_episode(
        env.current_task,
        env.history,
        env.tool_results
    )

    print(f"🎯 Final Score: {score}")
    return score


# ==============================
# MAIN
# ==============================

if __name__ == "__main__":
    print("\n🚀 Running OPTIMAL Agent...\n")

    scores = run_baseline_all_tasks()

    print("\n📊 FINAL SCORES")
    for i, s in enumerate(scores, 1):
        print(f"Task {i} → Score: {s}")