import subprocess

def ip_scan():
	for ping in range(26, 30):
		successful_ip = []
		address = "192.168.86." + str(ping)
		res = subprocess.call(['ping', '-c', '3', address])
		if res == 0:
			#print("ping to", address, "OK")
			successful_ip.append(address)
		elif res == 2:
		#	print("no response from", address)
			successful_ip.append(address)
		else:
		#	print("ping to", address, "failed!")
			successful_ip.append(address)
	print('Here are all the ip address:\n{0}'.format(successful_ip))
	return

ip_scan()