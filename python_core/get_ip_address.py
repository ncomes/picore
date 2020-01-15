#from subprocess import call
import commands

def get_ip_address(print_ip=False):
	#ip_address = call(['hostname', '-I'])
	ip_address = commands.getoutput('hostname -I')
	if print_ip:
		print('Here is the ip address: {0}'.format(ip_address))
	return ip_address


#ip = get_ip_address()
#print('Here is the ip address: {0}'.format(ip))

