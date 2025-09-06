import asyncio
from time import sleep
from ic.client import Client
from ic.identity import Identity
from ic.agent import Agent
from ic.candid import encode, Types
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519
from cryptography.hazmat.backends import default_backend
from golem_base_sdk import GenericBytes, GolemBaseClient

# import
import split
import subprocess
import os
import signal
import sys


# global value
identity_file = "identity.pem"



if os.path.exists(identity_file):
    with open(identity_file, "r") as f:
        private_key_pem = f.read().strip()
else:
    private_key_pem = ""

# Funkcja do generowania nowej tożsamości
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
        print(f"Nowa tożsamość zapisana do {identity_file}", flush=True)
        return pem_pkcs8
    except Exception as e:
        print(f"Błąd generowania tożsamości: {e}", flush=True)
        return None

# Funkcja do ładowania tożsamości
def load_identity_from_pem(pem_data):
    global private_key_pem
    try:
        if not pem_data or not pem_data.startswith("-----BEGIN PRIVATE KEY-----"):
            print("Brak klucza, generowanie nowej tożsamości...", flush=True)
            pem_data = generate_new_identity()
            if pem_data is None:
                return None
            private_key_pem = pem_data.strip()

        identity = Identity.from_pem(pem_data)
        #print("Tożsamość załadowana", flush=True)
        return identity
    except Exception as e:
        print(f"Błąd ładowania tożsamości: {e}", flush=True)
        return None


er_data = False


canisterId = 'p2137-cai'
glue_array = []

received_conn = ""
received_title = ""
received_conector = []

binfile = []

async def icpcon(metode, item1=None, item2=None, item3=None, item4=None, item5=None, item6=None, item7=None):
    global er_data, received_conn, received_title, received_conector
   
    ic_url = 'https://ic0.app'
    client = Client(url=ic_url)
    identity = load_identity_from_pem(private_key_pem)
    agent = Agent(identity, client)    
    
    try:

        if metode == 'file_one':
            param_file = [{'type': Types.Vec(Types.Text), 'value': glue_array}]
            result = await agent.query_raw_async(canisterId, "file_one", encode(param_file))


        if metode == 'glue':
            param_glue = [{'type': Types.Vec(Types.Text), 'value': glue_array}]
            result = await agent.query_raw_async(canisterId, "glue_get", encode(param_glue))


            if isinstance(result, list) and len(result) > 0:
                first_element = result[0]

                if isinstance(first_element, dict) and 'value' in first_element:
                    result_nice = first_element['value']
                    #print(f'raport: {result_nice}')
                    return result_nice
                else:
                    print("data error")
                    return None
            else:
                print("data error")
                return None

        
        if metode == 'gluePUSH':
            param_glue = [{'type': Types.Vec(Types.Text), 'value': glue_array}]
            
            result = await agent.update_raw_async(canisterId, "glue_push", encode(param_glue))



            if isinstance(result, list) and len(result) > 0:
                first_element = result[0]

                if isinstance(first_element, dict) and 'value' in first_element:
                    result_nice = first_element['value']
                    #print(f'raport: {result_nice}')
                    return result_nice
                else:
                    print("data error")
                    return None
            else:
                print("data error")
                return None


        if metode == 'help':
            param_query = [{'type': Types.Nat, 'value': int(item1)}]
            
            result = await agent.query_raw_async(canisterId, "help", encode(param_query))



            if isinstance(result, list) and len(result) > 0:
                first_element = result[0]

                if isinstance(first_element, dict) and 'value' in first_element:
                    result_nice = first_element['value']
                    #print(f'raport: {result_nice}')
                    return result_nice
                else:
                    print("data error")
                    return None
            else:
                print("data error")
                return None
        

        if metode == 'hwoisme' or metode == 'getapp' or metode == 'getbox':
            if metode == 'getapp':
                param_query = [{'type': Types.Nat, 'value': int(item1)}]
                result = await agent.query_raw_async(canisterId, "conn_one", encode(param_query))
            elif metode == 'getbox':
                param_query = [{'type': Types.Nat, 'value': int(item1)}]
                result = await agent.query_raw_async(canisterId, "frend_one", encode(param_query))
            else:
                param_query = []
                result = await agent.query_raw_async(canisterId, "hwoisme", encode(param_query))

            
            
            if isinstance(result, list) and len(result) > 0:
                first_element = result[0]
                #print(f"First element: {first_element}")
                
                if isinstance(first_element, dict) and 'value' in first_element:
                    conn_data = first_element['value']
                    #print(f"Conn data: {conn_data}")
                    #print(f"Conn data type: {type(conn_data)}")
                    #print(f"Conn data keys: {conn_data.keys() if isinstance(conn_data, dict) else 'Not dict'}")
                    
                    if isinstance(conn_data, dict):
                        global received_conn, received_title, received_conector
                        
                        
                        values = list(conn_data.values())

                        if len(values) >= 3:
                            received_title = str(values[0]) if isinstance(values[0], str) else ''
                            received_conn = str(values[1]) if isinstance(values[1], str) else ''
                            received_conector = values[2] if isinstance(values[2], list) else []
                        else:
                            return False
                        #print(f'Odebrano strukturę Conn:')
                        #print(f'conn: {received_conn}')
                        #print(f'title: {received_title}')
                        #print(f'conector: {received_conector}')
                        
                        return True

            return None

        return None
    except Exception as e:
        print(f'Error: {e} ')
        er_data = True
        return None

