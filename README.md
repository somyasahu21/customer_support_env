---
title: Customer Support OpenEnv
emoji: "🤖"
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
license: mit
short_description: "RL-based intelligent customer support simulation with LLM + tools"
---

# 🤖 Customer Support OpenEnv 

A **real-world AI environment** where agents learn to solve customer support problems using:

✔ Multi-step reasoning
✔ Tool usage (APIs)
✔ Emotional intelligence
✔ LLM-based decision making

---

# 🚀 Live Demo

🔗 API Docs
https://somya2108-customer-support-openenv.hf.space/docs

🔗 Base URL
https://somya2108-customer-support-openenv.hf.space

---

# 🧠 What This Project Does

This system simulates **real customer support scenarios**:

* 🔐 Password reset
* 💰 Refund & billing issues
* ⚠️ Multi-problem complaints
* 🚨 Fraud / unauthorized transactions

👉 The AI agent must:

* Understand the problem
* Respond like a human
* Use tools
* Resolve or escalate

---



### 🧠 LLM-Based Semantic Grader

* Uses BERT-style embeddings
* Understands intent (not just keywords)
* Scores actions intelligently

### 🤖 Multi-Agent Interaction

* Customer replies dynamically
* Emotion changes (angry → happy)
* Real conversation simulation

### 🛠 Real API Integration

* verify_payment
* process_refund
* send_auth_otp

### 🎯 Hybrid Scoring System

* Rule-based + Semantic grading
* Final score: **0.0 → 1.0**

### 📊 Logging + Leaderboard

* Step logs
* Episode logs
* Performance tracking

---

# ⚙️ How the Environment Works

1️⃣ Reset environment
2️⃣ Agent sees ticket
3️⃣ Agent chooses action
4️⃣ Environment updates state
5️⃣ Reward given
6️⃣ Loop until solved

---

# 🧩 Action Space

```json
{
  "action_type": "classify | respond | tool_call | resolve | escalate",
  "content": "optional",
  "tool_call": {
    "tool_name": "string",
    "tool_input": {}
  }
}
```

---

# 🛠 Tools Available

| Tool               | Purpose         |
| ------------------ | --------------- |
| send_reset_link    | Reset password  |
| refund_api         | Refund          |
| process_refund     | Real refund API |
| check_order_status | Order tracking  |
| verify_payment     | Payment check   |
| send_auth_otp      | OTP auth        |
| escalate           | Human support   |

---

# 💰 Reward System

| Action    | Reward |
| --------- | ------ |
| classify  | +0.2   |
| respond   | +0.3   |
| tool_call | +0.4   |
| resolve   | +1.0   |
| escalate  | +0.2   |

Extra signals:

* 😊 Customer satisfaction
* ⏱ Efficiency penalty
* 🔁 Repetition penalty
* ❌ Wrong action penalty

👉 Final reward always: **0.0 → 1.0**

---

# 🧪 Grading System

Final Score =

* 60% Semantic (LLM understanding)
* 40% Rule-based logic


---

# 📚 Task Types

| Type     | Example        |
| -------- | -------------- |
| Easy     | Password reset |
| Medium   | Refund         |
| Hard     | Multi-issue    |
| Critical | Fraud          |

---

# 📊 Real Output (Inference)

```text
[START] task=customer_support env=openenv model=gpt-4o-mini

[STEP] step=1 action=classify reward=0.50 done=false error=null
[STEP] step=2 action=respond reward=0.53 done=false error=null
[STEP] step=3 action=tool_call reward=0.50 done=false error=null
[STEP] step=4 action=resolve reward=0.90 done=true error=null

[END] success=true steps=4 rewards=0.50,0.53,0.50,0.90
```

---

# 📈 Why This Output is Strong

✔ Correct workflow
✔ Proper tool usage
✔ Fast resolution
✔ High reward

---

# ⚙️ Run Locally

```bash
git clone https://github.com/somyasahu21/customer_support_env
cd customer_support_env
docker build -t cs-env .
docker run -p 7860:7860 cs-env
```

---

# 🚀 Run Inference

```bash
python inference.py
```

---

# 🔐 Environment Variables

```bash
API_BASE_URL=https://api.openai.com/v1
MODEL_NAME=gpt-4o-mini
HF_TOKEN=your_api_key
```

---

# 🏆 Why This Project Wins

✔ Real-world simulation
✔ LLM + RL integration
✔ Multi-agent behavior
✔ Tool-based reasoning
✔ Production-ready API

👉 This is NOT a toy project — it's a **real AI system**

---

# 🙌 Authors

**Somya Sahu** – AI Developer, RL Systems
**Girish Bagdi** – AI Developer
**Pawan Jogi** – RL Systems

---
