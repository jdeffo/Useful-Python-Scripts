#! /usr/bin/env python3

import sys, os, shutil
from paramiko import SSHClient
from scp import SCPClient
from tqdm import *

#Dictionary of servers
servers = {
    'Web' : "root@45.55.58.148",
    #'Web' : 'jdeffo.com',
}
#Dictionary of server folder paths
server_paths = {
    'Web' : "../var/www/html/",
}
#Dictionary of local folder paths
local_paths = {
    'Web' : "/Users/jeremydefossett/Source/Repos/JDeffo-Web/",
}

#Take in args
if len(sys.argv) < 3:
    print("Usage: Python V1.py [Server] [Password]")
    sys.exit()

server_arg = sys.argv[1]
password = sys.argv[2]

#Server
server = servers[server_arg]
print(server)
#Copy/Put paths
folder_path = local_paths[server_arg]
copy_path = server_paths[server_arg]

#SSH Transfer
ssh = SSHClient()
ssh.load_system_host_keys(os.path.expanduser(os.path.join("~", ".ssh", "known_hosts")))
ssh.connect(hostname="45.55.58.148", port=22, username="root", password=password)
sftp = ssh.open_sftp()

#SCP
scp = SCPClient(ssh.get_transport())

#Files Transferred
count = 0

print("Path: " + folder_path)

#Copy local files
for dir_name, sub_dir_name, file_list in tqdm(os.walk(folder_path)):
    print("--START--\n")
    if('.git' in dir_name):
        print("Skipped: " + sub_folder)
    elif('Depricated' in dir_name):
        print("Skipped: " + sub_folder)
    else:
        #Set put path
        print(dir_name)
        print('\n')
        #dest = copy_path + dir_name.replace(copy_path, '//')
        sub_folder = dir_name.split("JDeffo-Web/")[-1]
        print(sub_folder)
        #dest = copy_path + sub_folder + "/"
        dest = copy_path + sub_folder
        print("Destination: " + dest)

        for fname in file_list:
            if (dir_name[-1] != '/'):
                dir_name += '/'
            local_dir = dir_name + fname
            print("Local put: " + local_dir)
            if (dest[-1] != '/'):
                dest += '/'
            server_dir = dest + fname
            print("Server put: " + server_dir)
            #Put file on server
            sftp.put(local_dir, server_dir)
            count = count + 1

print(str(count) + " files were transferred to " + server_arg)
sftp.close()
ssh.close()
