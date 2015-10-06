import socket
import cgi, cgitb

PORT = 10000
HOST = {1:"192.168.0.5", 2:"192.168.0.16"}
COMANDOS = {1:"ps", 2:"df", 3:"finger", 4:"uptime"}
respostas = []
lista_comandos = []

form = cgi.FieldStorage()

for i in range(1,3):
	cSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	cSocket.connect((HOST[i],PORT))
	for j in range(1,4):
		if (form.getvalue("maq"+str(i)+"_"+COMANDOS[j])):
			parametro = form.getvalue("maq"+str(i)+"-"+COMANDOS[j])
			cSocket.send("REQUEST "+str(j)+" "+parametro)
			resposta = cSocket.recv(4096)
			lista_comandos.append(COMANDOS[j])
			respostas.append(resposta)
	cSocket.close()