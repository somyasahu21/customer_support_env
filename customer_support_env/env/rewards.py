def compute_reward(env, action):
    reward = 0.0

    # STEP EFFICIENCY
    reward -= env.step_count * 0.03

    # ACTION QUALITY
    if action.action_type == "classify":
        reward += 0.2

    elif action.action_type == "respond":
        reward += 0.3
        env.customer_satisfaction += 0.1

    elif action.action_type == "tool_call":
        reward += 0.4

    elif action.action_type == "resolve":
        if env.step_count <= env.current_task.get("optimal_steps", 5):
            reward += 1.2
        else:
            reward += 0.6

    elif action.action_type == "escalate":
        reward += 0.3

  
    reward += env.customer_satisfaction * 0.5

   
    if len(env.history) > 2 and env.history[-1] == env.history[-2]:
        reward -= 0.2

    return max(min(reward, 2.0), -1.0)
