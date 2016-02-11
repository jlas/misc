import pandas as pd
import struct

# http://www.nch.com.au/acm/8k8bitpcm.wav
with open('8k8bitpcm.wav') as f:
    raw = f.read()

header = raw[:40]
data = raw[40:]

def frombytes(bytes):
    return [struct.unpack('B',b)[0] for b in bytes]

def tobytes(data):
    return ''.join([struct.pack('B',b) for b in data])

def decode(samples):  # 8 bit PCM
    return [(s - 128)/128.0 for s in samples]

def encode(samples):  # 8 bit PCM
    return [s*128 + 128 for s in samples]

samples = decode(frombytes(data))
samples = [s/2 for s in samples]

with open('out.wav', 'wb') as f:
    f.write(header + tobytes(encode(samples)))

