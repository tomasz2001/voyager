import os
import math
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
async def upload_file(canister_id: str, file_path: str, note: str = ""):
    """Wysyła plik do wskazanego canistera w paczkach po 1 MB."""
    identity = load_identity()
    client = Client(url=IC_URL)
    agent = Agent(identity, client)

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
async def download_file(canister_id: str, pin_index: int, save_dir: str = "./downloads"):
    identity = load_identity()
    client = Client(url=IC_URL)
    agent = Agent(identity, client)

    param = [{"type": Types.Nat, "value": int(pin_index)}]
    pin = await ic_query(agent, canister_id, "query_pin", param)
    print("[DEBUG] Odpowiedź query_pin:", pin)

    if not pin or not isinstance(pin, dict) or len(pin) < 3:
        print("[ERROR] Nie udało się pobrać metadanych pliku.")
        return None

    values = list(pin.values())
    file_name = values[0]
    chunk_ids = values[1]
    file_note = values[2]

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

    os.makedirs(save_dir, exist_ok=True)
    save_path = os.path.join(save_dir, file_name)

    with open(save_path, "wb") as f:
        f.write(bytes(all_data))

    print(f"[OK] Zapisano plik: {save_path} ({round(len(all_data)/1024/1024,2)} MB)")
    return save_path


async def check_file(canister_id: str, pin_index: int):
    identity = load_identity()
    client = Client(url=IC_URL)
    agent = Agent(identity, client)

    param = [{"type": Types.Nat, "value": int(pin_index)}]
    pin = await ic_query(agent, canister_id, "query_pin", param)

    if not pin or not isinstance(pin, dict):
        print("[ERROR] Nie udało się pobrać metadanych pliku.")
        return None

    values = list(pin.values())
    if len(values) < 3:
        print("[ERROR] Zbyt mało danych w pin.")
        return None

    file_name = values[0]
    chunk_ids = values[1]
    file_note = values[2]
    if(file_name == "ERROR"):
        raport = f"file index = {pin_index} is not exist"
        print(raport)
        return raport

    
    raport = f"""
    file name = {file_name}
    file note = {file_note}

    file index  =  {pin_index}
    file chunk size =  {len(chunk_ids)}
    """
    print(raport)
    return raport
