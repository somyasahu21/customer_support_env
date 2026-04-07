import random
from env.environment import CustomerSupportEnv
from env.models import Action, ToolCall
from env.graders import grade_episode


def run_baseline():
    print("🤖 Running baseline")

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
            # choose tool based on problem
            if "password" in text:
                action = Action(
                    action_type="tool_call",
                    tool_call=ToolCall(
                        tool_name="send_reset_link",
                        tool_input={"method": "email"}
                    )
                )
            else:
                action = Action(
                    action_type="tool_call",
                    tool_call=ToolCall(
                        tool_name="refund_api",
                        tool_input={"order_id": 123}
                    )
                )

        elif step == 3:
            # ✅ FINAL STEP MUST BE RESOLVE
            action = Action(action_type="resolve")

        else:
            break

        obs, reward, done, _ = env.step(action)

        print(f"Step {step+1} → {action.action_type} | Reward: {reward}")

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
# RUN MULTIPLE TASKS
# ==============================

def run_baseline_all_tasks():
    scores = []
    for i in range(3):
        print(f"\n===== TASK {i+1} =====")
        score = run_baseline()
        scores.append(score)
    return scores


# ==============================
# MAIN
# ==============================

if __name__ == "__main__":
    print("\n🚀 Running OPTIMAL Agent...\n")

    scores = run_baseline_all_tasks()

    print("\n📊 FINAL SCORES")
    for i, s in enumerate(scores, 1):
        print(f"Task {i} → Score: {s}")