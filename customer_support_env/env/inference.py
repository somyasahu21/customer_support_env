"""
Final Inference Script (OpenEnv Compatible)
=========================================

Uses:
- Hugging Face Router (OpenAI-compatible)
- Your deployed API

Required ENV:
- HF_TOKEN
- MODEL_NAME
"""

import os
import json
import time
import requests
from openai import OpenAI

# ==============================
# CONFIGURATION
# ==============================

# 👉 YOUR DEPLOYED ENV (IMPORTANT)
ENV_API = "https://somya2108-customer-support-openenv.hf.space"

# 👉 HF ROUTER (MANDATORY)
HF_BASE_URL = "https://router.huggingface.co/v1"

API_KEY = os.getenv("HF_TOKEN")
MODEL_NAME = os.getenv("MODEL_NAME")

MAX_STEPS = 8

if not API_KEY:
    raise ValueError("❌ HF_TOKEN not set")

if not MODEL_NAME:
    raise ValueError("❌ MODEL_NAME not set")

# ==============================
# CLIENT
# ==============================

client = OpenAI(
    base_url=HF_BASE_URL,
    api_key=API_KEY
)

print("✅ Using model:", MODEL_NAME)
print("🌐 Environment:", ENV_API)

# ==============================
# PROMPT
# ==============================

SYSTEM_PROMPT = """
You are an intelligent customer support agent.

Goal:
- Solve the customer issue
- Use tools if needed
- Minimize steps

Actions:
- classify
- respond
- tool_call
- resolve
- escalate

Return ONLY JSON:
{
  "action_type": "..."
}
"""

# ==============================
# SAFE PARSE
# ==============================

def parse_action(text):
    try:
        return json.loads(text)
    except:
        return {"action_type": "classify"}

# ==============================
# LLM AGENT
# ==============================

def get_action(obs):
    prompt = f"""
Ticket: {obs['ticket_text']}
Priority: {obs['priority']}
History: {obs['history']}
Step: {obs['step_count']}
"""

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            max_tokens=120
        )

        content = response.choices[0].message.content
        return parse_action(content)

    except Exception as e:
        print("⚠️ Model error:", e)
        return {"action_type": "classify"}

# ==============================
# MAIN LOOP
# ==============================

def main():
    print("\n🚀 STARTING INFERENCE\n")

    # RESET
    obs = requests.get(f"{ENV_API}/reset").json()

    total_reward = 0

    for step in range(1, MAX_STEPS + 1):

        print(f"\n📌 STEP {step}")
        print("🧾 Ticket:", obs["ticket_text"])

        action = get_action(obs)

        print("🤖 Action:", action)

        # STEP
        res = requests.post(
            f"{ENV_API}/step",
            json=action
        ).json()

        obs = res["observation"]
        reward = res["reward"]["value"]
        done = res["done"]

        total_reward += reward

        print(f"💰 Reward: {reward:.2f}")
        print(f"📊 Total Reward: {total_reward:.2f}")
        print(f"😊 Satisfaction: {obs['customer_satisfaction']:.2f}")

        time.sleep(0.5)

        if done:
            print("\n✅ Episode finished")
            break

    # FINAL SCORE
    grader = requests.get(f"{ENV_API}/grader").json()

    print("\n🏁 FINAL RESULT")
    print("🎯 Score:", grader["score"])
    print("💰 Total Reward:", round(total_reward, 2))


# ==============================
# RUN
# ==============================

if __name__ == "__main__":
    main()