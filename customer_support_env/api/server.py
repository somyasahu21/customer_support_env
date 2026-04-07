from fastapi import FastAPI, Body
from typing import Optional

from env.environment import CustomerSupportEnv
from env.graders import grade_episode
from baseline.run_baseline import run_baseline
from env.models import Action, Observation, StepResponse

app = FastAPI(title="Customer Support OpenEnv API")

# Initialize environment
env = CustomerSupportEnv()


# ==============================
# RESET ENDPOINT
# ==============================

@app.post("/reset", response_model=Observation)
def reset():
    return env.reset()


# ✅ ADD THIS (IMPORTANT FOR VALIDATION)
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

        # ✅ FIXED HERE
        if isinstance(reward, dict):
            reward_value = float(reward.get("value", 0))
        else:
            reward_value = float(reward)

        reward_value = max(0.0, min(1.0, reward_value))

        return StepResponse(
            observation=obs,
            reward={
                "value": reward_value,
                "reason": "step executed"
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

# ✅ ADD THIS 
@app.get("/step")
def step_get():
    return {
        "message": "Use POST /step with JSON action payload"
    }


# ==============================
# STATE ENDPOINT
# ==============================

@app.get("/state", response_model=dict)
def state():
    try:
        return env.state()
    except Exception as e:
        return {"error": str(e)}


# ==============================
# TASKS ENDPOINT
# ==============================

@app.get("/tasks", response_model=dict)
def tasks():
    return {
        "tasks": ["easy", "medium", "hard"],
        "action_schema": Action.model_json_schema()
    }


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

        return {"score": float(score)}

    except Exception as e:
        return {"score": 0.0, "error": str(e)}


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
            "GET /baseline"
        ]
    }