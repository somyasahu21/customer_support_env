import json
import os

LOG_FILE = "episode_logs.jsonl"


def log_step(state, action, reward):
    record = {
        "state": state,
        "action": action,
        "reward": reward
    }

    with open(LOG_FILE, "a") as f:
        f.write(json.dumps(record) + "\n")


def log_episode(task, history, score):
    record = {
        "task": task,
        "history": history,
        "score": score
    }

    with open("episodes_summary.jsonl", "a") as f:
        f.write(json.dumps(record) + "\n")