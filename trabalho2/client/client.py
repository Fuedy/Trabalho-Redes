from socket import *
import sys
import select
import binascii
import time
import random
import os.path    

#IMPORTANTE: LER O README DO REPOSITORIO SOBRE O T2

#Funcao usada para a corrupcao de pacote
#A chance depende do corruption factor: Chance de corromper = 1/(corruptionFactor+1)
#Para corromper, apenas troca o checksum para o valor 0
#A variavel de retorno eh o novo checksum do pacote
def PacketCorruption(checksumIn, corruptionFactor):

	corruptionVar = random.randint(0, corruptionFactor)

	if(corruptionVar == 0):
		checksumIn = "0"

	return checksumIn

#Funcao usada para a perda de pacote
#A chance depende do packetLossFactor: Chance de corromper = 1/(packetLossFactor+1)
#Para corromper, apenas troca o checksum para o valor
#A variavel de retorno define se o pacote vai ser perdido ou nao 
def PacketLoss(packetLossFactor):

	packetLossVar = random.randint(0, packetLossFactor)
	return packetLossVar

#As duas funcoes abaixo servem para juntar os pacotes num arquivo so novamente
#Maiores explicacoes de como essa funcao funciona e motivo, estao no arquivo readme do repositorio.
#A funcao appendchunk coloca byte a byte no arquivo, ate acabar o arquivo
def AppendChunk(sSourceFilespec, fDestinationFileHandle):

    fInput = open(sSourceFilespec, "rb") 
    
    while True:
        byte = fInput.read(1) 

        if byte: 
            fDestinationFileHandle.write(byte)
        else:
            fInput.close()
            break

#A funcao RebuildChunkedFile ira definir o nome e tamanho de cada arquivo chunk    
def RebuildChunkedFile(sSourcePath, sFilename, sDestinationPath, sChunkPrefix):
    
    sDestinationFilespec = sDestinationPath +  sFilename
    
    if os.path.isfile(sDestinationFilespec) :

        print "Destination already exists: " + sDestinationFilespec
        return None
    
    fDestinationFile = open(sDestinationFilespec, "wb")
    
    nChunkNumber = 1
    while True:

        sSourceFilespec = sSourcePath + sChunkPrefix + str(nChunkNumber) + "_" + sFilename

        if os.path.isfile(sSourceFilespec):
            AppendChunk(sSourceFilespec, fDestinationFile)
            nChunkNumber = nChunkNumber + 1
        else:
            break
            
            
    fDestinationFile.close()

#Funcao utilzada para limpar os arquivos temporarios criados.
def RemoveTemporaryFiles(nChunkNumber,file_name):
	for i in range (1,nChunkNumber+1):
		sOutputFilespec = "./" + "chunk" + str(i) + "_" + str(file_name)
		os.remove(sOutputFilespec)

#Variaveis que vem da chamada do programa. Definem o host, numero da porta e nome do arquivo
host = sys.argv[1]
port = int(sys.argv[2])
nomeArquivo = sys.argv[3]

#Variaveis que definem a chance de corrupcao e perda de pacote
corruptionFactor = 19
packetLossFactor = 19

#Aloca o socket
s = socket(AF_INET,SOCK_DGRAM)
addr = (host,port)

#Tamanho do buffer de leitura. Igual valor UDP maximo de 64k
buf=65536

#Envia o nome do arquivo que quer baixar
s.sendto(nomeArquivo,addr)

data,addr = s.recvfrom(buf)

print "Arquivo que sera baixado",data.strip()

#Variavel de controle para o numeros de pacotes
numerochunk = 1

#Loop para o recebimento do arquivo
while True:
	try:
		#Recebe o pacote
		data,addr = s.recvfrom(buf)

		#Separa o header dos dados do pacote. A definicao do header eh feito no server.py
		headerpos = data.find("||")
		message = data[headerpos+2:]
		header = data[0:headerpos]
		header = header.split("|")
		print header
		if PacketLoss(packetLossFactor) == 0 :
			print "Perdeu o pacote"
		else: 
			header[1] = PacketCorruption(header[1], corruptionFactor)
			if str(header[0]) != str(-1) :
				lastChunk = header[0]
				#Funcao usada para criar o checksum, utiliza a biblioteca binascii.py
				checksum = binascii.crc32(message)
				if (str(checksum) == str(header[1])):
					pedaco = "chunk" + str(header[0]) + "_" + nomeArquivo
					f = open(pedaco,'wb')
					f.write(message)
					s.sendto(header[0], addr)
					numerochunk = numerochunk + 1
				else:
					print "checksum errado"
			else:
				print "Fechou arquivo"
				f.close()
				s.close()
				break
	except timeout:
		f.close()
		s.close()
		print "Fechou o arquivo"
		break

#Reconstroi o arquivo final utilizando os pacotes recebidos
RebuildChunkedFile("./", str(nomeArquivo), "./", "chunk")

#Limpa os arquivos temporarios criados
RemoveTemporaryFiles(int(lastChunk),nomeArquivo)