#!./venv/bin/python
import sys
import os
import time
import vcgencmd as vc

IDLE = 40
WARNING = 45
CRITICAL = 50

def main():
    start_time = time.time()
    while True:
        temp = vc.measure_temp()
        clock = int(vc.measure_clock('arm')/1000000)
        print(f'{temp}, {clock}')

        if temp > CRITICAL:
            # send critical
            tts = 1
        elif temp > WARNING:
            tts = 3
            # send warning
        elif temp > IDLE or clock >= 1500:
            tts = 5
        else:
            tts = 10

        time.sleep(tts)

if __name__ == '__main__':
    main()
