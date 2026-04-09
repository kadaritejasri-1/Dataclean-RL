from fastapi import FastAPI
from pydantic import BaseModel

from env.env import DataCleanEnv
from models.schemas import Action
from tasks.easy import task_easy
from tasks.medium import task_medium
from tasks.hard import task_hard
from graders.grader import grade

app = FastAPI()

env = DataCleanEnv()

# -------------------------
# TASKS
# -------------------------
TASKS = {
    "easy": task_easy,
    "medium": task_medium,
    "hard": task_hard
}

# -------------------------
# REQUEST MODELS
# -------------------------
class ResetRequest(BaseModel):
    task: str = "easy"


# -------------------------
# RESET
# -------------------------
@app.post("/reset")
def reset(req: ResetRequest):
    task = req.task

    if task == "easy":
        data = task_easy()
    elif task == "medium":
        data = task_medium()
    elif task == "hard":
        data = task_hard()
    else:
        data = task_easy()

    env.load_data(data)

    return {"message": f"{task} task loaded"}


# -------------------------
# STEP
# -------------------------
@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action.action_type)

    return {
        "observation": obs,
        "reward": reward,
        "done": done,
        "info": info
    }


# -------------------------
# STATE
# -------------------------
@app.get("/state")
def state():
    return env.state()


# -------------------------
# TASKS LIST
# -------------------------
@app.get("/tasks")
def get_tasks():
    return {
        "tasks": list(TASKS.keys()),
        "actions": [
            "fix_missing",
            "remove_duplicates",
            "convert_type",
            "normalize_text",
            "drop_row",
            "fill_default",
            "rename_column"
        ]
    }


# -------------------------
# GRADER
# -------------------------
@app.get("/grader")
def grader():
    score = grade(env.data)

    # force valid range (IMPORTANT)
    if score <= 0:
        score = 0.1
    elif score >= 1:
        score = 0.9

    return {"score": score}


# -------------------------
# BASELINE (OPTIONAL)
# -------------------------
@app.get("/baseline")
def run_baseline():
    scores = {}

    for name, task_fn in TASKS.items():
        data = task_fn()
        env.load_data(data)

        for _ in range(5):
            action = Action(action_type="remove_duplicates")
            env.step(action.action_type)

        scores[name] = grade(env.data)

    return scores
