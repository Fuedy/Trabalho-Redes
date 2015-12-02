from socket import *
import sys

s = socket(AF_INET,SOCK_DGRAM)
host ="127.0.0.1"
port = int(sys.argv[1])
buf =1024
s.bind((host,port))
addr = (host,port)


file_name,addr = s.recvfrom(buf)
print file_name

s.sendto(file_name,addr)

f=open(file_name,"rb")
data = f.read(buf)
while (data):
    if(s.sendto(data,addr)):
        print "sending ..."
        data = f.read(buf)
s.close()
f.close()