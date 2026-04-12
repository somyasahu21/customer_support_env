from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

model = SentenceTransformer("all-MiniLM-L6-v2")


def semantic_similarity(text1, text2):
    emb1 = model.encode([text1])
    emb2 = model.encode([text2])
    return cosine_similarity(emb1, emb2)[0][0]


def extract_actions(history):
    return [
        (h["action"] if isinstance(h, dict) else str(h)).lower()
        for h in history
    ]


def grade_semantic(task, history, tool_results):
    score = 0.0

    expected_intent = task.get("text", "").lower()

    actions = extract_actions(history)

    action_text = " ".join(actions)
    tool_text = " ".join([str(t).lower() for t in tool_results])

    intent_signal = action_text + " " + tool_text

    sim_intent = semantic_similarity(intent_signal, expected_intent)
    score += 0.4 * sim_intent

    # 🔥 TOOL MATCH FIX
    if task.get("hidden_tool"):
        expected_tool = task["hidden_tool"].lower()

        if expected_tool in tool_text or any(expected_tool in str(t).lower() for t in tool_results):
            score += 0.3
        else:
            sim_tool = semantic_similarity(tool_text, expected_tool)
            score += 0.3 * sim_tool

    # 🔥 RESOLUTION
    if "resolve" in actions or "escalate" in actions:
        score += 0.2

        if actions[:4] in [
            ["classify", "respond", "tool_call", "resolve"],
            ["classify", "respond", "tool_call", "escalate"]
        ]:
            score += 0.1

    # 🔥 COMPLETENESS
    if len(actions) >= task.get("optimal_steps", 4) - 1:
        score += 0.1

    return float(min(score, 1.0))