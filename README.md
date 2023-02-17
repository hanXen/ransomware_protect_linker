# ransomware_protect_linker
A Proof-of-Concept for avoid ransomware impact by camouflage & hide files.

The main idea is that the most of ransomwares don't encrypt the system files. (.exe, .dll ...)

To access the hidden file, we utilize the link file (a.k.a. shortcuts) in Windows to solve the usablity issue.

This is the latest version for the deployment.  
(Applying Encrypted & camouflaged DB / Adanced model / Right-Click Function ...)    
If you want to see the test code, check the ```src```. &nbsp;(default key based encrypted / non-encrypted DB , non-advanced model )  

[+] UPDATE: Applied password based encrypt, every function require password. (hide / recover / access file)

## usage

### requirements
```bash
> pip install pycryptodome
> pip install pywin32
```

### build
```bash
> ./init_db.py
> pyinstaller -F enc_adv_linker.py
> pyinstaller -F hiding.py
> pyinstaller -F recovery.py
> Set-RightClick.bat (Run as Administrator)
```
### run
```bash
# Hide All Files (testbed Directory) (Run as Administrator)
> hiding.exe -hide
# Hide File (or you can just rigt-click the file) (Run as Administrator)
> hiding.exe --hidefile [filename]
# Recover All Files (testbed Directory)
> recovery.exe --recover
# Recover File (Extract) (or you can just rigt-click the file)
> recovery.exe --recoverfile
```
