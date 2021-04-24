#!/bin/python3
import os
import subprocess
import sys
import getpass

def update_system():
    os.system("yes|apt-get update")
    os.system("yes|apt-get upgrade")

if __name__ == '__main__':
    update_system()