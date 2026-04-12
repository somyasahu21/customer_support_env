from fastapi import FastAPI, Body
from typing import Optional
import json

from env.environment import CustomerSupportEnv
from env.graders import grade_episode
from baseline.run_baseline import run_baseline
from env.models import Action, Observation, StepResponse
from env.leaderboard import update_leaderboard

app = FastAPI(title="Customer Support OpenEnv API")

# Initialize environment
env = CustomerSupportEnv()


# ==============================
# RESET ENDPOINT
# ==============================

@app.post("/reset", response_model=Observation)
def reset():
    return env.reset()


#  REQUIRED FOR VALIDATION
@app.get("/reset")
def reset_get():
    try:
        return env.reset()
    except Exception as e:
        return {"error": str(e)}


# ==============================
# STEP ENDPOINT
# ==============================

@app.post("/step", response_model=StepResponse)
def step(action: Optional[Action] = Body(default=None)):

    if action is None:
        return StepResponse(
            observation=env.reset(),
            reward={"value": 0.0, "reason": "no action"},
            done=False,
            info={}
        )

    try:
        obs, reward, done, info = env.step(action)

        # ✅ Normalize reward 
        if isinstance(reward, dict):
            reward_value = float(reward.get("value", 0))
        else:
            reward_value = float(reward)

        
        reward_value = max(-1.0, min(1.0, reward_value))

        return StepResponse(
            observation=obs,
            reward={
                "value": reward_value,
                "reason": reward.get("reason", "step executed") if isinstance(reward, dict) else "step executed"
            },
            done=done,
            info=info or {}
        )

    except Exception as e:
        return StepResponse(
            observation=env.reset(),
            reward={"value": 0.0, "reason": "error"},
            done=False,
            info={"error": str(e)}
        )


#  REQUIRED FOR VALIDATION
@app.get("/step")
def step_get():
    return {
        "message": "Use POST /step with JSON action payload",
        "example": {
            "action_type": "tool_call",
            "tool_call": {
                "tool_name": "refund_api",
                "tool_input": {"order_id": 123}
            }
        }
    }

# ==============================
# STATE ENDPOINT 
# ==============================
@app.get("/state", response_model=dict)
def state():
    try:
        env_state = env.state()

        return {
            **env_state,

            # 🔥 Action space 
            "action_space": [
                "classify",
                "respond",
                "tool_call",
                "resolve",
                "escalate"
            ],

            # 🔥 Observation schema
            "observation_fields": [
                "ticket_text",
                "sentiment",
                "history",
                "customer_satisfaction",
                "customer_message"
            ],

            # 🔥 Extra clarity 
            "current_step": env_state.get("history", [])[-1]["step"] if env_state.get("history") else 0,
            "max_steps": 10
        }

    except Exception as e:
        return {"error": str(e)}


# ==============================
# TASKS ENDPOINT 
# ==============================

@app.get("/tasks", response_model=dict)
def tasks():
    try:
        return {
            "tasks": [t["type"] for t in env.tasks],
            "difficulties": [t.get("difficulty") for t in env.tasks],
            "action_schema": Action.model_json_schema()
        }
    except Exception as e:
        return {"error": str(e)}


# ==============================
# GRADER ENDPOINT
# ==============================

@app.post("/grader", response_model=dict)
def grader():
    try:
        score = grade_episode(
            env.current_task,
            env.history,
            env.tool_results
        )
        return {"score": float(score)}

    except Exception as e:
        return {"score": 0.0, "error": str(e)}


# ==============================
# BASELINE ENDPOINT 
# ==============================

@app.get("/baseline")
def baseline():
    try:
        print("🤖 Running smart baseline...")
        score = run_baseline()
        print(f"🎯 Score: {score}")

        # 🔥 Update leaderboard automatically
        try:
            update_leaderboard("baseline_agent", score)
        except Exception:
            pass

        return {"score": float(score)}

    except Exception as e:
        return {"score": 0.0, "error": str(e)}


# ==============================
# LEADERBOARD ENDPOINT
# ==============================

@app.get("/leaderboard")
def leaderboard():
    try:
        with open("leaderboard.json", "r") as f:
            return json.load(f)
    except:
        return []


# ==============================
# HEALTH CHECK
# ==============================

@app.get("/health")
def health():
    return {
        "status": "ok",
        "env_initialized": env is not None
    }


# ==============================
# ROOT ENDPOINT
# ==============================

@app.get("/")
def home():
    return {
        "message": "🚀 Customer Support OpenEnv API is running",
        "docs": "/docs",
        "endpoints": [
            "GET /reset",
            "POST /reset",
            "GET /step",
            "POST /step",
            "GET /state",
            "GET /tasks",
            "POST /grader",
            "GET /baseline",
            "GET /leaderboard",
            "GET /health"
        ]
    }