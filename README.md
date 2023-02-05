# ransomware_protect_linker
A Proof-of-Concept for avoid ransomware impact by camouflage & hiding files.

To access the hidden file, we utilize the link file(a.k.a. shortcuts) in Windows to solve the usablity issue.

This is the latest version for the deployment. (Applying Encrypted & camoyflaged DB / Adanced model / Right-Click Function ...)  
If you want to see the test code, check the ```src```. (non-encrypted DB / not-advanced model )  

## usage

### build
```bash
> pyinstaller -u -F enc_adv_linker.py
> pyinstaller -u -F hiding.py
> pyinstaller -F recovery.py
> Set-RightClick.bat (Run as Administrator)
```
### run
```bash
# Hide All Files (testbed Directory)
> hiding.exe -hide
# Hide File (or you can just rigt-click the file)
> hiding.exe --hidefile [filename]
# Recover All Files (testbed Directory)
> recovery.exe --recover
# Recover File (Extract) (or you can just rigt-click the file)
> recovery.exe --recoverfile
```
