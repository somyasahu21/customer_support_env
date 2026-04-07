def grade_password(task, history, tool_results):
    actions = [str(h).lower() for h in history]
    score = 0.0

    if "classify" in actions:
        score += 0.2
    if "respond" in actions:
        score += 0.2
    if any("reset" in str(t).lower() for t in tool_results):
        score += 0.3
    if "resolve" in actions:
        score += 0.3

    return min(score, 1.0)


def grade_refund(task, history, tool_results):
    actions = [str(h).lower() for h in history]
    score = 0.0

    if "classify" in actions:
        score += 0.2
    if "respond" in actions:
        score += 0.2
    if any("refund" in str(t).lower() for t in tool_results):
        score += 0.3
    if "resolve" in actions:
        score += 0.3

    return min(score, 1.0)


def grade_multi_issue(task, history, tool_results):
    actions = [str(h).lower() for h in history]
    score = 0.0

    if len(actions) >= task.get("optimal_steps", 6):
        score += 0.3
    if "respond" in actions:
        score += 0.2
    if len(tool_results) >= 1:
        score += 0.2
    if "resolve" in actions:
        score += 0.3

    return min(score, 1.0)


def grade_episode(task, history, tool_results):
    task_type = task.get("type")

    if task_type == "password_reset":
        return grade_password(task, history, tool_results)

    elif task_type == "refund":
        return grade_refund(task, history, tool_results)

    elif task_type == "multi_issue":
        return grade_multi_issue(task, history, tool_results)

    return 0.0