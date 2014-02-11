#!/usr/bin/python           # This is server.py file

import socket               # Import socket module
import numpy
import datetime
import Queue
import threading
img_dtype=numpy.float32
img_x=1024
img_y=1024
buffers=Queue.Queue()
host="127.0.0.1"
port = 12345                # Reserve a port for your service.
host="118.138.241.70"
port=30000
nports=5
nbuffers=5*nports

def recvloop(s,buffers,outputQ,endStream):
    c,addr=s.accept()
    while True:
        b=buffers.get()
        nbytes=c.recv_into(b,b.itemsize*img_x*img_y,socket.MSG_WAITALL)
        if nbytes!=b.itemsize*img_x*img_y:
            outputQ.put(endStream)
            c.close
            return
        outputQ.put(b)

for i in range(0,nbuffers):
    b=numpy.empty((img_x,img_y),dtype=img_dtype)
    buffers.put(b)

ta=numpy.empty((1,1),dtype=img_dtype)
endStream=object()
q=[]
s=[]
t=[]
for n in range(0,nports):
    q.append(Queue.Queue())
    s.append(socket.socket())
    s[n].bind((host,port+n))
    s[n].listen(5)
    t.append(threading.Thread(target=recvloop,args=[s[n],buffers,q[n],endStream]))
    t[n].start()

notDone=True
count=0
while notDone:
    for n in range(0,nports):
        r=q[n].get()
        if not isinstance(r,type(ta)):
            if r==endStream:
                notDone=False
                t[n].join()
        else:
            count=count+1
            buffers.put(r)
print "received %d chunks of data"%count
