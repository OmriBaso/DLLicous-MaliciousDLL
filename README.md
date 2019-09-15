# DLLicous
**______________________________________________________________________________________________________________________________**

**A generator for malicious DLL files. Fast-Easy-Simple.**

**Usage**

Usage is pretty simple just run the script with Python3 or " .\DLLicous.py " 
and the script will prompt you for everything you need - make sure your specify the right payloads
for the target.

**Upcoming V2**

What's new in V2 Version ? (Not Released yet) 
As i said - V2 is for PT so I made my self a scenario where the organization has a firewall that blocks downloading executables.
and I had two options to solve that:
1. Write a reverse shell in C to the DLL
2. Base64encode and Decode the NC binary inside the DLL and write the ` nc.exe ` 
Inside the working directory of the DLL and launch the attack from there.
Another new feature in mind is:
having the base64 code of ` nc.exe ` also inside the DLL instead of downloading 
it from the web or copying it from the SMB server.

V2 will probably be released in the next month

**Credits**

Code was written by "J3wker" Aka Omri Baso.

Credits for the SMB Server used in the program goes to "SecureAuthCorp" 
