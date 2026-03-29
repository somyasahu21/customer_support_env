def grade_episode(task, history, tool_results):
    actions = [str(h).lower() for h in history]

    score = 0.0

    # Workflow correctness
    if "classify" in actions:
        score += 0.2

    if "respond" in actions:
        score += 0.2

    if len(tool_results) > 0:
        score += 0.2

    # Efficiency bonus
    if len(actions) <= task.get("optimal_steps", 5):
        score += 0.2

    # Resolution
    if "resolve" in actions:
        score += 0.2

    return round(min(score, 1.0), 3)
