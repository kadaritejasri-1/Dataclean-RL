import os
import requests
from openai import OpenAI

# Environment variables (REQUIRED FORMAT)
API_BASE_URL = os.getenv("API_BASE_URL", "https://tejasri-kadari-dataclean-rl.hf.space")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")
HF_TOKEN = os.getenv("HF_TOKEN")

# Safe OpenAI client initialization
if HF_TOKEN:
    client = OpenAI(api_key=HF_TOKEN)
else:
    client = None


def run_task(task_name):
    print(f"START task={task_name}")

    # Reset environment
    r = requests.post(f"{API_BASE_URL}/reset", json={"task": task_name})
    obs = r.json()

    done = False
    total_reward = 0

    while not done:
        # Simple baseline action (can be improved later)
        action = {"action_type": "remove_duplicates"}

        r = requests.post(f"{API_BASE_URL}/step", json=action)
        res = r.json()

        reward = res.get("reward", 0)
        done = res.get("done", False)

        total_reward += reward

        print(f"STEP action={action['action_type']} reward={reward}")

        if done:
            break

    # Get final score
    r = requests.get(f"{API_BASE_URL}/grader")
    score = r.json().get("score", 0)

    print(f"END score={score}")

    return score


def main():
    results = {}

    for task in ["easy", "medium", "hard"]:
        score = run_task(task)
        results[task] = score

    print("FINAL RESULTS:", results)


if __name__ == "__main__":
    main()