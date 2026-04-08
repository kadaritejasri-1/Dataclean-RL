import os
import requests

API_BASE_URL = os.getenv("API_BASE_URL", "https://tejasri-kadari-dataclean-rl.hf.space")
MODEL_NAME = os.getenv("MODEL_NAME", "baseline")
HF_TOKEN = os.getenv("HF_TOKEN")

def main():
    task = "dataclean"
    env = "dataclean-rl"

    print(f"[START] task={task} env={env} model={MODEL_NAME}", flush=True)

    rewards = []
    steps = 0
    success = False

    try:
        # Reset
        r = requests.post(f"{API_BASE_URL}/reset", json={"task": "easy"})
        data = r.json()

        done = False

        while not done and steps < 5:
            action = {"action_type": "remove_duplicates"}

            r = requests.post(f"{API_BASE_URL}/step", json=action)
            res = r.json()

            reward = float(res.get("reward", 0))
            done = res.get("done", False)

            rewards.append(reward)
            steps += 1

            print(
                f"[STEP] step={steps} action=remove_duplicates reward={reward:.2f} done={str(done).lower()} error=null",
                flush=True,
            )

        # Final score
        r = requests.get(f"{API_BASE_URL}/grader")
        score = float(r.json().get("score", 0))

        success = score > 0

    except Exception as e:
        print(f"[STEP] step={steps} action=error reward=0.00 done=true error={str(e)}", flush=True)
        score = 0.0

    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={','.join(f'{r:.2f}' for r in rewards)}",
        flush=True,
    )


if __name__ == "__main__":
    main()
