#!/usr/bin/python           # This is client.py file

import socket               # Import socket module
import datetime
import numpy
import time
import Queue
import threading
#s = socket.socket()         # Create a socket object
host = socket.gethostname() # Get local machine name
host="127.0.0.1"
port = 12345                # Reserve a port for your service.
host="118.138.241.70"
port=30000
nports=5
nrpt=10
img_dtype=numpy.float32
img_x=1024
img_y=1024

def sendloop(s,q,endStream):
    ta=numpy.empty((1,1),dtype=img_dtype)
    while True:
        b=q.get()
        if isinstance(b,type(ta)):
            s.send(b)
        elif b==endStream:
            s.close
            return


b=[]
s=[]
q=[]
t=[]
endStream=object()
for n in range(0,nports):
    b.append(numpy.empty((img_x,img_y),dtype=img_dtype))
    for i in range(0,img_x):
        for j in range(0,img_y):
            b[n][i,j]=i+img_x*j
    s.append(socket.socket())
    s[n].connect((host, port+n))
    q.append(Queue.Queue())
    t.append(threading.Thread(target=sendloop,args=[s[n],q[n],endStream]))
    t[n].start()
starttime=datetime.datetime.now()
for i in range(0,nrpt):
    for n in range(0,nports):
        q[n].put(b[n])
for n in range(0,nports):
    q[n].put(endStream)
for n in range(0,nports):
    t[n].join()
endtime=datetime.datetime.now()
print "time taken %s"%(endtime-starttime)
