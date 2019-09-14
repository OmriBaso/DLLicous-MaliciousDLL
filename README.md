# DLLicous
A generator for malicious DLL files for DLL Hijacking attacks.

**Usage**

Usage is pretty simple just run the scripy with Python3 or " .\DLLicous.py " 

and the script will prompt you for everything you need

**DLL Hijacking**

DLL hijacking the process of taking adventage of the way windows load 

"Shared Libraries".

for example when a program or service runs and it requires

srrstr.dll and its trying to load it from

 ` C:\Users\example\AppData\Local\Microsoft\WindowsApps\srrstr.dll `
 
windows is looking for the dll FIRST in the woking directory of the executable

If it doesnt find it, I continues to the path specified and it iterates over 

every folder in the path looking for the DLL and try to load it.

for example placing the DLL in:

` C:\Users\example\srrstr.dll `

will cause it to be loaded!  

so we could use our malicous DLL to hijack the path and get a malicious code

execute the privileges of the user who ran the exeuteable!

how do we do that ?

we generate a payload using my script and then place it at the middle of the path

for example in 

` C:\Users\example\AppData\Local\Microsoft\srrstr.dll `
**IMPORTANT NOTICE!!** 

The DLL name has to be same as the DLL you are trying to replace and 

of course the DLL that the program is trying to load / looking for


**Credits**

Code was written by "J3wker" Aka Omri Baso.

Credits for the SMB Server used in the program goes to "SecureAuthCorp"
