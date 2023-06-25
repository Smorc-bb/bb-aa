from random import choice, randint
from time import sleep
from threading import Thread 
from json import loads
from os import system
from ctypes import windll
try:
    import requests
except:
    system('pip install requests')
    import requests

clear = lambda: system('cls')
print('Telegram Channel - https://t.me/n4z4v0d & https://t.me/earlyberkut\n')
windll.kernel32.SetConsoleTitleW('Discord Bot | by NAZAVOD&EARLY BERKUT')

tokensfolder = str(input('TXT with tokens: '))
userdelay = str(input('Delay range before first message (example: 0-20): '))
userdelayint = userdelay.split('-')
with open(tokensfolder, 'r') as file:
    data = [token.strip() for token in file]

msg_set: list = open('msg.txt', 'r', encoding='utf-8').read().splitlines()
chat_id = int(input('Input chat id: '))
delay = int(input('Delay between messages in seconds: '))
clear()
def mainth(token, first_start):
    if first_start == True:
        session = requests.Session()
        session.headers['authorization'] = token
        first_start_sleeping = randint(int(userdelayint[0]),int(userdelayint[1]))
        print(f'First launch, sleeping {first_start_sleeping} sec')
        sleep(first_start_sleeping)
    while True:
        first_start = False
        try:
            msg = choice(msg_set)
            print(f'Sending message: {msg}')
            _data = {'content': str(msg), 'tts': False}
            r = session.post(
                f'https://discord.com/api/v9/channels/{chat_id}/messages', json=_data)
            if 'id' in loads(r.text):
                msg_id = loads(r.text)['id']
            elif 'message' in loads(r.text):
                errormsg = loads(r.text)['message']
                if 'retry_after' in loads(r.text):
                    timesleep = float(loads(r.text)['retry_after'])
                    print(f'Error: {errormsg}, sleeping {timesleep} sec')
                    sleep(timesleep)
                    mainth(token, first_start)
                else:
                    raise Exception(errormsg)
            else:
                raise Exception(r.text)
            print(f'Message sent')
            print(f'Sleeping {delay} seconds')
            sleep(delay)
        except Exception as error:
            print(f'Error: {str(error)}')
            pass

for _ in range(len(data)):
    while data:
        token = data.pop(0)
        first_start = True
        Thread(target=mainth, args=(token, first_start,)).start()