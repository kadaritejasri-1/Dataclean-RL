from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import traceback

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

task_list = ["easy", "medium", "hard"]
current_task_index = 0

# -------------------------
# REQUEST MODELS
# -------------------------
class ResetRequest(BaseModel):
    task: str = "easy"


# -------------------------
# RESET (FINAL FIX: TASK ROTATION)
# -------------------------
@app.post("/reset")
def reset(req: Optional[ResetRequest] = None):
    global current_task_index

    try:
        # Use provided task OR rotate automatically
        if req and req.task:
            task = req.task
        else:
            task = task_list[current_task_index]
            current_task_index = (current_task_index + 1) % len(task_list)

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

    except Exception as e:
        print(traceback.format_exc())
        return {"error": str(e)}


# -------------------------
# STEP (SAFE)
# -------------------------
@app.post("/step")
def step(action: Optional[Action] = None):
    try:
        action_type = action.action_type if action else "remove_duplicates"

        result = env.step(action_type)

        if isinstance(result, tuple):
            if len(result) == 4:
                obs, reward, done, info = result
            elif len(result) == 3:
                obs, reward, done = result
                info = {}
            else:
                raise ValueError("Unexpected step return format")

        elif isinstance(result, dict):
            obs = result.get("observation")
            reward = result.get("reward", 0)
            done = result.get("done", False)
            info = result.get("info", {})

        else:
            raise ValueError("Invalid step return type")

        return {
            "observation": obs,
            "reward": reward,
            "done": done,
            "info": info
        }

    except Exception as e:
        print(traceback.format_exc())
        return {
            "observation": None,
            "reward": 0.0,
            "done": True,
            "info": {"error": str(e)}
        }


# -------------------------
# STATE
# -------------------------
@app.get("/state")
def state():
    try:
        return env.state()
    except Exception as e:
        print(traceback.format_exc())
        return {"error": str(e)}


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
# GRADER (STRICT RANGE FIX)
# -------------------------
@app.get("/grader")
def grader():
    try:
        score = grade(env.data)

        # STRICT FIX: never 0 or 1
        if score <= 0:
            score = 0.1
        elif score >= 1:
            score = 0.9

        return {"score": score}

    except Exception as e:
        print(traceback.format_exc())
        return {"score": 0.1}


# -------------------------
# BASELINE
# -------------------------
@app.get("/baseline")
def run_baseline():
    scores = {}

    try:
        for name, task_fn in TASKS.items():
            data = task_fn()
            env.load_data(data)

            for _ in range(5):
                env.step("remove_duplicates")

            score = grade(env.data)

            if score <= 0:
                score = 0.1
            elif score >= 1:
                score = 0.9

            scores[name] = score

        return scores

    except Exception as e:
        print(traceback.format_exc())
        return {"error": str(e)}


# -------------------------
# ROOT (OPTIONAL)
# -------------------------
@app.get("/")
def root():
    return {"message": "DataClean RL API running"}
