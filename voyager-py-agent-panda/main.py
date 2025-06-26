# -- wszytko co potrzebne do obsługi icp achcetera poprostu te wszytkie importy skopiuj i wklej
# nie zapomni tylko zainstalować przez pip icpy jak byś nie wiedział komenda to
# pip install icpy   / w konsoli python
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

#voyager start point voyager_databox
canisterId = '5dgyf-maaaa-aaaab-aaeia-cai'

glue_array = []

# uproszczanie sobie życia innymi muwiąc robimy sobie fukcje do gadania z canistrem
async def icpcon(metode, item1):
    global er_data
    # tu jest typowe pierdu pierdu by komunikacja działała gitmajonez
    # na tym etapie kiedy gadasz z main-netem nic nie zmieniaj i bendzie dobrze
    # wykorzystuje natywną tosamość internetową
    ic_url = 'https://ic0.app'
    client = Client(url=ic_url)
    identity = Identity()
    agent = Agent(identity, client)

    # zmienna param przechowuje dane które chcemy przesłać na canister
    param_glue = [{'type': Types.Vec(Types.Text), 'value': glue_array}]
    param_qwery = [{'type': Types.Nat, 'value': item1}]
    
    try:
        if metode == 'glue':
            # tu jest powtórka z rozrywki wiec pomine tłumaczenia tego
            result = await agent.query_raw_async(canisterId, "glue_get", encode(param_glue))



            if isinstance(result, list) and len(result) > 0:
                first_element = result[0]

                if isinstance(first_element, dict) and 'value' in first_element:
                    result_nice = first_element['value']
                    print(f'raport: {result_nice}')
                    return result_nice
                else:
                    print("data error")
                    return None
            else:
                print("data error")
                return None

        if metode == 'gluePUSH':
            # tu jest powtórka z rozrywki wiec pomine tłumaczenia tego
            result = await agent.update_raw_async(canisterId, "glue_push", encode(param_glue))



            if isinstance(result, list) and len(result) > 0:
                first_element = result[0]

                if isinstance(first_element, dict) and 'value' in first_element:
                    result_nice = first_element['value']
                    print(f'raport: {result_nice}')
                    return result_nice
                else:
                    print("data error")
                    return None
            else:
                print("data error")
                return None


        return None
    except Exception as e:
        print(f'Error: {e} ')
        er_data = True
        return None
            

async def monitor():
# glue test 
    
    command = input("comand ready: ")
    if(command == "glue"):
        # glue test 
        glue_array.clear()
        print("glue multi text test")
        while True:
            user_input = input("> ")
            if user_input.strip().lower() == "push":
                break
            if user_input.strip():
                glue_array.append(user_input.strip())

        print(f"\go push {glue_array}\n")
        raport = await icpcon("glue", glue_array)
        if(raport == "PUSH"):
            raport = await icpcon("gluePUSH", glue_array)
      
        print(raport)

    elif(command == "target"):
        canisterId = input("wpisz canister usługi z n/ którą chcesz rozmawiać: ")
    
    elif(command == "help"):
        print("target: wybierz caniser z którym chcesz rozmawiać")
        print("glue: skorzystaj z interfejsu glue z wybranym targetem")
        print("")
        
    else:
        print("komenda nie obsługiwana")

    


if __name__ == '__main__':
    print("[the panda] naiprosztrzy agnet do voyagera")
    print("zyczymy miłej zabawy jak [nie wiesz] co robić")
    print("wpisz [help]")
    while True:
       asyncio.run(monitor())
