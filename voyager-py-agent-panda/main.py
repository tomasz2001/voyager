import asyncio
from time import sleep
from ic.client import Client
from ic.identity import Identity
from ic.agent import Agent
from ic.candid import encode, Types
# import serial
import subprocess
import os
import signal


er_data = False


canisterId = 'p2137-cai'

glue_array = []

received_conn = ""
received_title = ""
received_conector = []


async def icpcon(metode, item1):
    global er_data, received_conn, received_title, received_conector
   
    ic_url = 'https://ic0.app'
    client = Client(url=ic_url)
    identity = Identity()
    agent = Agent(identity, client)

    
    
    
    
    try:
        if metode == 'glue':
            param_glue = [{'type': Types.Vec(Types.Text), 'value': glue_array}]
            # tu jest powtórka z rozrywki wiec pomine tłumaczenia tego
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
                result = await agent.query_raw_async(canisterId, "hwoisme", encode(param_query))
            elif metode == 'getbox':
                param_query = [{'type': Types.Nat, 'value': int(item1)}]
                result = await agent.query_raw_async(canisterId, "hwoisme", encode(param_query))
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
                            received_conn = str(values[0]) if isinstance(values[0], str) else ''
                            received_title = str(values[1]) if isinstance(values[1], str) else ''
                            received_conector = values[2] if isinstance(values[2], list) else []
                        else:
                            received_conn = ''
                            received_title = ''
                            received_conector = []

                        #print(f'Odebrano strukturę Conn:')
                        #print(f'conn: {received_conn}')
                        #print(f'title: {received_title}')
                        #print(f'conector: {received_conector}')
                        
                        return {
                            'conn': received_conn,
                            'title': received_title,
                            'conector': received_conector
                        }

            return None

        return None
    except Exception as e:
        print(f'Error: {e} ')
        er_data = True
        return None
            

async def monitor():
    global canisterId, received_conn, received_title, received_conector
    command = input("comand ready: ")
    if(command == "glue"):
        # glue test 
        glue_array.clear()
        print("")
        while True:
            user_input = input("> ")
            if user_input.strip().lower() == "push":
                break
            if user_input.strip():
                glue_array.append(user_input.strip())

        
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
        raport = await icpcon("hwoisme", None)
        if raport:
            print("Dane Conn zostały pomyślnie odebrane:")
            print(f"received_conn: {received_conn}")
            print(f"received_title: {received_title}")  
            print(f"received_conector: {received_conector}")
        else:
            print("Nie udało się odebrać danych Conn")
            print("")
    
    elif(command == "help"):
        print("");
        if(canisterId == "p2137-cai"):
            print("")
            print("hwosime: sprawdzi z kim rozmawiasz i jakie ma interfejsy")
            print("target: wybierz caniser z którym chcesz rozmawiać")
            print("glue: skorzystaj z interfejsu glue z wybranym targetem")
            print("help: skorzystaj z pomocy")
        else:
            line = input("podaj strone pomocy tej usługi")
            raport = await icpcon("help", line)
            print(raport)
            print("")
    else:
        print("komenda nie obsługiwana")

    


if __name__ == '__main__':
    print("")
    print("[the panda] naiprosztrzy agnet do voyagera")
    print("zyczymy miłej zabawy jak [nie wiesz] co robić")
    print("wpisz [help]")
    while True:
       asyncio.run(monitor())
