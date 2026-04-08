import os
import requests
try:
    from openai import OpenAI
except Exception:
    print("[START] task=dataclean env=dataclean-rl model=unknown", flush=True)
    print("[STEP] step=0 action=error reward=0.00 done=true error=openai_import_failed", flush=True)
    print("[END] success=false steps=0 score=0.00 rewards=0.00", flush=True)
    exit(0)

API_BASE_URL = os.getenv("API_BASE_URL") or "http://localhost:8000"
API_KEY = os.getenv("API_KEY", "test")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")

def main():
    task = "dataclean"
    env = "dataclean-rl"

    print(f"[START] task={task} env={env} model={MODEL_NAME}", flush=True)

    rewards = []
    steps = 0
    success = False

    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    try:
        completion = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[{"role": "user", "content": "Say hello"}],
            max_tokens=5
        )
        _ = completion.choices[0].message.content

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

        r = requests.get(f"{API_BASE_URL}/grader")
        score = float(r.json().get("score", 0))

        success = score > 0

    except Exception as e:
        print(f"[STEP] step={steps} action=error reward=0.00 done=true error={str(e)}", flush=True)
        score = 0.0

    rewards_str = ",".join(f"{r:.2f}" for r in rewards) if rewards else "0.00"

    print(
        f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={rewards_str}",
        flush=True,
    )

if __name__ == "__main__":
    main()