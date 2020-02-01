import os
import paramiko

class SSHClient:
    def __init__(self):
        self.ssh = paramiko.SSHClient

    def open_connection(self, hostname, username, pswd):
        self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(hostname=hostname, username=username, password=pswd)

    def send_file(self, localpath, remotepath):
        sftp = self.ssh.open_sftp()
        sftp.put(localpath, remotepath)
        sftp.close()
        return

    def close_connection(self):
        self.ssh.close()
        return

'''  
def ssh_send_file(localpath, remotepath, username, password):
    ssh = paramiko.SSHClient()

    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname='piDepot01.local', username=username, password=password)
    sftp = ssh.open_sftp()
    sftp.put(localpath, remotepath)
    sftp.close()
    ssh.close()
    return
'''
#local_file = r'/home/pi/Desktop/test.txt'
#remote_path = r'/home/pi/Desktop/test.txt'
#ssh_send_file(local_file, remote_path, 'pi', 'piDepot')