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
    """
    Safe step handler:
    - Handles missing action (validation case)
    - Prevents crash
    """

    
    if action is None:
        return StepResponse(
            observation=env.reset(),  # fallback
            reward=0.0,
            done=False,
            info={"warning": "No action provided"}
        )

    try:
        obs, reward, done, info = env.step(action)

        return StepResponse(
            observation=obs,
            reward=float(reward),
            done=bool(done),
            info=info if info else {}
        )

    except Exception as e:
        return StepResponse(
            observation=env.reset(),
            reward=0.0,
            done=False,
            info={"error": str(e)}
        )



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
