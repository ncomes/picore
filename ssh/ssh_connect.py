import os
import paramiko


def ssh_send_file(localpath, remotepath, username, password):
    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    #ssh.load_system_host_keys()
    #ssh.load_host_keys(os.path.expanduser(os.path.join('~', '.ssh', 'known_hosts')))
    ssh.connect(hostname='piDepot01.local', username=username, password=password)
    sftp = ssh.open_sftp()
    sftp.put(localpath, remotepath)
    sftp.close()
    ssh.close()
    return

local_file = r'/home/pi/Desktop/test.txt'
remote_path = r'/home/pi/Desktop/test.txt'
ssh_send_file(local_file, remote_path, 'pi', 'piDepot')