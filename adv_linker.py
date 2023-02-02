import os
import sys
import json
import argparse
import subprocess

USERPROFILE = os.environ['USERPROFILE']

with open(f"{USERPROFILE}\\Desktop\\linking\\app_path.json", "r") as f:
    app_path_dict = json.load(f)

with open(f"{USERPROFILE}\\Desktop\\linking\\mapping.db", "r") as f:
    data = f.read()
    # 복호화 프로세스

data = json.loads(data.replace("'",'"'))    
mapping_dict = data['mapping_table']
rainbow_table = data['rainbow_table']

def ext2app(ext):
    for app in app_path_dict.keys():
        if ext in app_path_dict[app]['ext']:
            return app_path_dict[app]['path']

    return ""

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Super Simple Argument Parsing",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    parser.add_argument('--name', required=True)

    args = parser.parse_args()

    if len(sys.argv) != 3 :
        print("Usage: ./linking.py --name [File Hash Name]")
        sys.exit()

    h_name = args.name
    hidden_name = rainbow_table[h_name]
    ext = mapping_dict[hidden_name].split('.')[-1]
    app = ext2app(ext)

    if ext in app_path_dict['photo']['ext']:
        # cmd = 'C:\\Windows\\system32\\rundll32.exe "C:\\Program Files\\Windows Photo Viewer\\PhotoViewer.dll", ImageView_Fullscreen '
        cmd = f'{app} {app_path_dict["photo"]["arg"]} {hidden_name}'
    else:
        cmd = [f'{app}', f'{hidden_name}']

    subprocess.Popen(cmd)
    # print(cmd)
    # os.system(cmd)
    



