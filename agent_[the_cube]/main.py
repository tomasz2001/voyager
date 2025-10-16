import ollama

# =======================
# SYSTEM prompt – literalność
# =======================
system_prompt = """
You are a literal assistant.
Follow instructions exactly.
Do not add explanations, comments, or examples.
Return only the exact output requested.
"""

# =======================
# Few-shot przykłady
# =======================
few_shot = [
    {"role": "user", "content": "Input: Write B\nOutput:"},
    {"role": "assistant", "content": "B"},
    {"role": "user", "content": "Input: Now write A\nOutput:"},
    {"role": "assistant", "content": "A"},
]

# =======================
# Funkcja wywołująca model literalnie
# =======================
def call_model_literal(prompt, model="obedient:latest"):
    messages = [{"role": "system", "content": system_prompt}] + few_shot + [{"role": "user", "content": prompt}]
    res = ollama.chat(model=model, messages=messages)
    return res["message"]["content"].strip()

# =======================
# Agent przetwarzający wiele promptów (bez historii)
# =======================
def run_prompts(prompts, model="obedient:latest"):
    print("=== Literal Agent ===\n")
    first = True

    for prompt in prompts:
        if first:
            print(f"Prompt: {prompt}")
            print("Agent: 👍 Okay, got your first instruction!\n")
            first = False
        else:
            response = call_model_literal(prompt, model)
            print(f"Prompt: {prompt}")
            print(f"Agent: {response}\n")

# =======================
# Przykład użycia
# =======================
if __name__ == "__main__":
    prompts = [
        "Write B",
        "Now write A",
        "Join both letters together",
        "Return a JSON object with previous outputs"
    ]

    run_prompts(prompts, model="obedient:latest")
