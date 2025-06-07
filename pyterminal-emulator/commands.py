import os
import subprocess
import shutil
import stat
import platform
import pycurl
import shlex
import tarfile
import gzip
import shutil
import zipfile
import sys
import requests
from io import BytesIO

#inp is input
#rootuser is username
#user is username
#role is root/guest
#path is location where a work is done
#basepath is a path where th program cannot exit

#COLORS
BLUE = "\033[34m"
RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"

def inp(path="C:\\", basepath="C:\\", role="guest", user="VM"):
    if path == basepath:
        pat = "~"
    else:
        lb = len(basepath)
        pat = path[lb:]
    if basepath not in path:
        path = basepath

    if role == "root":
        print(f"{BLUE}┌──({RED}root㉿{user}{BLUE})-[{RESET}{pat}{BLUE}]")
        return input(f"{BLUE}└─{RED}# {RESET}").strip()
    else:
        print(f"{GREEN}┌──({BLUE}guest㉿{user}{GREEN})-[{RESET}{pat}{GREEN}]")
        return input(f"{GREEN}└─{BLUE}$ {RESET}").strip()
        


def fullexit():
    exit

def exit():
    print("Exiting terminal...\n")
    role= "guest"
    user= "vm"
    return role,user

    
def sudo(password="kali",rootuser="kali"):
    attemp=0
    while True:
        password = input("[sudo] password for vm: ")
        if "kali" == password:
            role="root"
            user=rootuser
            break
        else:
            attemp+=1
            if attemp == 3:
                print("sudo: 3 incorrect password attempts\n")
                break
            print("Sorry, try again.")
            continue
    return role,user




def ls(path,execution="simulate.py"):
    try:
        for i in os.listdir(path):
            if i==execution:    #execution of main file
                continue
            if "." not in i:
                print(f"{BLUE}{i}{RESET}",end="  ")
            else:
                print(i,end=" ")
        print("\n")
    except Exception as e:
         print("Error:", e,"\n:")


def cd(inp, path, basepath="C:\\"):
    _, new_dir = inp.split(" ", 1)
    if "../" in new_dir:
        up_levels = new_dir.count("../")
        for _ in range(up_levels):
            if path != basepath:
                path = os.path.dirname(path)
        new_dir = new_dir.replace("../", "")
    if ".." in new_dir:
        if path != basepath:
            path = os.path.dirname(path)
        new_dir = new_dir.replace("..", "")
    if new_dir.strip() != "":
        new_path = os.path.join(path, new_dir)
    else:
        new_path = path
    if os.path.isdir(new_path):
        return new_path
    else:
        print("Directory does not exist\n")
        return path

def cdonly(basepath="C:\\"):
    path= basepath
    return path

def cp(inp, path):
    parts = inp.split()
    if len(parts) < 3:
        print("Usage: cp <source> <destination>")
        return
    src = os.path.join(path, parts[1])
    dest = os.path.join(path, parts[2])
    try:
        if os.path.isdir(src):
            shutil.copytree(src, dest)
        else:
            shutil.copy2(src, dest)
        print(f"Copied {parts[1]} to {parts[2]}\n")
    except Exception as e:
        print(f"Error: {e}\n")

def mv(inp, path):
    parts = inp.split()
    if len(parts) < 3:
        print("Usage: mv <source> <destination>\n")
        return
    src = os.path.join(path, parts[1])
    dest = os.path.join(path, parts[2])
    try:
        shutil.move(src, dest)
        print(f"Moved {parts[1]} to {parts[2]}\n")
    except Exception as e:
        print(f"Error: {e}\n")


def touch(inp, path):
    parts = inp.split()
    if len(parts) < 2:
        print("Usage: touch <filename>\n")
        return
    file_path = os.path.join(path, parts[1])
    try:
        with open(file_path, 'a'):
            os.utime(file_path, None)
        print(f"Touched {parts[1]}\n")
    except Exception as e:
        print(f"Error: {e}\n")


