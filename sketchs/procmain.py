#!/usr/bin/python3

import time
import subprocess
import json

if __name__ == "__main__":
    with open('data.json', 'w') as f:
        json.dump({'bps': 30},f)
    proc = subprocess.Popen(["python","sketchs/procsub.py"])
    print("proc:",proc)
    time.sleep(5)
    proc.kill()
    proc.terminate()