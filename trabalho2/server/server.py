from socket import *
import sys
import os.path
import struct
import math
import os

headerproto = "%d ||"

def WriteChunk(fInput, fOutput, nMaxBytes):
    
    for i in xrange(nMaxBytes - 1): # loop until nMaxBytes or out of data

        byte = fInput.read(1) # read a byte
        
        if byte: # if we got one, write it, otherwise, close fInput and leave
            fOutput.write(byte)
        else:
            fInput.close()
            
            break

    fOutput.close()

def WriteChunkFiles(sInputFilepath, sInputFilename, sOutputFilepath, sPrefix, nChunkSize):

	sInputFilespec = sInputFilepath + sInputFilename
	nChunkNumber = 1

	with open(sInputFilespec, "rb") as f:
	    while True:

	        sOutputFilespec = sOutputFilepath + sPrefix + str(nChunkNumber) + "_" + sInputFilename
	        out = open(sOutputFilespec, "wb")
	        header = headerproto % (nChunkNumber)

	        WriteChunk(f, out, nChunkSize)

	        g = open(sOutputFilespec, "rb")
	        data = g.read()
	        data = header + data
	        s.sendto(data,addr)
	        #mensagem = s.recvfrom(buf)
         	#print str(mensagem)
         	os.remove(sOutputFilespec)

	        if f.closed:
	        	header = headerproto % (-1)
	        	s.sendto(header, addr)
	        	break
	            
	        nChunkNumber = nChunkNumber + 1


s = socket(AF_INET,SOCK_DGRAM)
host = "127.0.0.1"
port = int(sys.argv[1])
buf = 1024
s.bind((host,port))
addr = (host,port)

file_name,addr = s.recvfrom(buf)
print file_name

s.sendto(file_name,addr)

WriteChunkFiles("./", str(file_name), "./", "chunk", 100)

s.close()