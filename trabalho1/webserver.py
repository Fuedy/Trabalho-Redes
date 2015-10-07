#!/usr/bin/python
#necessario colocar caminho do python para uso do apache

#Importada bibliotecas para funcionamento dos sockets e scripts cgi
import socket
import cgi, cgitb

#Porta de comunicacao previamente definida
PORT = 10000

#HOST e um vetor com os ip's das maquinas onde os daemons estao presentes
HOST = {1:"192.168.0.5", 2:"192.168.0.16"}

#COMANDOS e um vetor com os comandos que podem ser requisitados as maquinas
COMANDOS = {1:"ps", 2:"df", 3:"finger", 4:"uptime"}

#definicao dos caracteres invalidos para consulta as maquinas
maior = ">"
ponto = ";"
pipe = "|"

#o formulario submetido pelo servidor e lido e guardado
form = cgi.FieldStorage()

#comeco da criacao da pagina de resposta com as respostas dos comandos realizados nas maquinas
print "Content-type:text/html"
print
print "<html>"
print "<head>"
print "<title>Trabalho de Redes 1</title>"
print "</head>"
print "<body>"

#loop externo responsavel por fazer controle de todas as tres maquinas possiveis de comunicacao
#foi definido que e possivel comunicar com ate tres maquinas e requisitar comandos
for i in range(1,4):

	#criacao de um socket que se comunica com protocolo v4 de enderecos e cria um servico confiavel de entrega de pacote
	cSocket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)

	#e exibido na pagina o nome e numero da maquina em questao 
	print "<h2>" + "MAQUINA " + str(i) + "</h2>"

	#o socket criado acima e conectado com uma das maquinas utilizando a porta definida acima e o primeiro dos enderecos tambem definido acima
	cSocket.connect((HOST[i],PORT))

	#loop interno para controle dos comandos possiveis de ser requisitados para cada maquina
	for j in range(1,5):

		#condicao para verificar se a caixa de marcacao do comando, no formulario, esta marcada
		if (form.getvalue("maq"+str(i)+"_"+COMANDOS[j])):
			#caso a caixa esteja marcada, e armazenado em uma variavel o parametro selecionado
			parametro = form.getvalue("maq"+str(i)+"-"+COMANDOS[j])

			#condicao para exclusao de parametros invalidos para requisicao
			if (str(parametro) == "None" or maior in str(parametro) or ponto in str(parametro) or pipe in str(parametro)):
				parametro = ""

			#exibicao do nome do comando junto com o parametro requisitado, caso ele exista
			print "<h4>" + str(COMANDOS[j]) + " " + str(parametro) + "</h4>"

			#envio do request, atraves do socket, para o daemon localizado na maquina em questao
			cSocket.send("REQUEST "+str(j)+" "+str(parametro))

			#resposta recebida da maquina. Armazenada em uma variavel
			resposta = cSocket.recv(16384)

			#devido ao "Mounted on" ter um espaco em seu nome tivemos que concatena-lo para que nossa regra de pular linha na tabela funcione
			resposta = resposta.replace("Mounted on", "MountedOn")

			#aqui apenas marcamos o final de cada linha da tabela
			resposta = resposta.replace("\n", " fimLinha ")
			print "<table>"
			print "<tr>"

			#conta o numero de palavras que terao que ser exibidas na resposta
			nroPalavras = len(resposta[11:].split())

			#e separado cada palavra da resposta
			resposta = resposta[11:].split()

			#no final de cada linha e colocado um </tr> para funcionar como final de linha de tabela
			#ao final de cada palavra e dado um </td> para mostrar o final de cada celula da tabela
			for k in range(nroPalavras):
				if str(resposta[k]) == "fimLinha":
					print "</tr>"
				else:
					print "<td>"
					print str(resposta[k])
					print "</td>"
			print "</tr>"
			print "</table>"

	#fechamento do socket aberto para comunicao com a maquina
	cSocket.close()

#fim da pagina html de resposta
print "</body>"
print "</html>"