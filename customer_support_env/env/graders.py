def correct_tool_used(tool_results):
    return any("Refund processed" in t for t in tool_results)

def valid_sequence(history):
    return "classify" in history and "respond" in history

def grade_episode(task, history, tool_results):
    score = 0.0

    if task["requires_tool"]:
        if correct_tool_used(tool_results):
            score += 0.4

    if valid_sequence(history):
        score += 0.3

    if len(history) <= task["optimal_steps"]:
        score += 0.2

    if "resolve" in history:
        score += 0.1

    return min(score, 1.0)