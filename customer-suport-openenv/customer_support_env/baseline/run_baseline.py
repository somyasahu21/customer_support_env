import random
from env.environment import CustomerSupportEnv
from env.models import Action, ToolCall
from env.graders import grade_episode
from env.leaderboard import update_leaderboard


def run_baseline():
    print("🤖 Running baseline")

    random.seed(42)
    env = CustomerSupportEnv()
    obs = env.reset()

    for step in range(10):
        text = obs.ticket_text.lower()

        # ==============================
        # STEP LOGIC 
        # ==============================

        if step == 0:
            action = Action(action_type="classify")

        elif step == 1:
            action = Action(action_type="respond")

        elif step == 2:
            # 🔥 smarter tool selection
            if "password" in text:
                action = Action(
                    action_type="tool_call",
                    tool_call=ToolCall(
                        tool_name="send_reset_link",
                        tool_input={"method": "email"}
                    )
                )

            elif "refund" in text or "charged" in text:
                action = Action(
                    action_type="tool_call",
                    tool_call=ToolCall(
                        tool_name="refund_api",
                        tool_input={"order_id": 123}
                    )
                )

            elif "order" in text or "late" in text:
                action = Action(
                    action_type="tool_call",
                    tool_call=ToolCall(
                        tool_name="check_order_status",
                        tool_input={"order_id": 456}
                    )
                )

            elif "unauthorized" in text or "fraud" in text:
                action = Action(action_type="escalate")

            else:
                action = Action(action_type="respond")

        elif step == 3:
            # 🔥 fraud case must escalate
            if "unauthorized" in text or "fraud" in text:
                action = Action(action_type="escalate")
            else:
                action = Action(action_type="resolve")

        elif step == 4:
            # fallback resolution
            action = Action(action_type="resolve")

        else:
            break

        # ==============================
        # STEP EXECUTION
        # ==============================

        obs, reward, done, _ = env.step(action)

        reward_value = reward.get("value", 0) if isinstance(reward, dict) else reward

        print(f"Step {step+1} → {action.action_type} | Reward: {reward_value}")

        if done:
            break

    # ==============================
    # FINAL SCORE
    # ==============================

    score = grade_episode(
        env.current_task,
        env.history,
        env.tool_results
    )

    print(f"🎯 Final Score: {score}")

    # 🔥 Update leaderboard
    try:
        update_leaderboard("baseline_agent", score)
    except Exception:
        pass

    return score


# ==============================
# RUN MULTIPLE TASKS
# ==============================

def run_baseline_all_tasks():
    scores = []

    for i in range(4):  
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