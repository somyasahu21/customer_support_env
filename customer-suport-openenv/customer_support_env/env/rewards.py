def compute_reward(env, action):
    reward = 0.0

    # ==============================
    # BASE REWARD 
    # ==============================
    if action.action_type == "classify":
        reward += 0.2

    elif action.action_type == "respond":
        reward += 0.3

    elif action.action_type == "tool_call":
        reward += 0.4

    elif action.action_type == "resolve":
        reward += 0.6

    elif action.action_type == "escalate":
        reward += 0.2

    # ==============================
    #  FIXED: RESOLUTION BONUS
    # ==============================
    if getattr(env, "issue_resolved", False):
        reward += 0.3

    # ==============================
    #  CORRECT TOOL BONUS
    # ==============================
    if action.action_type == "tool_call" and env.hidden_required_tool:
        if any(env.hidden_required_tool in str(t).lower() for t in env.tool_results):
            reward += 0.3
        else:
            reward -= 0.2

    # ==============================
    #  REPETITION PENALTY
    # ==============================
    if len(env.history) > 1:
        if env.history[-1]["action"] == env.history[-2]["action"]:
            reward -= 0.2

    # ==============================
    #  EFFICIENCY PENALTY
    # ==============================
    reward -= 0.05 * env.step_count

    # ==============================
    #  BAD RESOLUTION PENALTY
    # ==============================
    if action.action_type == "resolve":
        if env.customer_satisfaction < 0.6:
            reward -= 0.4

    # ==============================
    # CLAMP FINAL REWARD
    # ==============================
    return float(max(min(reward, 1.0), -1.0))