import ollama

system_prompt = """
You are a literal assistant.
Follow all instructions exactly.
Do not explain or comment.
Return only the exact literal outputs requested.
"""

def call_model_batch(prompts, model="obedient:latest"):
    joined = "\n".join(f"Task {i+1}: {p}" for i, p in enumerate(prompts))
    messages = [{"role": "system", "content": system_prompt},
                {"role": "user", "content": f"Perform all of these tasks:\n{joined}"}]
    res = ollama.chat(model=model, messages=messages)
    return res["message"]["content"].strip()

if __name__ == "__main__":
    prompts = [
        "Write B",
        "Now write A",
        "Join both letters together",
    ]
    print("=== Batch Agent ===\n")
    print(call_model_batch(prompts, model="obedient:latest"))