def head(inp, path):
    parts = inp.split()
    if len(parts) < 2:
        print("Usage: head <filename> [-n <lines>]\n")
        return
    filename = parts[1]
    lines = 10
    if "-n" in parts:
        lines = int(parts[parts.index("-n")+1])
    try:
        with open(os.path.join(path, filename), 'r') as f:
            for i in range(lines):
                print(f.readline(), end='')
            print()
    except Exception as e:
        print(f"Error: {e}\n")


def tail(inp, path):
    parts = inp.split()
    if len(parts) < 2:
        print("Usage: tail <filename> [-n <lines>]\n")
        return
    filename = parts[1]
    lines = 10
    if "-n" in parts:
        lines = int(parts[parts.index("-n")+1])
    try:
        with open(os.path.join(path, filename), 'r') as f:
            content = f.readlines()
            print(''.join(content[-lines:]))
    except Exception as e:
        print(f"Error: {e}\n")

def ln(inp, path):
    parts = inp.split()
    if len(parts) < 3 or parts[1] != "-s":
        print("Usage: ln -s <target> <link_name>\n")
        return
    target = os.path.join(path, parts[2])
    link_name = os.path.join(path, parts[3])
    try:
        os.symlink(target, link_name)
        print(f"Symbolic link created: {link_name} -> {target}\n")
    except Exception as e:
        print(f"Error: {e}")


def find(inp, path):
    parts = inp.split()
    if len(parts) < 2:
        print("Usage: find <name>\n")
        return
    name = parts[1]
    for root, dirs, files in os.walk(path):
        if name in files or name in dirs:
            print(os.path.join(root, name))
    print()
    
def cat(inp, path):
    parts = inp.split()
    if len(parts) != 2:
        print("Usage: cat <file.txt>\n")
        return
    file_path = os.path.join(path, parts[1])
    if os.path.isfile(file_path):
        with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
            print(f.read())
    else:
        print("File not found\n")

def chmod(inp, path):
    parts = inp.split()
    if len(parts) != 3:
        print("Usage: chmod [±rwx] <filename>\n")
        return

    mode, filename = parts[1], parts[2]
    full_path = os.path.join(path, filename)

    if not os.path.exists(full_path):
        print("No such file or directory\n")
        return

    try:
        current_permissions = os.stat(full_path).st_mode
        for flag in mode:
            if flag == '+':
                action = 'add'
            elif flag == '-':
                action = 'remove'
            elif flag == 'r':
                current_permissions = (
                    current_permissions | stat.S_IREAD
                    if action == 'add'
                    else current_permissions & ~stat.S_IREAD
                )
            elif flag == 'w':
                current_permissions = (
                    current_permissions | stat.S_IWRITE
                    if action == 'add'
                    else current_permissions & ~stat.S_IWRITE
                )
            elif flag == 'x':
                current_permissions = (
                    current_permissions | stat.S_IEXEC
                    if action == 'add'
                    else current_permissions & ~stat.S_IEXEC
                )
        os.chmod(full_path, current_permissions)
        print(f"Permissions updated: {mode} applied to {filename}\n")
    except Exception as e:
        print("Error:", e, "\n")  

def mkdir(inp,path):
    
    try:
        _, dirname = inp.split(" ", 1)
        os.mkdir(os.path.join(path, dirname))
        print(f"Directory '{dirname}' created.\n")
    except FileExistsError:
        print("Directory already exists.\n")
    except Exception as e:
        print("Error:", e)
        print("Usage: mkdir <directory_name>\n")
        
def rm(inp,path):
    parts = inp.split()
    if len(parts) >= 2:
        target = parts[-1]
        full_path = os.path.join(path, target)

        def remove_readonly(func, path, _):
            os.chmod(path, stat.S_IWRITE)
            func(path)

        if not os.path.exists(full_path):
            print("No such file or directory\n")

        try:
            if "-rf" in parts:
                shutil.rmtree(full_path, onerror=remove_readonly)
                print(f"Deleted directory: {target}\n")
            elif os.path.isdir(full_path):
                os.rmdir(full_path)
                print(f"Deleted empty directory: {target}\n")
            else:
                os.remove(full_path)
                print(f"Deleted file: {target}\n")
        except Exception as e:
            print("Error: an error occured during process\n")
    else:
        print("Usage: rm [-rf] <file-or-folder>\n")




