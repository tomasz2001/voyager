import os
import asyncio
from ic.client import Client
from ic.identity import Identity
from ic.agent import Agent
from ic.candid import encode, Types
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519

IDENTITY_FILE = "identity.pem"
IC_URL = "https://ic0.app"


# =====================================
#  Ładowanie lub generowanie tożsamości
# =====================================
def load_identity():
    if not os.path.exists(IDENTITY_FILE):
        print("[INFO] Generuję nową tożsamość...")
        key = ed25519.Ed25519PrivateKey.generate()
        pem = key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption(),
        )
        with open(IDENTITY_FILE, "wb") as f:
            f.write(pem)
    with open(IDENTITY_FILE, "rb") as f:
        pem_data = f.read()
    return Identity.from_pem(pem_data)


def create_agent(ic_url: str | None = None) -> Agent:
    """Tworzy agenta ICP używając tożsamości z pliku albo generuje ją."""
    identity = load_identity()
    client = Client(url=ic_url or IC_URL)
    return Agent(identity, client)


# =====================================
#  Funkcje do komunikacji z canisterem
# =====================================
async def ic_query(agent, canister_id, method, args=None):
    args = args or []
    result = await agent.query_raw_async(canister_id, method, encode(args))
    if isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict) and "value" in result[0]:
        return result[0]["value"]
    return None


async def ic_update(agent, canister_id, method, args=None):
    args = args or []
    result = await agent.update_raw_async(canister_id, method, encode(args))
    if isinstance(result, list) and len(result) > 0 and isinstance(result[0], dict) and "value" in result[0]:
        return result[0]["value"]
    return None


# =====================================
#  Upload pliku w paczkach po 1 MB
# =====================================
async def upload_file(canister_id: str, file_path: str, note: str = "", ic_url: str | None = None):
    """Wysyła plik do wskazanego canistera w paczkach po 1 MB."""
    agent = create_agent(ic_url)

    with open(file_path, "rb") as f:
        data = f.read()

    file_name = os.path.basename(file_path)
    file_size = len(data)
    file_size_mb = round(file_size / (1024 * 1024), 2)
    chunk_size = 1024 * 1024  # 1 MB

    print(f"[INFO] Wysyłanie pliku: {file_name} ({file_size_mb} MB)")
    chunks = [data[i:i + chunk_size] for i in range(0, len(data), chunk_size)]
    print(f"[INFO] Podzielono plik na {len(chunks)} paczek.")

    chunk_indices = []

    for i, chunk in enumerate(chunks):
        print(f"  → Wysyłanie paczki {i+1}/{len(chunks)}...")
        param = [{"type": Types.Vec(Types.Nat8), "value": list(chunk)}]
        index = await ic_update(agent, canister_id, "add_file", param)
        if index is not None:
            chunk_indices.append(index)
        else:
            print(f"[ERROR] Nie udało się zapisać paczki {i+1}")

    # Rekord File_pin
    file_pin = {
        "name": file_name,
        "file_note": f"{note} | {file_size_mb} MB | {len(chunks)} chunks",
        "file_line": chunk_indices,
    }

    param_pin = [
        {
            "type": Types.Record(
                {
                    "name": Types.Text,
                    "file_note": Types.Text,
                    "file_line": Types.Vec(Types.Nat),
                }
            ),
            "value": file_pin,
        }
    ]

    pin_index = await ic_update(agent, canister_id, "add_pin", param_pin)
    print(f"[OK] Plik zapisany w canisterze (pin_index = {pin_index})")

    return {
        "pin_index": pin_index,
        "chunks": len(chunks),
        "size_MB": file_size_mb,
        "file_name": file_name,
    }


