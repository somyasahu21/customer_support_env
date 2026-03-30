def grade_episode(task, history, tool_results):
    actions = [str(h).lower() for h in history]

    score = 0.0

    # ==============================
    # EXISTING LOGIC 
    # ==============================

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

    # ==============================
    # DIFFICULTY-BASED SCORING 
    # ==============================

    difficulty = task.get("difficulty", "easy")

    # Medium: small bonus
    if difficulty == "medium":
        if len(tool_results) > 0:
            score += 0.05   

    # Hard: smarter logic
    if difficulty == "hard":
        optimal = task.get("optimal_steps", 5)

        # Reward deeper reasoning
        if len(actions) >= optimal:
            score += 0.1
        else:
            score -= 0.1

        # Only penalize if clearly too short
        if len(actions) < 3:
            score -= 0.1

    # ==============================
    # FINAL CLAMP 
    # ==============================

    score = max(min(score, 1.0), 0.0)

    return round(score, 3)
