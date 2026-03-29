---
title: Customer Support OpenEnv
emoji: "🤖"
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
license: mit
short_description: "RL-based customer support simulation API"
---

# 🤖 Customer Support OpenEnv Environment

A **real-world reinforcement learning environment** where AI agents learn to solve customer support problems using structured reasoning, tool usage, and multi-step decision making.

---

# 🚀 Live Demo

🔗 **API Docs:**
https://somya2108-customer-support-openenv.hf.space/docs

🔗 **Base URL:**
https://somya2108-customer-support-openenv.hf.space

---

# 🧠 What This Environment Simulates

This environment models **real customer support workflows**:

* 🔐 Password reset requests
* 💰 Refund & billing issues
* ⚠️ Multi-issue complaints (late order + double charge + frustration)

Agents must behave like **real support agents**:

* Understand intent
* Respond politely
* Use backend tools
* Resolve efficiently

---

# 🎯 Why This Project is Important

Unlike toy RL environments, this system:

✅ Models **real-world business workflows**
✅ Requires **multi-step reasoning**
✅ Combines **language + decision making + tools**
✅ Can be used to evaluate **LLM agents (e.g. Nemotron, GPT)**

---

# ⚙️ OpenEnv API Design

### 🔁 Core Endpoints

| Endpoint    | Description           |
| ----------- | --------------------- |
| `/reset`    | Start new episode     |
| `/step`     | Perform an action     |
| `/state`    | Internal state        |
| `/tasks`    | Task info + schema    |
| `/grader`   | Final score (0.0–1.0) |
| `/baseline` | Run baseline agent    |

---

# 🧩 Action Space

Agents interact using structured actions:

```json
{
  "action_type": "classify | respond | tool_call | resolve | escalate",
  "content": "optional message",
  "tool_call": {
    "tool_name": "string",
    "tool_input": {}
  }
}
```

---

# 🛠️ Available Tools

| Tool                 | Purpose           |
| -------------------- | ----------------- |
| `send_reset_link`    | Reset password    |
| `refund_api`         | Process refunds   |
| `check_order_status` | Verify order      |
| `tech_diagnostics`   | Diagnose issues   |
| `escalate`           | Transfer to human |

---

# 🔄 Workflow (How the Environment Works)

Each episode follows a **multi-step interaction loop**:

### Step-by-step flow:

1. **Environment reset**

   * New ticket generated

2. **Agent observes**

   * Ticket text
   * History
   * Satisfaction score

3. **Agent decides action**

   * classify / respond / tool_call / resolve

4. **Environment updates**

   * Executes tool (if any)
   * Updates state
   * Computes reward

5. **Loop continues**

   * Until resolved / escalated / max steps

---

# 📊 Example Episode

```text
Ticket: "Reset my password"

Step 1 → classify
Step 2 → respond
Step 3 → tool_call (send_reset_link)
Step 4 → resolve
```

✔ Efficient
✔ Correct workflow
✔ High reward

---

# 💰 Reward Design (Important for RL)

Reward is **dense and informative**, not sparse:

| Action    | Reward |
| --------- | ------ |
| classify  | +0.2   |
| respond   | +0.3   |
| tool_call | +0.4   |
| resolve   | +1.0   |
| escalate  | +0.3   |

Additional signals:

* 😊 Customer satisfaction bonus
* ⏱ Step penalty (efficiency)
* 🔁 Repeated action penalty

👉 Encourages:

* Correct workflow
* Fast resolution
* Meaningful actions

---

# 🧪 Grading System (0.0 → 1.0)

Final score is computed using:

| Criteria         | Weight |
| ---------------- | ------ |
| Correct workflow | 0.4    |
| Tool usage       | 0.2    |
| Resolution       | 0.2    |
| Efficiency       | 0.2    |

✔ Deterministic
✔ Reproducible
✔ Fair evaluation

---

# 📚 Task Design

| Difficulty | Description                        |
| ---------- | ---------------------------------- |
| Easy       | Single-step issue (password reset) |
| Medium     | Refund handling                    |
| Hard       | Multi-issue + emotional user       |

👉 Hard tasks require:

* Multiple responses
* Proper sequencing
* Tool reasoning

---

# 🤖 Baseline Agent

A deterministic rule-based agent is provided:

* Ensures reproducibility
* Provides benchmark score
* Demonstrates optimal workflow

---

# 🧠 Agent Evaluation

This environment supports evaluation of:

* Rule-based agents
* LLM agents (e.g. Nemotron, GPT)
* RL-trained policies

---

# 🏆 What Makes This Environment Strong

✅ Real-world domain (customer support)
✅ Multi-step reasoning required
✅ Tool-based interaction
✅ Dense reward shaping
✅ Deterministic grading
✅ LLM-compatible

---

# ⚙️ Running Locally

```bash
git clone https://github.com/somyasahu21/customer_support_env
cd customer_support_env
docker build -t cs-env .
docker run -p 7860:7860 cs-env
```

---

# 🚀 Inference Script

Run:

```bash
python inference.py
```

✔ Deterministic + LLM hybrid
✔ Works with HF Space
✔ Produces reproducible scores

---

# 🔐 Environment Variables (Required)

```bash
API_BASE_URL=https://api.openai.com/v1
MODEL_NAME=gpt-4o-mini
HF_TOKEN=your_api_key
```

---

# 📌 Key Highlights 

✔ Fully working OpenEnv environment
✔ Real-world applicability
✔ Strong reward + grading design
✔ Clean API + Docker deployment
✔ Deterministic + LLM-ready

---
# 📊 Example Output (Inference Results)

The following results demonstrate how the environment evaluates agent performance across tasks of varying difficulty.

---

## 🧪 Evaluation Results

```text
Task        Difficulty   Score   Reward
---------------------------------------
Task 1      Medium       1.00    4.35
Task 2      Hard         0.70    3.15
Task 3      Easy         1.00    3.55
```

---

## 📈 Summary

```text
Average Score: 0.90
Total Reward: 11.05
```

---

## 🧠 Interpretation

* ✅ **Easy Task** → Fully solved with optimal steps
* ✅ **Medium Task** → Efficient handling with correct tool usage
* ⚠️ **Hard Task** → Lower score due to increased complexity and multi-issue reasoning

---

## 🎯 Key Takeaways

* The environment **successfully differentiates task difficulty**
* Rewards reflect **efficiency + correctness**
* Hard tasks require **more reasoning and steps**
* Evaluation is **realistic and non-trivial**

---

## 🏆 Why This Output Matters

This demonstrates that:

* The environment is **not a toy problem**
* Agents must perform **multi-step reasoning**
* Evaluation is **robust and meaningful**
* Suitable for benchmarking **LLM and RL agents**


# 🙌 Author

**Somya Sahu**
AI Developer | RL Systems 
**Girish Bagdi**
AI Developer 
**Pawan Jogi**
RL Systems 
---
