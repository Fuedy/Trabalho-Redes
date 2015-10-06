#!/usr/bin/python

import socket
import cgi, cgitb

PORT = 10000
HOST = {1:"192.168.0.5", 2:"192.168.0.16"}
COMANDOS = {1:"ps", 2:"df", 3:"finger", 4:"uptime"}
maior = ">"
ponto = ";"
pipe = "|"

form = cgi.FieldStorage()

print "Content-type:text/html"
print
print "<html>"
print "<head>"
print "<title>Trabalho de Redes 1</title>"
print "</head>"
print "<body>"

for i in range(1,3):
	cSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
	print "<h2>" + "MAQUINA " + str(i) + "</h2>"
	cSocket.connect((HOST[i],PORT))
	for j in range(1,5):
		if (form.getvalue("maq"+str(i)+"_"+COMANDOS[j])):
			parametro = form.getvalue("maq"+str(i)+"-"+COMANDOS[j])
			if (str(parametro) == "None" or maior in str(parametro) or ponto in str(parametro) or pipe in str(parametro)):
				parametro = ""
			print "<h4>" + str(COMANDOS[j]) + " " + str(parametro) + "</h4>"
			cSocket.send("REQUEST "+str(j)+" "+str(parametro))
			resposta = cSocket.recv(16384)
			resposta = resposta.replace("\n", "<br>")
			print "<p>" + str(resposta[11:]) + "</p>"
	cSocket.close()

print "</body>"
print "</html>"