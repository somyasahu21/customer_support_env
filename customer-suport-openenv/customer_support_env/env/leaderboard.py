import json

LEADERBOARD_FILE = "leaderboard.json"


def update_leaderboard(agent_name, score):
    try:
        with open(LEADERBOARD_FILE, "r") as f:
            data = json.load(f)
    except:
        data = []

    data.append({
        "agent": agent_name,
        "score": score
    })

    data = sorted(data, key=lambda x: x["score"], reverse=True)[:10]

    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f, indent=2)

    return data