# dzdzownica funk code
async def vdz_golem_one(target):

    client = await GolemBaseClient.create_ro_client(
        "https://ethwarsaw.holesky.golemdb.io/rpc", 
        "wss://ethwarsaw.holesky.golemdb.io/rpc/ws"
    )
    get = (await client.get_storage_value(GenericBytes.from_hex_string(target)))
    await client.disconnect()
    return get

async def get_vd_by_index(index=0):
    
    client = await GolemBaseClient.create_ro_client(
        "https://ethwarsaw.holesky.golemdb.io/rpc", 
        "wss://ethwarsaw.holesky.golemdb.io/rpc/ws"
    )
    vd_entities = await client.query_entities('type="vd"')
    
    if index < 0 or index >= len(vd_entities):
        await client.disconnect()
        return None

    entity = vd_entities[index]

    
    target_hash = entity.entity_key

    await client.disconnect()
    return target_hash




async def monitor():
    global canisterId, received_conn, received_title, received_conector
    command = input("comand ready: ")
    if(command == "glue"):
        # glue test 
        glue_array.clear()
        print("Wpisz dane do tablicy, zatwierdzając każdą linię klawiszem Enter.")
        print("Gdy skończysz, wpisz '@push', aby wysłać tablicę.")
        print("Jeśli nie chcesz wysyłać, wpisz '@break'.")
        print("")
        while True:
            user_input = input("> ")
            if user_input.strip().lower() == "@push":
                break
            if user_input.strip().lower() == "@break":
                glue_array.clear()
                break
            glue_array.append(user_input)
            
                
        if user_input == "@break":
            raport = "Glue został złamany i nie został przesłany."
        else:
            raport = await icpcon("glue", glue_array)
            print("");
        
        if(raport == "PUSH"):
            raport = await icpcon("gluePUSH", glue_array)
            print(raport)
            print("")
            
        else:
            print(raport)
            print("")

    elif(command == "target"):
        print("")
        canisterId = input("wpisz canister usługi z n/ którą chcesz rozmawiać: ")

    elif(command == "hwoisme"):
        print("")
        raport = await icpcon("hwoisme")
        if raport == True:
            print("Dane Conn zostały pomyślnie odebrane:")
            print(f"received_conn: {received_conn}")
            print(f"received_title: {received_title}")  
            print(f"received_conector: {received_conector}")
        else:
            print("Nie udało się odebrać danych Conn")
            print("")

    elif(command == "getapp"):
        print("")
        get = input("podaj index: ")
        print("")
        raport = await icpcon("getapp", get)
        if raport == True:
            print("Dane Conn zostały pomyślnie odebrane:")
            print(f"received_conn: {received_conn}")
            print(f"received_title: {received_title}")  
            print(f"received_conector: {received_conector}")
        else:
            print("Nie udało się odebrać danych Conn")
            print("")

    elif(command == "getbox"):
        print("")
        get = input("podaj index: ")
        print("")
        raport = await icpcon("getbox", get)
        if raport == True:
            print("Dane Conn zostały pomyślnie odebrane:")
            print(f"received_conn: {received_conn}")
            print(f"received_title: {received_title}")  
            print(f"received_conector: {received_conector}")
        else:
            print("Nie udało się odebrać danych Conn")
            print("")
        
    elif(command == "help"):
        print("");
        if(canisterId == "p2137-cai" or canisterId == ""):
            print("")
            print("hwosime: sprawdzi z kim rozmawiasz i jakie ma interfejsy")
            print("target: wybierz caniser z którym chcesz rozmawiać")
            print("glue: skorzystaj z interfejsu glue z wybranym targetem")
            print("help: skorzystaj z pomocy")
            print("getbox: spytaj databox o inne databoxy")
            print("getapp: spytaj databox o aplikacje")
            print("vo-dz: fukcja dżdżownica aktualnie on-golem-DB")
        else:
            line = input("podaj strone pomocy tej usługi")
            raport = await icpcon("help", line)
            print(raport)
            print("")
    elif(command == "fileone"):
        print("fukcja fileone jest nadal w budowie")
        print("dzienkujemy za skorzystanie z usług panda_voyager_agnet")


    elif(command == "vo-dz"):
        target = input("wybierz-target lub wpisz auto: ")
        if(target == "auto"):
            index = input("podaj-index [liczba] szukaj: ")
            print("") 
            target = await get_vd_by_index(int(index))
            print("Target hash: ", target)
            print("")
        work = await vdz_golem_one(target)
        
        work = work.decode("utf-8")
        parts = work.split("/")

        a = parts[0]
        b = parts[1]  
        c = parts[2]
        if(a != "vd"):
            print("UWAGA! dane tu umieszczone mogą być nie poprawne lub uszkodzone")
        print("canister-databox-id: ", b)
        print("zdefiniowany poprzedni zapis: ", c)
        print("")
        while True:
            print("chcesz sprawdzić zdefiniowany wcześniejszy zapis: [tak/nie]")
            qwery = input("jeżeli chcesz już ustawić ten databox jako target napisz [target]: ")
            print("")
            if(qwery == "tak"):
                target = c
                work = await vdz_golem_one(target)
        
                work = work.decode("utf-8")
                parts = work.split("/")

                a = parts[0]
                b = parts[1]  
                c = parts[2]
                print("canister-databox-id: ", b)
                print("zdefiniowany poprzedni zapis hash: ", c)
                print("")
                
            elif(qwery == "target"):
                canisterId = b
                break
            else:
                break

    else:
        print("komenda nie obsługiwana")

    
if __name__ == '__main__':
    print("")
    print("")
    print("[the panda] naiprosztrzy agnet do voyagera")
    print("zyczymy miłej zabawy jak [nie wiesz] co robić")
    print("wpisz [help]")
    print("")
    print("")
    while True:
       asyncio.run(monitor())
