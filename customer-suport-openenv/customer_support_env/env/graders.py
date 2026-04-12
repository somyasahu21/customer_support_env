from .semantic_grader import grade_semantic
from env.logger import log_episode


# ==============================
# BULLETPROOF NORMALIZATION 
# ==============================
def normalize_score(score):
    score = float(score)

    if score <= 0.0:
        score = 0.001
    elif score >= 1.0:
        score = 0.999

    #  prevent floating precision issues
    score = round(score, 6)

    #  strict safety (VERY IMPORTANT)
    if score == 0.0:
        score = 0.001
    if score == 1.0:
        score = 0.999

    return score


# ==============================
# HELPER
# ==============================
def extract_actions(history):
    return [
        (h["action"] if isinstance(h, dict) else str(h)).lower()
        for h in history
    ]


# ==============================
# LEGACY RULE-BASED
# ==============================

def grade_password(task, history, tool_results):
    actions = extract_actions(history)
    score = 0.0

    if "classify" in actions:
        score += 0.2
    if "respond" in actions:
        score += 0.2

    if any("send_reset_link" in str(t).lower() for t in tool_results):
        score += 0.3

    if "resolve" in actions:
        score += 0.3

    if actions[:4] == ["classify", "respond", "tool_call", "resolve"]:
        score += 0.1

    return normalize_score(score)


def grade_refund(task, history, tool_results):
    actions = extract_actions(history)
    score = 0.0

    if "classify" in actions:
        score += 0.2
    if "respond" in actions:
        score += 0.2

    if any("process_refund" in str(t).lower() or "refund_api" in str(t).lower() for t in tool_results):
        score += 0.3

    if "resolve" in actions:
        score += 0.3

    if actions[:4] == ["classify", "respond", "tool_call", "resolve"]:
        score += 0.1

    return normalize_score(score)


def grade_multi_issue(task, history, tool_results):
    actions = extract_actions(history)
    score = 0.0

    if len(actions) >= task.get("optimal_steps", 6):
        score += 0.2

    if "respond" in actions:
        score += 0.2

    if len(tool_results) >= 1:
        score += 0.2

    combined = str(history).lower() + " " + str(tool_results).lower()

    if "refund" in combined and "order" in combined:
        score += 0.2

    if "resolve" in actions:
        score += 0.2

    return normalize_score(score)


# ==============================
# FRAUD GRADER
# ==============================

def grade_fraud(task, history, tool_results):
    actions = extract_actions(history)
    score = 0.0

    if "classify" in actions:
        score += 0.2

    if "respond" in actions:
        score += 0.2

    if "escalate" in actions:
        score += 0.4

    if actions[:4] == ["classify", "respond", "tool_call", "escalate"]:
        score += 0.2

    return normalize_score(score)


# ==============================
# FINAL HYBRID GRADER
# ==============================

def grade_episode(task, history, tool_results):

    task_type = task.get("type")

    if task_type == "password_reset":
        rule_score = grade_password(task, history, tool_results)

    elif task_type == "refund":
        rule_score = grade_refund(task, history, tool_results)

    elif task_type == "multi_issue":
        rule_score = grade_multi_issue(task, history, tool_results)

    elif task_type == "fraud":
        rule_score = grade_fraud(task, history, tool_results)

    else:
        rule_score = 0.001


    # ==============================
    # SEMANTIC SCORE
    # ==============================
    try:
        semantic_score = grade_semantic(task, history, tool_results)
        semantic_score = normalize_score(semantic_score)

    except Exception:
        semantic_score = normalize_score(0.3 + (0.4 * rule_score))


    # ==============================
    # WRONG ACTION PENALTY
    # ==============================
    actions = extract_actions(history)

    invalid_actions = ["random", "hack", "invalid"]

    penalty = 0.0
    if any(a in actions for a in invalid_actions):
        penalty -= 0.2


    # ==============================
    # FINAL SCORE
    # ==============================
    final_score = (0.6 * semantic_score) + (0.4 * rule_score) + penalty


    # ==============================
    # FINAL BOOST
    # ==============================
    if "resolve" in actions or "escalate" in actions:
        final_score += 0.1


    # ==============================
    #  FINAL SAFE NORMALIZATION
    # ==============================
    final_score = normalize_score(final_score)


    # ==============================
    # LOGGING
    # ==============================
    try:
        log_episode(task, history, final_score)
    except Exception:
        pass


    print("FINAL SCORE:", final_score)

    return final_score
