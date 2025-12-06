import requests
import sys


MODEL = "gemma2:2b" 
OLLAMA_URL = "http://localhost:11434/api/chat"

# Ten prompt to złoto – działa w 99,999% przypadków
SYSTEM_PROMPT = """Odpowiadasz TYLKO jednym słowem: TRUE lub FALSE.
- Żadnych innych słów
- Żadnych znaków interpunkcyjnych
- Żadnych spacji na końcu
- Żadnych wyjaśnień, myślenia, "chyba", "tak", "nie"
Tylko dokładnie: TRUE albo FALSE"""

def evaluate(condition: str) -> bool:
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": condition.strip()}
        ],
        "stream": False,
        "options": {
            "temperature": 0.0,      # zero losowości
            "num_predict": 4,        # max 4 tokeny → nie ma szans napisać nic więcej
            "stop": ["\n", " ", "."] # dodatkowe zabezpieczenie
        }
    }

    try:
        r = requests.post(OLLAMA_URL, json=payload, timeout=20)
        r.raise_for_status()
        answer = r.json()["message"]["content"].strip().upper()

        if answer == "TRUE":
            return True
        elif answer == "FALSE":
            return False
        else:
            print(f"!!! MODEL ZŁAMAŁ ZASADY → '{answer}'")
            return None

    except Exception as e:
        print(f"Błąd połączenia: {e}")
        return None


if __name__ == "__main__":
    print("Wpisz warunek do sprawdzenia (lub 'quit' żeby wyjść)\n")

    while True:
        warunek = input("Warunek: ").strip()

        if warunek.lower() in ["quit", "exit", "q", "koniec"]:
            print("Do widzenia!")
            break
        if not warunek:
            continue

        wynik = evaluate(warunek)

        if wynik is not None:
            print(f"{wynik}")
        else:
            print("[BŁĄD MODELU]")