def pwd(path,basepath="C:\\"):
    i=len(basepath)
    if path[i-1]== "\\":
        i+=1
    print("C:\\",path[i:],"\n",sep="")

def whoami(role="guest",user="VM"):
    print(role,"/",user,"\n",sep="")




def ifconfig():
    try:
        result = subprocess.run("ipconfig", capture_output=True, text=True, shell=True)
        print(result.stdout)
        if result.stderr:
            print("Error:", result.stderr)
    except Exception as e:
        print("Failed to fetch network info:", e, "\n")

def ping(inp):
    parts = inp.split()
    if len(parts) >= 2:
            target = parts[1]
            count = "4"  # default
            if len(parts) == 3 and parts[2].isdigit():
                count = parts[2]
            try:
                cmd = ["ping", "-n" if platform.system() == "Windows" else "-c", count, target]

                kwargs = {
                    "capture_output": True,
                    "text": True
                }

                if platform.system() == "Windows":
                    kwargs["creationflags"] = subprocess.CREATE_NO_WINDOW

                result = subprocess.run(cmd, **kwargs)

                print(result.stdout)
                if result.stderr:
                    print(result.stderr)
            except Exception as e:
                print("Error running ping:", e)
    else:
        print("Usage: ping <host> [count]")

def curl(inp):
    parts = shlex.split(inp)
    if len(parts) < 2 or parts[0] != "curl":
        print("Invalid curl command.")
        return

    buffer = BytesIO()
    c = pycurl.Curl()
    headers = []

    url = None
    method = "GET"
    data = None
    user = None
    user_agent = None
    cookie = None

    i = 1
    while i < len(parts):
        arg = parts[i]

        if arg == "-X":
            method = parts[i + 1]
            i += 1
        elif arg in ("--data", "-d"):
            data = parts[i + 1]
            i += 1
        elif arg == "-H":
            headers.append(parts[i + 1])
            i += 1
        elif arg == "-u":
            user = parts[i + 1]
            i += 1
        elif arg == "-A":
            user_agent = parts[i + 1]
            i += 1
        elif arg == "--cookie":
            cookie = parts[i + 1]
            i += 1
        elif not arg.startswith("-"):
            url = arg
        i += 1

    if not url:
        print("No URL specified.")
        return

    c.setopt(c.URL, url)
    c.setopt(c.WRITEDATA, buffer)

    if method != "GET":
        c.setopt(c.CUSTOMREQUEST, method)

    if data:
        c.setopt(c.POSTFIELDS, data)

    if headers:
        c.setopt(c.HTTPHEADER, headers)

    if user:
        c.setopt(c.USERPWD, user)

    if user_agent:
        c.setopt(c.USERAGENT, user_agent)

    if cookie:
        c.setopt(c.COOKIE, cookie)

    try:
        c.perform()
        print(buffer.getvalue().decode("utf-8"))
    except pycurl.error as e:
        print("Curl error:", e)
    finally:
        c.close()
 
def parse_wget_args(args):
    options = {
        'url': None,
        'output': None,
        'no_check_cert': False
    }
    skip = False
    for i, arg in enumerate(args):
        if skip:
            skip = False
            continue
        if arg == '--no-check-certificate':
            options['no_check_cert'] = True
        elif arg == '-O' and i + 1 < len(args):
            options['output'] = args[i + 1]
            skip = True
        elif not arg.startswith('-'):
            options['url'] = arg
    return options

