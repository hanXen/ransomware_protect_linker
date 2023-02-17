import os
import sys
import getpass
from aes import AESCipher

if getattr(sys, 'frozen', False):
    file_path = sys.executable
    file_name = file_path.split("\\")[-1]
    DIR_PATH = file_path.split(f"\\dist\\{file_name}")[0]
else:
    file_path = os.path.abspath(__file__)
    file_name = file_path.split("\\")[-1]
    DIR_PATH = file_path.split(f"\\{file_name}")[0]

aes = AESCipher()

with open(f"{DIR_PATH}\\db\\mapping.db", "r") as f:
    data = f.read()
    
pw = getpass.getpass("Enter PASSWORD : ")
pw2 = getpass.getpass("Convfirm PASSWORD : ")
if not pw or pw != pw2:
    print("[-] PASSWORD ERROR")
    sys.exit()

data = aes.encrypt(data, pw)
with open(f"{DIR_PATH}\\db\\enc_mapping.dll", "w") as f:
    f.write(data)

with open(f"{DIR_PATH}\\db\\app_path.json", "r") as f:
    data = f.read()

with open(f"{DIR_PATH}\\db\\app_path.dll", "w") as f:
    f.write(data)
    
# os.remove(f"{DIR_PATH}\\db\\mapping.db")
# os.remove(f"{DIR_PATH}\\db\\app_path.json")
        
    
