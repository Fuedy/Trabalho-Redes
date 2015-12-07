from socket import *
import sys
import select
import binascii
import time
import random
import os.path    

def AppendChunk(sSourceFilespec, fDestinationFileHandle):

    fInput = open(sSourceFilespec, "rb") 
    
    while True:
        byte = fInput.read(1) 

        if byte: 
            fDestinationFileHandle.write(byte)
        else:
            fInput.close()
            break

def PacketCorruption(checksumIn, corruptionFactor):

	corruptionVar = random.randint(0, corruptionFactor)

	if(corruptionVar == 0):
		checksumIn = "0"

	return checksumIn

    
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
            #os.remove(sSourceFilespec)
            nChunkNumber = nChunkNumber + 1
        else:
            break
            
            
    fDestinationFile.close()

host = sys.argv[1]
port = int(sys.argv[2])
corruptionFactor = 1
s = socket(AF_INET,SOCK_DGRAM)
nomeArquivo = sys.argv[3]

addr = (host,port)
buf=65536

s.sendto(nomeArquivo,addr)

data,addr = s.recvfrom(buf)

print "Received File:",data.strip()
numerochunk = 1

while True:
	try:
		#pedaco = "chunk" + str(numerochunk) + "_" + nomeArquivo
		data,addr = s.recvfrom(buf)
		#s.sendto("ack", addr)
		headerpos = data.find("||")
		message = data[headerpos+2:]
		header = data[0:headerpos]
		header = header.split("|")
		print header
		header[1] = PacketCorruption(header[1], corruptionFactor)
		if str(header[0]) != str(-1) :
			checksum = binascii.crc32(message)
			print str(checksum) + "," + str(header[1])
			if (str(checksum) == str(header[1])):
				pedaco = "chunk" + str(header[0]) + "_" + nomeArquivo
				f = open(pedaco,'wb')
				f.write(message)
				#time.sleep(0.1)
				s.sendto(header[0], addr)
				#s.settimeout(1)
				numerochunk = numerochunk + 1
			else:
				print "checksum errado"
		else:
			print "fechou arquivo"
			f.close()
			s.close()
			break
	except timeout:
		f.close()
		s.close()
		print "File Downloaded"
		break

RebuildChunkedFile("./", str(nomeArquivo), "./", "chunk")