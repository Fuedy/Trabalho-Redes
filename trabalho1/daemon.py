from subprocess import call
from threading import Thread
import sys
import subprocess
import socket
import time

TAMANHO_MAX = 4096

def handle(clientsocket):
	while 1:
		pacote = clientsocket.recv(TAMANHO_MAX)
		if pacote == '': return
		print pacote
		argumentos = pacote.split()
		if '>'  in str(argumentos) or '|' in str(argumentos) or ';' in str(argumentos):
			print "Parametro Invalido. Nao use > ou | ou ; "

		elif str(argumentos[0] == "REQUEST"):
			if str(argumentos[1]) == "1":
				comando = "ps"
			elif str(argumentos[1]) == "2":
				comando = "df"
			elif str(argumentos[1]) == "3":
				comando = "finger"
			elif str(argumentos[1]) == "4":
				comando = "uptime"
			try:
				saida = subprocess.Popen([comando, str(argumentos[2])], stdout = subprocess.PIPE, stderr = subprocess.STDOUT).communicate()[0]
			except:
				saida = subprocess.Popen([comando], stdout = subprocess.PIPE, stderr = subprocess.STDOUT).communicate()[0]
			print saida
			pacoteResposta = "RESPONSE " + str(argumentos[1]) + " " + saida
			print "--------------"
			print str(pacoteResposta)
			clientsocket.send(pacoteResposta)

PORT = 10000
HOST = '192.168.0.16'

serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
while serversocket.connect_ex((HOST,PORT)) <>0:
	print "Esperando abrir conexao com o backend.py"
	time.sleep(2)

while 1:
	ct = Thread(target=handle, args=(serversocket,))
	ct.run()







