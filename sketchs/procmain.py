#!/usr/bin/python3

import time
import subprocess

if __name__ == "__main__":
    proc = subprocess.Popen("python procsub.py",
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            shell=True)
    out, err = proc.communicate(input="insta\n".encode())