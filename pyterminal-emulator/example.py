from pyterminalx import commands as com

role= "guest"
user= "vm"
rootuser="user"
password="kali"
path = "C:\\"
basepath="C:\\"
lb=len(basepath)

com.clear()

while True:

    inp=com.inp(path,basepath,role,user)
    #exit
    if inp == "exit":
        role,user=com.exit()
        continue

    #Full Exit
    if inp == "full exit":
        com.clear()
        break

    #sudo su
    if inp == "sudo su":
        role,user=com.sudo(password,rootuser)
        continue

    #ls
    if inp == "ls":
        if role == "root":
            com.ls(path)
        else:
            com.noroot()
        continue

    #cd home
    if inp.startswith("cd "):
        if role == "root":
            if ":" in inp:
                continue
            path=com.cd(inp,path,basepath)
        else:
             com.noroot()
        continue

    #cd
    if inp == "cd":
        path=com.cdonly(basepath)
        continue
    
    # cp
    if inp.startswith("cp"):
        if role == "root":
            com.cp(inp, path)
        else:
            com.noroot()
        continue

    # mv
    if inp.startswith("mv"):
        if role == "root":
            com.mv(inp, path)
        else:
            com.noroot()
        continue

    # touch
    if inp.startswith("touch"):
        if role == "root":
            com.touch(inp, path)
        else:
            com.noroot()
        continue

    # head
    if inp.startswith("head"):
        if role == "root":
            com.head(inp, path)
        else:
            com.noroot()
        continue

    # tail
    if inp.startswith("tail"):
        if role == "root":
            com.tail(inp, path)
        else:
            com.noroot()
        continue

    # ln
    if inp.startswith("ln"):
        if role == "root":
            com.ln(inp, path)
        else:
            com.noroot()
        continue

    # find
    if inp.startswith("find"):
        if role == "root":
            com.find(inp, path)
        else:
            com.noroot()
        continue
    
    # chmod
    if inp.startswith("chmod"):
        if role == "root":
            com.chmod(inp, path)
        else:
            com.noroot()
        continue
        
     #mkdir
    if inp.startswith("mkdir"):
        if role == "root":
            com.mkdir(inp,path)
        else:
            com.noroot()
        continue
        
    # rm and rm -rf
    if inp.startswith("rm"):
        if role == "root":
            com.rm(inp,path)
        else:
            com.noroot()
        continue
    
    #pwd
    if inp == "pwd":
        if role == "root":
            com.pwd(path,basepath)
        else:
            com.noroot()
        continue

    #whoami
    if inp == "whoami":
        com.whoami(role,user)
        continue

    #ifconfig
    if inp == "ifconfig":
        if role == "root":
            com.ifconfig()
        else:
            com.noroot()
        continue

    # ping
    if inp.startswith("ping"):
        if role == "root":
            com.ping(inp)
        else:
            com.noroot()
        continue

    #curl
    if inp.startswith("curl"):
        if role == "root":
            com.curl(inp)
        else:
            com.noroot()
        continue
    
    #wget
    if inp.startswith("wget"):
        if role == "root":
            com.wget(inp, path)
        else:
            com.noroot()
        continue
    
    #git
    if inp.startswith("git"):
        if role == "root":
            com.git(inp)
        else:
            ux.noroot()
        continue

    
    #bash
    if inp.startswith("bash"):
        if role == "root":
            com.bash(inp, path)
        else:
            com.noroot()
        continue

    #python    
    if inp.startswith("python"):
        if role == "root":
            com.python(inp, path)
        else:
            com.noroot()
        continue
        
    #tar
    if inp.startswith("tar"):
        if role == "root":
            com.tar(inp, path)
        else:
            com.noroot()
        continue
    
    
    #gzip
    if inp.startswith("gzip"):
        if role == "root":
            com.gzip(inp, path)
        else:
            com.noroot()
        continue
    
    #cat
    if inp.startswith("cat"):
        if role == "root":
            com.cat(inp, path)
        else:
            com.noroot()
        continue

    #zip
    if inp.startswith("zip"):
        if role == "root":
            com.zip(inp, path)
        else:
            com.noroot()
        continue



    #clear
    if inp == "clear":
        com.clear()
        continue

    #blank
    if inp == "":
        continue
    
    com.nocommand(inp)