# =====================================
#  Pobieranie i składanie pliku
# =====================================
async def download_file(
    canister_id: str,
    pin_index: int,
    save_dir: str = "./downloads",
    save_path: str | None = None,
    ic_url: str | None = None,
):
    agent = create_agent(ic_url)

    param = [{"type": Types.Nat, "value": int(pin_index)}]
    pin = await ic_query(agent, canister_id, "query_pin", param)
    print("[DEBUG] Odpowiedź query_pin:", pin)

    if not pin or not isinstance(pin, dict) or len(pin) < 3:
        print("[ERROR] Nie udało się pobrać metadanych pliku.")
        return None

    values = list(pin.values())
    file_name = pin.get("name") or values[0]
    chunk_ids = pin.get("file_line") or values[1]
    file_note = pin.get("file_note") or values[2]

    if file_name == "ERROR":
        print(f"[ERROR] Plik o indeksie {pin_index} nie istnieje lub nie można go wczytać.")
        return None

    print(f"[INFO] Pobieranie pliku {file_name} ({len(chunk_ids)} paczek)...")

    all_data = bytearray()
    for i, chunk_id in enumerate(chunk_ids):
        print(f"  → Pobieranie paczki {i+1}/{len(chunk_ids)}...")
        param = [{"type": Types.Nat, "value": chunk_id}]
        chunk = await ic_query(agent, canister_id, "query_file", param)
        if not chunk:
            print(f"[WARN] Brak paczki {chunk_id}")
            continue
        all_data.extend(chunk)

    if save_path:
        # Jeśli podano pełną ścieżkę pliku, użyj jej bezpośrednio
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
    else:
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, file_name)

    with open(save_path, "wb") as f:
        f.write(bytes(all_data))

    print(f"[OK] Zapisano plik: {save_path} ({round(len(all_data)/1024/1024,2)} MB)")
    return save_path


async def check_file(canister_id: str, pin_index: int, ic_url: str | None = None):
    agent = create_agent(ic_url)

    param = [{"type": Types.Nat, "value": int(pin_index)}]
    pin = await ic_query(agent, canister_id, "query_pin", param)

    if not pin or not isinstance(pin, dict):
        print("[ERROR] Nie udało się pobrać metadanych pliku.")
        return None

    values = list(pin.values())
    if len(values) < 3:
        print("[ERROR] Zbyt mało danych w pin.")
        return None

    # W canisterze wartość może być zwrócona jako rekord, dlatego próbujemy odczytać po kluczach.
    file_name = pin.get("name") or values[0]
    chunk_ids = pin.get("file_line") or values[1]
    file_note = pin.get("file_note") or values[2]

    if file_name == "ERROR":
        raport = {
            "exists": False,
            "pin_index": pin_index,
            "msg": "Plik nie istnieje lub nie udało się go wczytać.",
        }
        print(raport["msg"])
        return raport

    raport = {
        "exists": True,
        "pin_index": pin_index,
        "file_name": file_name,
        "file_note": file_note,
        "chunk_count": len(chunk_ids) if hasattr(chunk_ids, "__len__") else None,
    }
    print(f"[INFO] {raport}")
    return raport


async def list_pins(canister_id: str, start_index: int = 0, end_index: int = 10, ic_url: str | None = None):
    """Pobiera metadane plików (piny) w przedziale indeksów."""
    agent = create_agent(ic_url)

    result = []
    for idx in range(start_index, end_index + 1):
        try:
            param = [{"type": Types.Nat, "value": int(idx)}]
            pin = await ic_query(agent, canister_id, "query_pin", param)
            if not pin or not isinstance(pin, dict):
                continue
            values = list(pin.values())
            if len(values) < 1:
                continue
            file_name = pin.get("name") or values[0]
            # ERROR w polu name oznacza że plik nie istnieje / nie udało się wczytać.
            if file_name == "ERROR":
                result.append({
                    "index": idx,
                    "name": "<ERROR>",
                    "error": True,
                    "raw": pin,
                })
            else:
                result.append({
                    "index": idx,
                    "name": file_name,
                    "raw": pin,
                })
        except Exception:
            continue
    return result
