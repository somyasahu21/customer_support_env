from fastapi import FastAPI
from env.environment import CustomerSupportEnv
from env.graders import grade_episode
from baseline.run_baseline import run_baseline
from env.models import Action, Observation, StepResponse

app = FastAPI(title="Customer Support OpenEnv API")

# Initialize environment
env = CustomerSupportEnv()


# RESET ENDPOINT
@app.get("/reset", response_model=Observation)
def reset():
    """
    Resets the environment and returns the initial observation.
    """
    return env.reset()


# STEP ENDPOINT (FULLY FIXED)
@app.post("/step", response_model=StepResponse)
def step(action: Action):
    """
    Takes an action and returns:
    - observation
    - reward
    - done
    - info
    """
    obs, reward, done, info = env.step(action)

    return StepResponse(
        observation=obs,
        reward=reward,
        done=done,
        info=info
    )


# STATE ENDPOINT
@app.get("/state", response_model=dict)
def state():
    """
    Returns the internal state of the environment.
    """
    return env.state()


# TASKS ENDPOINT (WITH ACTION SCHEMA)
@app.get("/tasks", response_model=dict)
def tasks():
    """
    Returns available tasks and action schema.
    """
    return {
        "tasks": ["easy", "medium", "hard"],
        "action_schema": Action.model_json_schema()
    }


# GRADER ENDPOINT
@app.get("/grader", response_model=dict)
def grader():
    """
    Returns score (0.0 - 1.0) for current episode.
    """
    score = grade_episode(
        env.current_task,
        env.history,
        env.tool_results
    )
    return {"score": float(score)}


# BASELINE ENDPOINT (REPRODUCIBLE)
@app.get("/baseline", response_model=dict)
def baseline():
    """
    Runs baseline agent and returns score.
    """
    return {"score": float(run_baseline())}

@app.get("/")
def home():
    return {
        "message": "🚀 Customer Support OpenEnv API is running",
        "docs": "/docs",
        "endpoints": [
            "/reset",
            "/step",
            "/state",
            "/tasks",
            "/grader",
            "/baseline"
        ]
    }
