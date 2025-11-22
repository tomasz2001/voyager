import serial
import time
import asyncio
from ic.client import Client
from ic.identity import Identity
from ic.agent import Agent
from ic.candid import encode, Types

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.backends import default_backend

import subprocess
import os
import signal
import sys
identity_file = "identity.pem"

if os.path.exists(identity_file):
    with open(identity_file, "r") as f:
        private_key_pem = f.read().strip()
else:
    private_key_pem = ""


# Function to generate a new identity
def generate_new_identity():
    try:
        private_key = ed25519.Ed25519PrivateKey.generate()
        pem_pkcs8 = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        ).decode('utf-8')
        with open(identity_file, "w") as f:
            f.write(pem_pkcs8)
        print(f"New identity saved to {identity_file}", flush=True)
        return pem_pkcs8
    except Exception as e:
        print(f"Identity generation error: {e}", flush=True)
        return None


# Function to load identity from PEM data
def load_identity_from_pem(pem_data):
    global private_key_pem
    try:
        if not pem_data or not pem_data.startswith("-----BEGIN PRIVATE KEY-----"):
            print("No key found, generating new identity...", flush=True)
            pem_data = generate_new_identity()
            if pem_data is None:
                return None
            private_key_pem = pem_data.strip()

        identity = Identity.from_pem(pem_data)
        return identity
    except Exception as e:
        print(f"Error loading identity: {e}", flush=True)
        return None
# canister conn
canisterId = ""

async def icpcon(metode, item1=None):
    global er_data, received_conn, received_title, received_conector
    param_chip = [{'type': Types.Text, 'value': item1}]

    ic_url = 'https://ic0.app'
    client = Client(url=ic_url)
    identity = load_identity_from_pem(private_key_pem)
    agent = Agent(identity, client)

    try:

        if metode == 'chip':
            
            result = await agent.query_raw_async(canisterId, "chip", encode(param_chip))

            if isinstance(result, list) and len(result) > 0:
                first_element = result[0]

                if isinstance(first_element, dict) and 'value' in first_element:
                    result_nice = first_element['value']
                    print("raport : " + result_nice)
                    return result_nice
                else:
                    print("Data error")
                    return "dupa"
            else:
                print("Data error")
                return "dupa"

        if metode == 'chip_up':
            
            result = await agent.update_raw_async(canisterId, "chip_up", encode(param_chip))

            if isinstance(result, list) and len(result) > 0:
                first_element = result[0]

                if isinstance(first_element, dict) and 'value' in first_element:
                    result_nice = first_element['value']
                    print("raport : " + result_nice)
                    return result_nice
                else:
                    print("Data error")
                    return "dupa"
            else:
                print("Data error")
                return "dupa"

        
        return "dupa"
    except Exception as e:
        print(f'Error: {e} ')
        er_data = True
        return "dupa"

async def chip(input, canister):
    global canisterId
    canisterId = canister
    response = await icpcon("chip", input)
    return response 

async def chip_up(input, canister):
    global canisterId
    canisterId = canister
    response = await icpcon("chip_up", input)
    return response 

