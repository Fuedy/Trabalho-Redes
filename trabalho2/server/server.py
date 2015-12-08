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

    # Setup the input filespec and initialize nChunkNumber
    sInputFilespec = sInputFilepath + sInputFilename
    nChunkNumber = 1
    
    # Open the input file and call WriteChunk until we are out of data
    with open(sInputFilespec, "rb") as f:
        while True:
            # build the output filespec and open the file for binary write
            sOutputFilespec = sOutputFilepath + sPrefix + str(nChunkNumber) + "_" + sInputFilename
            out = open(sOutputFilespec, "wb")

            # write the chunked file
            WriteChunk(f, out, nChunkSize)
            
            # if the inputfile is closed upon return, it means we are out of data and finished
            if f.closed:
                break
                
            # if here, we still have data to write. Bump the chunk number and loop back
            nChunkNumber = nChunkNumber + 1
    return nChunkNumber

def RemoveTemporaryFiles(nChunkNumber,file_name):
	for i in range (1,nChunkNumber+1):
		sOutputFilespec = "./" + "chunk" + str(i) + "_" + str(file_name)
		os.remove(sOutputFilespec)


s = socket(AF_INET,SOCK_DGRAM)
host = "127.0.0.1"
port = int(sys.argv[1])
buf = 65536
s.bind((host,port))
addr = (host,port)
test = []
erroAck = []
terminou = 0
flag = 0
file_name,addr = s.recvfrom(buf)
print file_name

s.sendto(file_name,addr)
s.setblocking(0)
nChunkNumber = WriteChunkFiles("./", str(file_name), "./", "chunk", 64512)
lastChunkSent = 1
inicioJanela = 1

while terminou == 0:
	del test [:]
	lastChunkSent = inicioJanela
	enviado = 0
	for i in range(1,6):
		print "enttri nmo for"
		if lastChunkSent <= nChunkNumber :
			sOutputFilespec = "./" + "chunk" + str(lastChunkSent) + "_" + str(file_name)
			g = open(sOutputFilespec, "rb")
			print "zaia1"
			data = g.read()
			print "zaia2"
			checksum = binascii.crc32(data)
			header = headerproto % (lastChunkSent, checksum)
			data = header + data
			s.sendto(data,addr)
			enviado = enviado +1
			print lastChunkSent
			print nChunkNumber
			lastChunkSent = lastChunkSent + 1
			try:
				time.sleep(0.5)
				test.append(s.recv(buf))
			except error:
				print "deu errado no for"
		
	try:
		time.sleep(0.5)
		test.append(s.recv(buf))
  	except error:
  		print "deu erro no try"

  	time.sleep(0.5)
  	print test

  	flag = 0
  	t = 0
  	while t < 10:
  		if len(test)!=enviado:
  			time.sleep(0.1)
  			t = t+1
  		if len(test) == enviado:
  			t = 10
  			flag = 1
  	if flag == 1:
  		inicioJanela = inicioJanela + 5
  	if inicioJanela > lastChunkSent:  		
  		terminou = 1
  		header = headerproto % (-1,0)
  		print "mandei fim arquivo"
  		s.sendto(header,addr)


print test
print erroAck
s.close()
RemoveTemporaryFiles(nChunkNumber,file_name)