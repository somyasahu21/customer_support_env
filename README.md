---
title: Customer Support OpenEnv
emoji: 🤖
colorFrom: blue
colorTo: purple
sdk: docker
app_port: 7860
pinned: false
license: mit
short_description: RL-based customer support simulation API
---

# 🤖 Customer Support OpenEnv Environment

A **real-world reinforcement learning environment** where AI agents learn to handle customer support queries using structured actions, tools, and multi-step reasoning.

---

# 🚀 Live Demo

🔗 **API Docs:**  
https://somya2108-customer-support-openenv.hf.space/docs  

🔗 **Base URL:**  
https://somya2108-customer-support-openenv.hf.space  

---

# 🧠 Project Overview

This environment simulates **real customer support workflows** such as:

- Password reset requests  
- Refund processing  
- Multi-issue complaint handling  

Agents must:

✔ Understand user intent  
✔ Communicate effectively  
✔ Use tools (APIs)  
✔ Resolve or escalate issues  

---

# 🎯 Why This Matters

Customer support is a **high-impact real-world domain** used in:

- SaaS platforms  
- E-commerce systems  
- Banking & fintech  
- Technical support systems  

This environment enables training and evaluation of **AI agents capable of real operational tasks**, not games or toy problems.

---

# ⚙️ OpenEnv API Design

This project fully implements the OpenEnv standard:

### 🔁 Core Endpoints

| Endpoint | Description |
|--------|------------|
| `/reset` | Start new task |
| `/step` | Take action |
| `/state` | Current environment state |
| `/tasks` | Available tasks + schema |
| `/grader` | Returns score (0.0–1.0) |
| `/baseline` | Runs baseline agent |

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
