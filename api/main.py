from fastapi import FastAPI
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
# RESET
# -------------------------
@app.post("/reset")
def reset(task_name: str = "easy"):
    data = TASKS.get(task_name, task_easy)
    obs = env.reset(data, task_name)
    return obs


# -------------------------
# STEP
# -------------------------
@app.post("/step")
def step(action: Action):
    obs, reward, done, info = env.step(action)
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
def get_score():
    return {"score": grade(env.df)}


# -------------------------
# BASELINE (simple)
# -------------------------
@app.get("/baseline")
def run_baseline():
    scores = {}

    for name, data in TASKS.items():
        env.reset(data, name)

        # naive agent
        for _ in range(5):
            action = Action(action_type="remove_duplicates")
            env.step(action)

        scores[name] = grade(env.df)

    return scores