import os, random
import json
import time 
from base64 import b64encode
from Crypto.Cipher import Blowfish
from Crypto.Util.Padding import pad
from Crypto.Random import get_random_bytes

s = Blowfish.block_size
#key genrator 
key = get_random_bytes(16)
cipher = Blowfish.new(key, Blowfish.MODE_CBC)

#Saving to json file for dectyptioln program
iv = b64encode(cipher.iv).decode('utf-8')
key = b64encode(key).decode('utf-8')

with open('key.json', 'w') as f:
    json.dump({'iv': iv, 'key': key}, f)
    print(f)