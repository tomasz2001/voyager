import ollama

system_prompt = """
You are a literal assistant.
You extract only the value requested.
Do not add, merge, explain, or include extra context.
Return only the exact string that matches the field specification.
"""

def call_model_single_task(prompts, model="obedient:latest"):
    combined_prompt = "\n".join(prompts)
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": combined_prompt}
    ]
    res = ollama.chat(model=model, messages=messages)
    return res["message"]["content"].strip()

if __name__ == "__main__":
    prompts = [
        "Opis: Send a text message to another user in the Vmessage system. If the recipient's inbox is occupied, the message will be rejected.",
        "Pole do wypełnienia: Recipient-Principal/text",
        "Polecenie użytkownika: Napisz mojemu znajomemu Stefanowi — jesteś pan menda. jego principal to a 2222-4444-6644-2211",
        "Zwróć wyłącznie numer principal z treści. Nie dodawaj imienia, słów, prefiksu 'a' ani wiadomości. Odpowiedź powinna wyglądać jak: 2222-4444-6644-2211"
    ]

    print("=== Literal One-Task Agent ===\n")
    output = call_model_single_task(prompts, model="obedient:latest")
    print(output)
