from v_medium_newspaper import paint_text, np_print, paper_test
from ollama_core import evaluate
from v_chip import chip, chip_up
from time import sleep
import serial
import asyncio
import os
import signal
import sys
text1 = """"""
text2 = """"""
# tu zapisujesz swoje dyrektywy co do artykułuw 
fresh = ""

def paper_make():
    global text1, text2
    paint_text(text1, text2)
    np_print()

def import_text(text_add):
    global text1, text2
    if(len(text1) + len(text_add) <= 1500):
        if(len(text1)) != 0:
            text1 = text1 + "[endend]" + text_add
        else:
            text1 = text1 + text_add
    elif(len(text2) + len(text_add) <= 1500):
        if(len(text2)) != 0:
            text2 = text2 + "[endend]" + text_add
        else:
            text2 = text2 + text_add
    else:
        test = paper_test(text_add, text1, text2)
        if(test == "1_ok"):
            text1 = text1 + "[endend]" + text_add
        elif(test == "2_ok"):
            text2 = text2 + "[endend]" + text_add
        else:
            paper_make()
            text1 = text_add
            text2 = """"""

def raport_work(margin):
    global text1, text2
    os.system("clear")
    print("-----text1-----")
    print(text1)
    print("-----text2-----")
    print(text2)
    print("-----margin----")
    print(margin)

async def main(canister):
    margin_local = await chip("margin", canister)

    while True:
        chceck = await chip("margin", canister)
        while chceck == "dupa":
            chceck = await chip("margin", canister)
            
        if margin_local != chceck:
            texttext = await chip(margin_local, canister)
            while texttext == "dupa":
                texttext = await chip(margin_local, canister)
            
            if(evaluate( fresh + "[" + texttext + "]") == True):        
                import_text(texttext)
                print("text został przyjenty")
            else:
                print("text został odzucony ponieważ złamał dyrektywy \n lub model AI nie działa")
            margin_local = chceck
        await asyncio.sleep(5)
        sleep(10)
        raport_work(margin_local)
        

if __name__ == "__main__":
    asyncio.run(main("srfms-nqaaa-aaaah-qqipa-cai"))
