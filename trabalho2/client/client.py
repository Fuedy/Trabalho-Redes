from socket import *
import sys
import select

def AppendChunk(sSourceFilespec, fDestinationFileHandle):

    fInput = open(sSourceFilespec, "rb") 
    
    while True:
        byte = fInput.read(1) 

        if byte: 
            fDestinationFileHandle.write(byte)
        else:
            fInput.close()
            break


    
def RebuildChunkedFile(sSourcePath, sFilename, sDestinationPath, sChunkPrefix):
    
    import os.path    
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
            os.remove(sSourceFilespec)
            nChunkNumber = nChunkNumber + 1
        else:
            break
            
            
    fDestinationFile.close()

host=sys.argv[1]
port = int(sys.argv[2])
s = socket(AF_INET,SOCK_DGRAM)
nomeArquivo = sys.argv[3]

addr = (host,port)
buf=1024

s.sendto(nomeArquivo,addr)

data,addr = s.recvfrom(buf)

print "Received File:",data.strip()
numerochunk = 1

while True:
	try:
		pedaco = "chunk" + str(numerochunk) + "_" + nomeArquivo
		f = open(pedaco,'wb')
		data,addr = s.recvfrom(buf)
		#s.sendto("ack", addr)
		headerpos = data.find("||")
		message = data[headerpos+2:]
		header = data[0:headerpos]
		header = header.split("|")
		print header
		if header[0] != -1 :
			f.write(message)
			s.settimeout(1)
			numerochunk = numerochunk + 1
		else:
			f.close()
			s.close()
	except timeout:
		f.close()
		s.close()
		print "File Downloaded"
		break

RebuildChunkedFile("./", str(nomeArquivo), "./", "chunk")