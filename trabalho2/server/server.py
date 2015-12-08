from socket import *
import sys
import os.path
import struct
import math
import os
import binascii
import time

#IMPORTANTE: LER O README DO REPOSITORIO SOBRE O T2

#Definicao do cabecalho do pacote. Possui o numero de sequencia e o checksum do arquivo
headerproto = "%d|%d||"

#As duas funcoes abaixo servem para separar os pacotes
#Maiores explicacoes de como essa funcao funciona e motivo, estao no arquivo readme do repositorio.
#A funcao WriteChunk coloca byte a byte no pacote ate acabar o arquivo
def WriteChunk(fInput, fOutput, nMaxBytes):
		
		for i in xrange(nMaxBytes - 1):

				byte = fInput.read(1)
				
				if byte:
						fOutput.write(byte)
				else:
					fInput.close()
					break

		fOutput.close()

#A funcao WriteChunkFiles ira quebrar o arquivo desejado em varios pacotes (chunks) do tamanho especificado.
#Nessa aplicacao, quebramos em pacotes de de 64512 bytes, que eh proximo do valor maximo de UDP, para poder caber o cabecalho
def WriteChunkFiles(sInputFilepath, sInputFilename, sOutputFilepath, sPrefix, nChunkSize):

		
		sInputFilespec = sInputFilepath + sInputFilename
		nChunkNumber = 1
		
		
		with open(sInputFilespec, "rb") as f:
				while True:
						
						sOutputFilespec = sOutputFilepath + sPrefix + str(nChunkNumber) + "_" + sInputFilename
						out = open(sOutputFilespec, "wb")

						
						WriteChunk(f, out, nChunkSize)
						
						
						if f.closed:
								break
								
						
						nChunkNumber = nChunkNumber + 1
		return nChunkNumber

#A funcao RebuildChunkedFile ira definir o nome e tamanho de cada arquivo chunk
def RemoveTemporaryFiles(nChunkNumber,file_name):
	for i in range (1,nChunkNumber+1):
		sOutputFilespec = "./" + "chunk" + str(i) + "_" + str(file_name)
		os.remove(sOutputFilespec)

#Cria o socket com os valores passados como parametros
s = socket(AF_INET,SOCK_DGRAM)
host = "127.0.0.1"
port = int(sys.argv[1])
buf = 65536
s.bind((host,port))
addr = (host,port)

#Variavel test utilizada para escutar os ACK. A variavel erroAck armazena o numero dos pacotes do ACK que faltaram
test = []
erroAck = []

#Duas variaveis de controle, explicadas adiantes
terminou = 0
flag = 0

file_name,addr = s.recvfrom(buf)
print file_name

s.sendto(file_name,addr)

#Seta como nao bloqueante o socket
s.setblocking(0)

#Quebra o arquivo em pacotes
nChunkNumber = WriteChunkFiles("./", str(file_name), "./", "chunk", 64512)

lastChunkSent = 1
inicioJanela = 1

#Tamanho da Janela
tamanhojanela = 5

while terminou == 0:
	#Loop de envio de pacotes
	del test [:]
	lastChunkSent = inicioJanela
	enviado = 0
	for i in range(1,tamanhojanela+1):
		#Caso o ultimo chunk ja nao tenha sido enviado
		if lastChunkSent <= nChunkNumber :
			sOutputFilespec = "./" + "chunk" + str(lastChunkSent) + "_" + str(file_name)
			g = open(sOutputFilespec, "rb")
			data = g.read()
			checksum = binascii.crc32(data)
			#Usa o prototipo do header para criar o header (cabecalho)
			header = headerproto % (lastChunkSent, checksum)
			data = header + data
			s.sendto(data,addr)
			enviado = enviado +1
			lastChunkSent = lastChunkSent + 1
			try:
				time.sleep(0.5)
				test.append(s.recv(buf))
			except:
				print ""
	
	#Espera receber os acks de modo nao bloquante	
	try:
		time.sleep(0.5)
		test.append(s.recv(buf))
	except error:
			print "Ainda esperando ACK"
	flag = 0
	t = 0
	#Espera por 1 segundo os ACKS chegarem, senao da timeout e envia novamente
	while t < 10:
		if len(test)!=enviado:
			time.sleep(0.1)
			t = t+1
		if len(test) == enviado:
			t = 10
			flag = 1
	#Caso tenha recebido todos os ACKS, move para a proxima janela
	#Caso NAO tenha recebido todos os ACKS, envia novamente os pacotes da janela
	if flag == 1:
		inicioJanela = inicioJanela + tamanhojanela
	#Caso tenha enviado o ultimo pacote, envia pacote de fim arquivo
	if inicioJanela > lastChunkSent:  		
		terminou = 1
		header = headerproto % (-1,0)
		print "mandei fim arquivo"
		s.sendto(header,addr)

s.close()

#Remove os arquivos temporarios criados
RemoveTemporaryFiles(nChunkNumber,file_name)