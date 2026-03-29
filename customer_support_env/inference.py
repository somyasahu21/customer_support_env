"""
🚀 OpenEnv Final Inference Script 
==================================================

✔ Uses OpenAI Client (REQUIRED)
✔ Deterministic fallback (NO failure risk)
✔ Fully reproducible
✔ Works with HF Space
✔ Handles all tasks

Author: Somya Sahu
"""

import os
import time
import requests
from typing import Dict, Any

# ==============================
# OPTIONAL LLM SUPPORT 
# ==============================

USE_LLM = True

try:
    from openai import OpenAI

    API_BASE_URL = os.getenv("API_BASE_URL")
    MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4o-mini")
    HF_TOKEN = os.getenv("HF_TOKEN")

    client = OpenAI(api_key=HF_TOKEN)

except Exception:
    USE_LLM = False


# ==============================
# CONFIGURATION
# ==============================

ENV_API = "https://somya2108-customer-support-openenv.hf.space"
MAX_STEPS = 10
SLEEP_TIME = 0.2


# ==============================
# LOGGING
# ==============================

def log_header():
    print("=" * 60)
    print("🌐 Environment:", ENV_API)
    print("🤖 Agent Mode:", "LLM + Rule Hybrid" if USE_LLM else "Rule-Based")
    print("=" * 60)


def log_step(step, obs, action, reward, total_reward):
    print(f"\n📌 STEP {step}")
    print(f"🧾 Ticket: {obs['ticket_text']}")
    print(f"🤖 Action: {action['action_type']}")

    if action.get("tool_call"):
        print(f"🔧 Tool: {action['tool_call']['tool_name']}")

    print(f"💰 Reward: {reward:.3f}")
    print(f"📊 Total Reward: {total_reward:.3f}")
    print(f"😊 Satisfaction: {obs['customer_satisfaction']:.2f}")


def log_final(score, total_reward):
    print("\n" + "=" * 60)
    print("🏁 FINAL RESULT")
    print(f"🎯 Score: {score:.3f}")
    print(f"💰 Total Reward: {total_reward:.3f}")
    print("=" * 60)


# ==============================
# RULE-BASED AGENT 
# ==============================

def extract_order_id(text: str) -> int:
    import re
    match = re.search(r"#(\d+)", text)
    return int(match.group(1)) if match else 123


def rule_based_agent(obs: Dict[str, Any]) -> Dict[str, Any]:
    text = obs["ticket_text"].lower()
    history = obs.get("history", [])

    if "password" in text:
        if "classify" not in history:
            return {"action_type": "classify"}
        if "respond" not in history:
            return {"action_type": "respond"}
        if "tool_call" not in history:
            return {
                "action_type": "tool_call",
                "tool_call": {
                    "tool_name": "send_reset_link",
                    "tool_input": {"method": "email"}
                }
            }
        return {"action_type": "resolve"}

    if "refund" in text or "charged" in text:
        order_id = extract_order_id(text)

        if "classify" not in history:
            return {"action_type": "classify"}
        if "respond" not in history:
            return {"action_type": "respond"}
        if "tool_call" not in history:
            return {
                "action_type": "tool_call",
                "tool_call": {
                    "tool_name": "refund_api",
                    "tool_input": {"order_id": order_id}
                }
            }
        return {"action_type": "resolve"}

    return {"action_type": "classify"}


# ==============================
# LLM AGENT 
# ==============================

def llm_agent(obs: Dict[str, Any]) -> Dict[str, Any]:
    try:
        prompt = f"""
        You are a customer support agent.

        Ticket: {obs['ticket_text']}
        History: {obs['history']}

        Choose ONE action:
        classify / respond / tool_call / resolve / escalate

        Output ONLY action_type.
        """

        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )

        action_type = response.choices[0].message.content.strip().lower()

        return {"action_type": action_type}

    except Exception:
        return rule_based_agent(obs)


# ==============================
# HYBRID DECISION
# ==============================

def get_action(obs):
    if USE_LLM:
        return llm_agent(obs)
    return rule_based_agent(obs)


# ==============================
# MAIN LOOP 
# ==============================

def run_episode():
    obs = requests.get(f"{ENV_API}/reset").json()
    total_reward = 0

    for step in range(1, MAX_STEPS + 1):
        action = get_action(obs)

        res = requests.post(f"{ENV_API}/step", json=action).json()

        obs = res["observation"]
        reward = res["reward"]["value"]
        done = res["done"]

        total_reward += reward

        log_step(step, obs, action, reward, total_reward)

        if done:
            print("\n✅ Episode Finished")
            break

        time.sleep(SLEEP_TIME)

    return total_reward


# ==============================
#  RUN ALL TASKS
# ==============================

def run_all_tasks():
    results = []

    for i in range(3):
        print("\n" + "=" * 60)
        print(f"🧪 RUNNING TASK {i+1}")
        print("=" * 60)

        total_reward = run_episode()

        grader = requests.get(f"{ENV_API}/grader").json()
        score = grader["score"]

        log_final(score, total_reward)

        results.append({
            "task": i+1,
            "score": score,
            "reward": total_reward
        })

    return results


# ==============================
# sequentiall task
# ==============================

def main():
    log_header()

    print("\n🚀 Running All Tasks...\n")

    results = run_all_tasks()

    print("\n" + "=" * 60)
    print("📊 FINAL SUMMARY")
    print("=" * 60)

    for r in results:
        print(f"Task {r['task']} → Score: {r['score']} | Reward: {round(r['reward'], 2)}")


# ==============================
# ENTRYPOINT
# ==============================

if __name__ == "__main__":
    main()
