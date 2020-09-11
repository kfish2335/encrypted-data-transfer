import json
import os, random
import time 
from base64 import b64decode
from Crypto.Cipher import Blowfish
#from Crypto.Util.Padding import unpad
import socket
#key was shared with the encrpyed json to simplify things
pTimeStart = time.time()
chunk_size = 64*1024
BUFFER_SIZE = 1024

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((socket.gethostname(), 1234))
s.listen(1)

while True:
    # now our endpoint knows about the OTHER endpoint.
    clientsocket, address = s.accept()
    print(f"Connection from {address} has been established.")
    
    msg = clientsocket.recv(BUFFER_SIZE)
    fsize = int(msg.decode('utf-8'))
    rsize = 0
    
    filename = clientsocket.recv(BUFFER_SIZE)
    filename = filename.decode('utf-8')
    output_file = filename[:-4]
    
    with open(filename, 'wb') as fw:
        while True:
            data = clientsocket.recv(BUFFER_SIZE)
            rsize = rsize + len(data)
            if  data == b'end':
                print('Breaking from file write')
                break
            fw.write(data)
        
        clientsocket.close()
        break;
#opening Json file and assigning variables 
with open('key.json') as jdata:
    b64 = json.load(jdata)
    iv = b64decode(b64['iv'])
    key = b64decode(b64['key'])
    
    #decrytion
    start_time = time.time()
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv) 
    with open(filename, 'rb') as inf:
        with open(output_file, 'wb') as outf:
            while True:
                chunk = inf.read(chunk_size)
                if len(chunk)==0:
                    break
                chunk = cipher.decrypt(chunk)
                outf.write(chunk)
    end_time = time.time()
    print("encrypt--- %s seconds ---" % (end_time - start_time))
    print("APP--- %s seconds ---" % (end_time - pTimeStart))
    s.close()