def wget(inp, path):
    args = inp.split()[1:]
    opts = parse_wget_args(args)

    if not opts['url']:
        print("Usage: wget [--no-check-certificate] [-O output_file] <url>\n")
        return

    filename = opts['output'] or opts['url'].split('/')[-1]
    filepath = os.path.join(path, filename)

    try:
        print(f"Downloading: {filename}")
        with requests.get(opts['url'], stream=True, verify=not opts['no_check_cert']) as r:
            r.raise_for_status()
            total = int(r.headers.get('content-length', 0))
            downloaded = 0
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(8192):
                    f.write(chunk)
                    downloaded += len(chunk)
                    percent = int(downloaded * 100 / total) if total else 100
                    print(f"\rProgress: {percent}%", end="")
        print(f"\nDownloaded to: {filename}\n")
    except Exception as e:
        print("Download failed:", e, "\n")

 
def git(inp):
    if not inp.startswith("git "):
        print("Not a git command.")
        return

    try:
        result = subprocess.run(inp, shell=True, capture_output=True, text=True)
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(result.stderr)
        if not result.stdout and not result.stderr:
            print("Command executed.")
    except Exception as e:
        print("Error:", e)



def bash(inp, path):
    parts = inp.split()
    if len(parts) != 2:
        print("Usage: bash <script.sh>\n")
        return
    script_path = os.path.join(path, parts[1])
    if os.path.isfile(script_path) and script_path.endswith(".sh"):
        try:
            subprocess.run(["bash", script_path], check=True)
        except subprocess.CalledProcessError as e:
            print("Script error:", e, "\n")
    else:
        print("Shell script not found\n")

def python(inp, path):
    

    try:
        _, file = inp.split(" ", 1)
        script_path = os.path.join(path, file)
        if not os.path.isfile(script_path):
            print(f"File not found: {file}\n")
            return
        result = subprocess.run(
            ["python", script_path],
            capture_output=True,
            text=True
        )
        print(result.stdout)
        if result.stderr:
            print(result.stderr)
    except Exception as e:
        print(f"Error: {e}\n")
       

    
def tar(inp, path):
    parts = inp.split()
    if len(parts) < 3:
        print("Usage: tar -[cxf] <archive.tar> [files...]")
        return

    flag = parts[1]
    archive_path = os.path.join(path, parts[2])

    try:
        if flag == "-cf":  # Create archive
            with tarfile.open(archive_path, "w") as tarf:
                for file in parts[3:]:
                    tarf.add(os.path.join(path, file), arcname=file)
            print(f"Created archive: {parts[2]}")

        elif flag == "-xf":  # Extract archive
            with tarfile.open(archive_path, "r") as tarf:
                tarf.extractall(path)
            print(f"Extracted archive: {parts[2]}")

        elif flag == "-tf":  # List archive contents
            with tarfile.open(archive_path, "r") as tarf:
                tarf.list()
        
        else:
            print("Unsupported flag. Use -cf, -xf, or -tf.")
    except Exception as e:
        print("Error:", e)


def gzip(inp, path):
    parts = inp.split()
    if len(parts) != 2:
        print("Usage: gzip <file>")
        return

    original_file = os.path.join(path, parts[1])
    compressed_file = original_file + ".gz"

    if not os.path.exists(original_file):
        print(f"No such file: {parts[1]}")
        return

    try:
        with open(original_file, 'rb') as f_in:
            with gzip.open(compressed_file, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)
        os.remove(original_file)  # Remove original (like Linux gzip)
        print(f"Compressed: {parts[1]} -> {parts[1]}.gz")
    except Exception as e:
        print(f"Error compressing file: {e}")


def zip(inp, path):
    parts = inp.split()
    if len(parts) < 3:
        print("Usage: zip <archive.zip> <file1> <file2> ...")
        return

    archive = os.path.join(path, parts[1])
    try:
        with zipfile.ZipFile(archive, 'w') as zipf:
            for f in parts[2:]:
                full_path = os.path.join(path, f)
                zipf.write(full_path, arcname=f)
        print(f"Created zip archive: {parts[1]}")
    except Exception as e:
        print("Error:", e)




def noroot():
    print("No root permissions\n")

def clear():
    os.system('cls' if os.name == 'nt' else 'clear')

def nocommand(inp):
    print(f"{inp}: Command not found\n")
