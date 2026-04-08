import os

# Safe imports
try:
    import requests
except Exception as e:
    print("ERROR: requests not available", e)
    requests = None

try:
    from openai import OpenAI
except Exception as e:
    print("ERROR: openai not available", e)
    OpenAI = None


API_BASE_URL = os.getenv("API_BASE_URL", "https://tejasri-kadari-dataclean-rl.hf.space")
MODEL_NAME = os.getenv("MODEL_NAME", "gpt-3.5-turbo")
HF_TOKEN = os.getenv("HF_TOKEN")


def main():
    print("START")

    try:
        # Step 1: Call your API
        if requests:
            res = requests.get(f"{API_BASE_URL}/grader")
            print("STEP: API response", res.text)
        else:
            print("STEP: requests not available")

        # Step 2: LLM call (optional safe)
        if OpenAI and HF_TOKEN:
            client = OpenAI(api_key=HF_TOKEN)
            print("STEP: OpenAI client initialized")
        else:
            print("STEP: OpenAI skipped")

        print("END")

    except Exception as e:
        print("ERROR:", str(e))


if __name__ == "__main__":
    main()
