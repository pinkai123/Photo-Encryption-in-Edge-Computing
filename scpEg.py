from paramiko import SSHClient
from scp import SCPClient

def fileCheck(i):
        #Check for file in the directory and transfer them to the server if it exists
	fileExist = False
	ssh = SSHClient()
	ssh.load_system_host_keys()
	ssh.connect('<static ip address of your raspberry pi>',username = '<username>', password = '<password>')

        # SCPCLient takes a paramiko transport as an argument
	scp = SCPClient(ssh.get_transport())
	command = 'ls /home/pi/Downloads/face-detect-send'
	(stdin, stdout, stderr) = ssh.exec_command(command)
	for line in stdout.readlines():
		scp.get('/home/pi/Downloads/face-detect-send/' + 'key{}'.format(i))
		scp.get('/home/pi/Downloads/face-detect-send/' + 'faceCount{}'.format(i))
		scp.get('/home/pi/Downloads/face-detect-send/' + 'image{}'.format(i))
		scp.get('/home/pi/Downloads/face-detect-send/' + 'associated_data{}'.format(i))
		fileExist = True
		
	scp.close()
	return fileExist


def fileRemove(face_Count,i):
        #Remove file from the client after it is copied to the server
	fileExist = False
	ssh = SSHClient()
	ssh.load_system_host_keys()
	ssh.connect('<static ip address of your raspberry pi>',username = '<username>', password = '<password>')

	command ='rm '+ '/home/pi/Downloads/face-detect-send/' + 'faceCount{}'.format(i) + ' /home/pi/Downloads/face-detect-send/' + 'image{}'.format(i) +' /home/pi/Downloads/face-detect-send/' + 'key{}'.format(i) + ' /home/pi/Downloads/face-detect-send/' + 'associated_data{}'.format(i) +' /home/pi/Downloads/face-detect-send/final.jpg'
	ssh.exec_command(command)

	for i in range(1,int(face_Count)+1):
		command = 'rm /home/pi/Downloads/face-detect-send/'+'face{}.png'.format(i)
		ssh.exec_command(command)

if __name__ == '__main__':
		fileCheck()
