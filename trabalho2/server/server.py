from socket import *
import sys
import os.path
import struct
import math
import os
import binascii
import time

headerproto = "%d|%d||"

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

	        WriteChunk(f, out, nChunkSize)

	        g = open(sOutputFilespec, "rb")
	        data = g.read()
	        checksum = binascii.crc32(data)

	        header = headerproto % (nChunkNumber, checksum)
	        data = header + data
	        s.sendto(data,addr)
	        #mensagem = s.recvfrom(buf)
         	#print str(mensagem)
         	try:
         		time.sleep(0.5)
         		test.append(s.recv(buf))
         	except error:
         		print "deu errado"
         	#os.remove(sOutputFilespec)

	        if f.closed:
	        	flag = 0
	        	time.sleep(1)
	        	for i in range (1,nChunkNumber+1):
	        		for j in range (0,len(test)):
	        			if test[j] == str(i):
	        				flag = 1
	        		if flag == 0:
	        			erroAck.append(i)
	        		flag = 0
	        	for i in erroAck:
	        		resendFilePath = sOutputFilepath + sPrefix + str(i) + "_" + sInputFilename
	        		resendFile = open(resendFilePath,"rb")
	        		dataResend = resendFile.read()
	        		checksum = binascii.crc32(dataResend)
	        		header = headerproto % (i, checksum)
	        		dataResend = header + dataResend
	        		s.sendto(dataResend,addr)


	        	header = headerproto % (-1, 0)
	        	s.sendto(header, addr)
	        	break
	            
	        nChunkNumber = nChunkNumber + 1


s = socket(AF_INET,SOCK_DGRAM)
host = "127.0.0.1"
port = int(sys.argv[1])
buf = 65536
s.bind((host,port))
addr = (host,port)
test = []
erroAck = []
flag = 0
file_name,addr = s.recvfrom(buf)
print file_name

s.sendto(file_name,addr)
s.setblocking(0)
WriteChunkFiles("./", str(file_name), "./", "chunk", 64512)
print test
print erroAck
s.close()