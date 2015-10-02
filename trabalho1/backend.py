import socket
PORT = 10000
HOST = '192.168.0.2'
cSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
cSocket.connect((HOST,PORT))
msg = raw_input()
while msg <> '\x18':
	cSocket.send(msg)
	resposta = cSocket.recv(4096)
	print str(resposta)
	msg = raw_input()
cSocket.close()
