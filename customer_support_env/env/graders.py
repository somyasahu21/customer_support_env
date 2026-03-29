def grade_episode(task, history, tool_results):
    actions = [str(h).lower() for h in history]

    score = 0.0

    
    # EXISTING LOGIC 
   

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

  

    difficulty = task.get("difficulty", "easy")

    if difficulty == "medium":
        if len(tool_results) > 0:
            score += 0.1

    if difficulty == "hard":
        # require more reasoning steps
        if len(actions) >= task.get("optimal_steps", 5):
            score += 0.2
        else:
            score -= 0.2   

     
        if len(actions) <= 4:
            score -= 0.1
  
    # FINAL CLAMP 


    return round(max(min(score, 1.0), 0.0), 3)
