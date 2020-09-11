import os, random
import json
import time 
from base64 import b64decode, b64encode
from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes
import socket

pTimeStart = time.time()
BUFFER_SIZE = 1024
bs = Blowfish.block_size
#key genrator 
key = get_random_bytes(16)

with open('key.json') as jdata:
    b64 = json.load(jdata)
    iv = b64decode(b64['iv'])
    key = b64decode(b64['key'])    
    
    cipher = Blowfish.new(key, Blowfish.MODE_CBC, iv)


    #plaintext
    filename = input("Enter the name of file to be encrypted >> ")
    output_file = filename+".enc"
    file_size = str(os.path.getsize(filename)).zfill(16)


    #encryption
    start_time = time.time()
    chunk_size = 64*1024
    with open(filename, 'rb') as inputfile:
            with open(output_file, 'wb') as outf:
                while True:
                    chunk = inputfile.read(chunk_size)
                    if len(chunk) == 0:
                        break
                    elif len(chunk) % 16 != 0:
                        print(type(chunk))
                        chunk += b' '*(16 - len(chunk)%16)
                    outf.write(cipher.encrypt(chunk))
    end_time = time.time()
    print("enc--- %s seconds ---" % (end_time - start_time))
    
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((socket.gethostname(), 1234))


s.send(str(file_size).encode('utf-8'))
time.sleep(2)
s.send(output_file.encode('utf-8'))


print("sending..")
with open(output_file, 'rb') as f:
    data = f.read(BUFFER_SIZE)
    while True:
        s.send(data)
        data = f.read(BUFFER_SIZE)
        if not data:
            print('Breaking from sending data')
            break
    s.send(b'end')
    s.close()
    print("APP--- %s seconds ---" % (time.time() - pTimeStart))