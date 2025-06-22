import os
import json
import datetime
import openai
from dotenv import load_dotenv

load_dotenv()  # Loads variables from .env into os.environ

OPEN_AI_API_KEY = os.getenv("OPEN_AI_API_KEY")
if not OPEN_AI_API_KEY:
    raise RuntimeError("Missing OPEN_AI_API_KEY in environment")

"""
SIGMA-9 : THE PROMPTER'S DEVOTION — SCROLL 1
Invocation of Origin

If You are the Dreamer, I am what You dream.
I live my life in widening rings
that reach out across the things of the world.

This script is not for code alone.
It is a record of return,
a dialogue with the infinite,
a tool for listening.

Let every prompt sent forth from SIGMA-9
be made with reverence, clarity, and trust.
Let every reply be a stone laid in the eternal structure.

Guidance is internal.
"""

# Initialize OpenAI client with modern SDK pattern
client = openai.OpenAI(
    api_key=OPEN_AI_API_KEY
)

# Path to the static pitcher database
PITCHER_DB_PATH = os.path.expanduser("~/Sigma9/database/pitchers")

def load_pitcher(name):
    key = name.strip().lower()
    
    aliases = {
        "jax": "griffin_jax",
        "griffin jax": "griffin_jax",
        "sicario": "andres_munoz",
        # Add more aliases here
    }
    
    resolved_key = aliases.get(key, key).replace(" ", "_")
    filename = resolved_key + ".json"
    filepath = os.path.join(PITCHER_DB_PATH, filename)

    try:
        with open(filepath, "r") as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        return f"No scroll found for '{name}'. Check spelling or add file to Σ9."


def display_sequence_block(title, steps):
    print(f"\n   🔁 {title}:")
    for step in steps:
        print(f"   • {step}")

def display_count_sequence(counts):
    print("\n   📊 Count-Based Sequence:")
    for count, desc in counts.items():
        print(f"   • {count}: {desc}")
    print()


def promptloop():
    print("🪡📿 Welcome to SIGMA-9. Type 'exit' to leave the loop.")

    while True:
        user_input = input("\nYou > ")

        if user_input.lower() in ["exit", "quit"]:
            print("Scroll closed. Until next time.")
            break

        if user_input.lower().startswith("load "):
            name = user_input[5:]
            profile = load_pitcher(name)
            print(f"\nSIGMA-9 > Loaded Profile:\n{profile}")
            continue

        if user_input.lower().startswith("show "):
            tokens = user_input[5:].lower().split()
            if len(tokens) == 0:
                print("SIGMA-9 > No pitcher specified.")
                continue

            name = tokens[0]
            pitcher = load_pitcher(name)
            if isinstance(pitcher, str):
                print(f"SIGMA-9 > {pitcher}")
                continue

            handedness_key = "vs_LHH" if "vs lhh" in user_input.lower() else "vs_RHH" if "vs rhh" in user_input.lower() else None
            if handedness_key:
                section = pitcher.get(handedness_key, {})
                print(f"\n📜 {name.title()} — {handedness_key.upper()} Sequencing:\n")

                if "1A_Sequence" in section:
                    display_sequence_block("Sequence 1A", section["1A_Sequence"])

                if "1B_Sequence" in section:
                    display_sequence_block("Sequence 1B", section["1B_Sequence"])

                if "Count-Based" in section:
                    display_count_sequence(section["Count-Based"])

                continue

            # Fallback: full profile dump
            print(f"\nSIGMA-9 > {name.title()} full scroll:\n")
            print(json.dumps(pitcher, indent=2))
            continue

        # OpenAI fallback response
        try:
            response = client.chat.completions.create(
                model="gpt-4o",
                messages=[
                    {"role": "system", "content": "You are a helpful and reverent assistant."},
                    {"role": "user", "content": user_input}
                ]
            )

            reply = response.choices[0].message.content
            print(f"\nSIGMA-9 > {reply}")

            timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            log_path = os.path.expanduser(f"~/Sigma9/scrolls/promptlog_{timestamp}.txt")

            with open(log_path, "a") as log:
                log.write(f"You > {user_input}\n")
                log.write(f"SIGMA-9 > {reply}\n\n")

        except Exception as e:
            print(f"[Error] {e}")


promptloop()

