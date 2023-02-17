import os
import sys
import json
import string
import random
import win32com.client
import getpass
import argparse
import hashlib

# GET DEFAULT PATH
if getattr(sys, 'frozen', False):
    file_path = sys.executable
    file_name = file_path.split("\\")[-1]
    DIR_PATH = file_path.split(f"\\dist\\{file_name}")[0]
else:
    file_path = os.path.abspath(__file__)
    file_name = file_path.split("\\")[-1]
    DIR_PATH = file_path.split(f"\\src\\{file_name}")[0]

with open(f"{DIR_PATH}\\src\\app_path.json", "r") as f:
    app_path_dict = json.load(f)

with open(f"{DIR_PATH}\\src\\mapping.db", "r") as f:
    data = f.read()

data = json.loads(data.replace("'",'"'))    
hidden_ext_list = data['hidden_ext']
hidden_dir_dict = data['hidden_dir']
mapping_dict = data['mapping_table']
RECOVERY_PASS = data['recovery_pass']
hash_table = data['hash_table']

target_ext_list = []
ext_icon_dict = {}

def preprocessing():
    for key in list(hidden_dir_dict.keys()):
        if not os.path.exists(hidden_dir_dict[key]):
            print(f"[-] {key} doesn't exists.")
            del hidden_dir_dict[key]

    for key in list(app_path_dict.keys()):
        if not os.path.exists(app_path_dict[key]['path']):
            print(f"[-] {key} doesn't exists.")
            del app_path_dict[key]

    for app in app_path_dict.values():
        for ext in app['ext']:
            target_ext_list.append(ext) 
            ext_icon_dict[ext] = f"{DIR_PATH}\\icon\\{app['ico']}"
    print(f"[*] Supported Extension: {target_ext_list}")

def postprocessing():
    data['mapping_table'] = mapping_dict
    data['hash_table'] = hash_table
    with open(f"{DIR_PATH}\\db\\mapping.db", "w") as f:
        json.dump(data, f)

def ext2app(ext):
    for app in app_path_dict.keys():
        if ext in app_path_dict[app]['ext']:
            return app_path_dict[app]['path']

    return ""

def name_gen(len=8):
    name = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(len))
    ext = random.choice(hidden_ext_list)

    return f"{name}.{ext}"

def hash_name(name):
    sha = hashlib.new('sha1')
    sha.update(name.encode())
    
    return sha.hexdigest()

def make_shortcuts(file):
    ext = file.split(".")[-1].lower()
    if ext not in target_ext_list:
        return
    app_path = ext2app(ext)
    if not app_path:        
        return
    new_name = name_gen()
    hidden_file = f"{hidden_dir_dict['help']}\\{new_name}"
    shortcut_path = f"{file}.lnk"
    h_name = hash_name(hidden_file)
    try:
        os.rename(file, hidden_file)
        shell = win32com.client.Dispatch("WScript.Shell")
        shortcut = shell.CreateShortcut(shortcut_path)
        # Open with Python (FOR TEST)
        '''
        shortcut.Targetpath = 'python'
        shortcut.Arguments = f'"{DIR_PATH}\\adv_linker.py" --name {h_name}'
        '''
        # Open with execute file (FOR DIST)
        shortcut.Targetpath = f'{DIR_PATH}\\dist\\adv_linker.exe'
        shortcut.Arguments = f'--name {h_name}'
        shortcut.IconLocation = ext_icon_dict[ext]
        shortcut.Save()
        mapping_dict[hidden_file] = file
        hash_table[h_name] = hidden_file
        target_list.append(hidden_file)
        # print(f"[+] {file} => {hidden_file}")
    except:
        print(f"[-] {file} hiding fali :(")


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

def sychronize(target_list):
    for hidden_file in target_list:
        shortcut_path = f'{mapping_dict[hidden_file]}.lnk'
        file_st = os.stat(hidden_file)
        os.utime(shortcut_path,(file_st.st_atime,file_st.st_mtime))
        
def auth():
    pass_in = getpass.getpass("PASSWORD? : ")
    if pass_in == RECOVERY_PASS:
        return True
    return False

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--hide', required=False, action='store_true')
    parser.add_argument('--hidefile', required=False, type=str, help='File Path')
    parser.add_argument('--recover', required=False, action='store_true')
    parser.add_argument('--recoverfile', required=False, type=str, help='File Path')
    args = parser.parse_args()

    if len(sys.argv) != 2 and len(sys.argv) != 3:
        print("Usage: ./linking.py [option] ([arg])")
        sys.exit()

    preprocessing()
    
    target_list = []
    if args.hide:
        target_path = f"{DIR_PATH}\\testbed"
        file_list = os.listdir(target_path)
        for file in file_list:
            make_shortcuts(f"{target_path}\\{file}")
        postprocessing()
        sychronize(target_list)

    elif args.hidefile:
        make_shortcuts(args.hidefile)
        postprocessing()
        sychronize(target_list)

    elif args.recover:
        if not auth():
            print("[-] PASSWORD failed :(")
            sys.exit()
        for hidden_file in list(mapping_dict):
            recovery(hidden_file)
        postprocessing()

    elif args.recoverfile:
        if not auth():
            print("[-] PASSWORD failed :(")
            sys.exit()
        hidden_file = hash_table[args.recoverfile]
        recovery(hidden_file)
        postprocessing()


