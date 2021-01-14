#!./venv/bin/python
import os
from time import sleep
from datetime import datetime

import vcgencmd as vc
import requests
from dotenv import load_dotenv

LOG = 'logs/health.log'
IDLE = 30  # tts
WARNING = (45, 15)  # temp, tts
CRITICAL = (50, 10)
load_dotenv(override=True)
BOSS_ID = os.getenv('BOSS_ID')
TGRAM_TOKEN = os.getenv('TGRAM_TOKEN')

def say2boss(text):
    if not BOSS_ID:
        return None
    url = f'https://api.telegram.org/bot{TGRAM_TOKEN}/sendMessage?chat_id={BOSS_ID}&parse_mode=Markdown&text={text}'
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json()
        else:
            raise Exception(f'status_code {response.status_code}')
    except Exception as Ex:
        print(Ex)
        return False

def log(text):
    with open(LOG, 'a') as file:
        file.write(f'{datetime.now().replace(microsecond=0).isoformat()} - {text}\n')
    say2boss(text)

def main():
    log('start')
    try:
        last_temp = 0
        while True:
            temp = vc.measure_temp()
            # clock = int(vc.measure_clock('arm')/1000000)
            # print(f'{temp}, {clock}')

            if temp > CRITICAL[0]:
                tts = CRITICAL[1]
                if temp > last_temp:
                    log(f'CRITICAL TEMP: {temp}')

            elif temp > WARNING[0]:
                tts = WARNING[1]
                if temp > last_temp or last_temp > CRITICAL[0]:
                    log(f'WARNING TEMP: {temp}')

            else:
                tts = IDLE
                if last_temp > WARNING[0] or not last_temp:
                    log(f'IDLE TEMP: {temp}')

            last_temp = temp
            sleep(tts)
    except Exception as exc:
        log(exc)

if __name__ == '__main__':
    main()
