#A biblioteca Threading serve para trabalhar com threads. 
#A bilioteca subprocess fornece metodos de enviar um comando para ser executado pelo shell do sistema. 
#Depois, ele redireciona a saida alterando o destino do vetor de arquivos aberto para esse programa,
#onde o valor fica armazenado na variavel "saida"
#A biblioteca socket e o que permite trabalhar com sockets.

from threading import Thread
import subprocess
import socket

#Tamanho maximo para a mensagem.
TAMANHO_MAX = 16384

#Funcao que sera chamada na criacao da Thread
def handle(clientsocket):
	while 1:
		#Recebe o pacote do webserver
		pacote = clientsocket.recv(TAMANHO_MAX)

		#Caso pacote venha vazio
		if pacote == '': return

		#Separa o pacote usando o espaco como separador
		argumentos = pacote.split()

		#Verifica se o pacote tem o REQUEST
		if str(argumentos[0] == "REQUEST"):

			#Transforma o numero passado pelo pacote para o comando desejado
			if str(argumentos[1]) == "1":
				comando = "ps"
			elif str(argumentos[1]) == "2":
				comando = "df"
			elif str(argumentos[1]) == "3":
				comando = "finger"
			elif str(argumentos[1]) == "4":
				comando = "uptime"

			#Tenta executar o comando assumindo que possui parametros adicionais.
			#Ele apresenta erro caso nao tenha parametros adicionais
			try:
				saida = subprocess.Popen([comando, str(argumentos[2])], stdout = subprocess.PIPE, stderr = subprocess.STDOUT).communicate()[0]
			
			#No caso de erro do anterior, tenta executar sem os parametros adicionais 
			except:
				saida = subprocess.Popen([comando], stdout = subprocess.PIPE, stderr = subprocess.STDOUT).communicate()[0]
			
			#Gera o pacote de resposta para enviar para o webserver
			pacoteResposta = "RESPONSE " + str(argumentos[1]) + " " + saida

			#Envia a resposta
			clientsocket.send(pacoteResposta)

#Cria um socket TCP
serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Porta escolhida pelo grupo para o trabalho
PORT = 10000
HOST = ''

#Bind do socket e fica esperando conexao. O parametro do listen define o tamanho maximo da fila
serversocket.bind((HOST, PORT))
serversocket.listen(10)

#Gera as thread necessarias
while 1:
	#Cria conexao TCP com o webserver
    (clientsocket, address) = serversocket.accept()

    ct = Thread(target=handle, args=(clientsocket,))
    ct.run()







