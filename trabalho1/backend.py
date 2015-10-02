import socket
PORT = 10000
HOST = ''
cSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#cSocket.connect((HOST,PORT))
cSocket.bind((HOST,PORT))
cSocket.listen(10)
(sSocket, address) = cSocket.accept()
print "msg TESTE"
msg = raw_input()
while msg <> '\x18':
	sSocket.send(msg)
	resposta = sSocket.recv(4096)
	print str(resposta)
	msg = raw_input()
cSocket.close()

