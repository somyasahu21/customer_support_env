def compute_reward(env, action):
    reward = 0.0

    if action.action_type == "classify":
        reward += 0.2

    if action.action_type == "tool_call":
        reward += 0.4

    if action.action_type == "respond":
        reward += 0.3
        env.customer_satisfaction += 0.1

    if action.action_type == "resolve":
        reward += 1.0

    # penalties
    if env.step_count > 8:
        reward -= 0.2

    if action.action_type not in ["classify", "respond", "tool_call", "resolve", "escalate"]:
        reward -= 0.3

    reward += env.customer_satisfaction * 0.5
    reward -= env.step_count * 0.05

    return reward