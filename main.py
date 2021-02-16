#!./venv/bin/python
import os
from time import sleep
from datetime import datetime

import vcgencmd as vc
import requests
from dotenv import load_dotenv

LOG = 'logs/health.log'
load_dotenv(override=True)
BOSS_ID = os.getenv('BOSS_ID')
TGRAM_TOKEN = os.getenv('TGRAM_TOKEN')
WARNING_TEMP = int(os.getenv('WARNING_TEMP', 50))
CRITICAL_TEMP = int(os.getenv('CRITICAL_TEMP', 60))
IDLE_SLEEP = int(os.getenv('IDLE_SLEEP', 60))
WARNING_SLEEP = int(os.getenv('WARNING_SLEEP', 30))
CRITICAL_SLEEP = int(os.getenv('CRITICAL_SLEEP', 15))

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

            if temp > CRITICAL_TEMP:
                tts = CRITICAL_SLEEP
                if temp > last_temp:
                    log(f'CRITICAL TEMP: {temp}')

            elif temp > WARNING_TEMP:
                tts = WARNING_SLEEP
                if temp > last_temp or last_temp > CRITICAL_TEMP:
                    log(f'WARNING TEMP: {temp}')

            else:
                tts = IDLE_SLEEP
                if last_temp > WARNING_TEMP or not last_temp:
                    log(f'IDLE TEMP: {temp}')

            last_temp = temp
            sleep(tts)
    except Exception as exc:
        log(exc)

if __name__ == '__main__':
    main()
