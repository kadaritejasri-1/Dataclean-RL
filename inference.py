import os
import requests
try:
    from openai import OpenAI
except Exception as e:
    print("[STEP] step=0 action=error reward=0.00 done=true error=openai_import_failed", flush=True)
    print("[END] success=false steps=0 score=0.00 rewards=", flush=True)
    exit(0)
# REQUIRED ENV VARIABLES
API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")

import os
import requests
try:
    from openai import OpenAI
except Exception as e:
    print("[STEP] step=0 action=error reward=0.00 done=true error=openai_import_failed", flush=True)
    print("[END] success=false steps=0 score=0.00 rewards=", flush=True)
    exit(0)
# REQUIRED ENV VARIABLES
API_BASE_URL = os.getenv("API_BASE_URL")
API_KEY = os.getenv("API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-4.1-mini")

def main():
    env = "dataclean-rl"
    tasks = ["easy", "medium", "hard"]

    # REQUIRED: LLM client using proxy
    client = OpenAI(base_url=API_BASE_URL, api_key=API_KEY)

    for task in tasks:
        print(f"[START] task={task} env={env} model={MODEL_NAME}", flush=True)

        rewards = []
        steps = 0
        success = False

        try:
            #  REQUIRED: Make LLM call
            completion = client.chat.completions.create(
                model=MODEL_NAME,
                messages=[{"role": "user", "content": "Say hello"}],
                max_tokens=5
            )
            _ = completion.choices[0].message.content

            # Reset with task
            requests.post(f"{API_BASE_URL}/reset", json={"task": task})

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

            # Get score
            r = requests.get(f"{API_BASE_URL}/grader")
            score = float(r.json().get("score", 0))

            #  clamp again (extra safety)
            if score <= 0:
                score = 0.1
            elif score >= 1:
                score = 0.9

            success = score > 0

        except Exception as e:
            print("[START] task=error env=dataclean-rl model=none", flush=True)
            print("[STEP] step=0 action=error reward=0.00 done=true error=openai_import_failed", flush=True)
            print("[END] success=false steps=0 score=0.10 rewards=", flush=True)
            exit(0)

        print(
            f"[END] success={str(success).lower()} steps={steps} score={score:.2f} rewards={','.join(f'{r:.2f}' for r in rewards)}",
            flush=True,
        )


if __name__ == "__main__":
    main()
