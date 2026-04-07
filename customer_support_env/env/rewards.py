def compute_reward(env, action):
    reward = 0.0

    if action.action_type == "classify":
        reward += 0.2 

    elif action.action_type == "respond":
        reward += 0.3

    elif action.action_type == "tool_call":
        reward += 0.4

    elif action.action_type == "resolve":
        reward += 0.6

    if env.resolved:
        reward += 0.3

    return float(max(min(reward, 1.0), 0.0))