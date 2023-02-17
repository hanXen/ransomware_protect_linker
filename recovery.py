import os
import sys
import json
import getpass
import argparse
import hashlib
from aes import AESCipher


# GET DEFAULT PATH
if getattr(sys, 'frozen', False):
    file_path = sys.executable
    file_name = file_path.split("\\")[-1]
    DIR_PATH = file_path.split(f"\\dist\\{file_name}")[0]
else:
    file_path = os.path.abspath(__file__)
    file_name = file_path.split("\\")[-1]
    DIR_PATH = file_path.split(f"\\{file_name}")[0]

aes = AESCipher()

with open(f"{DIR_PATH}\\db\\enc_mapping.dll", "r") as f:
    data = f.read()

while True:
    pw = getpass.getpass("PASSWORD? : ")
    try:
        data = aes.decrypt(data, pw)
        if 'hidden_ext' in data:
            break
    except:
        print("[-] PASSWORD Fail :(")

data = json.loads(data.replace("'",'"'))    
mapping_dict = data['mapping_table']
hash_table = data['hash_table']
    
target_ext_list = []
ext_icon_dict = {}

def postprocessing():
    global data
    data['mapping_table'] = mapping_dict
    data['hash_table'] = hash_table
    data = aes.encrypt(json.dumps(data), pw)
    with open(f"{DIR_PATH}\\db\\enc_mapping.dll", "w") as f:
        f.write(data)

def hash_name(name):
    sha = hashlib.new('sha1')
    sha.update(name.encode())
    
    return sha.hexdigest()

def recovery(hidden_file):
    cmd = ""
    try:
        file = mapping_dict[hidden_file]
        os.rename(hidden_file, file)
        if os.path.exists(f'{file}.lnk'):
            os.remove(f'{file}.lnk')
        del mapping_dict[hidden_file]
        del hash_table[hash_name(hidden_file)]
        # print(f"[+] {hidden_file} => {file}")
    except:
        print(f"[-] {hidden_file} recovery fali :(")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--recover', required=False, action='store_true')
    parser.add_argument('--recoverfile', required=False, type=str, help='File Path')
    args = parser.parse_args()

    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print("Usage: ./linking.py [option] ([arg])")
        sys.exit()

    print("[*] File Recovery : lnk File => original File")

    if args.recover:
        for hidden_file in list(mapping_dict):
            recovery(hidden_file)

    elif args.recoverfile:
        hidden_file = hash_table[args.recoverfile]
        recovery(hidden_file)
        
    postprocessing()
