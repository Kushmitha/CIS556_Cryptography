#!/usr/bin/env sage

from sage.all import *
import struct
import re
import base64
from Crypto.PublicKey import RSA
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5

# Our "MPI" format consists of 4-byte integer length l followed by l bytes of binary key
def int_to_mpi(z):
    s = int_to_binary(z)
    return struct.pack('I',len(s))+s

# Horrible hack to get binary representation of arbitrary-length long int
def int_to_binary(z):
    s = ("%x"%z); s = (('0'*(len(s)%2))+s).decode('hex')
    return s

def bits_to_mpi(s):
    return struct.pack('I',len(s))+s

def parse_mpi(s, index):
    length = struct.unpack('<I', s[index:index+4])[0]
    z = Integer(s[index+4:index+4+length].encode('hex'), 16)
    return z, index+4+length

encrypt_header = '-----BEGIN PRETTY BAD ENCRYPTED MESSAGE-----\n'
encrypt_footer = '-----END PRETTY BAD ENCRYPTED MESSAGE-----\n'

# PKCS 7 pad message.
def pad(s,blocksize=AES.block_size):
    n = blocksize-(len(s)%blocksize)
    return s+chr(n)*n

# Encrypt string s using RSA encryption with AES in CBC mode.
# Generate a 256-bit symmetric key, encrypt it using RSA with PKCS1v1.5 padding, and prepend the MPI-encoded RSA ciphertext to the AES-encrypted ciphertext of the message.
def encrypt(rsakey,s):
    aeskey = Random.new().read(32)

    pkcs = PKCS1_v1_5.new(rsakey)
    output = bits_to_mpi(pkcs.encrypt(aeskey))
    
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(aeskey, AES.MODE_CBC, iv)

    output += iv + cipher.encrypt(pad(s))
    return encrypt_header + output.encode('base64') + encrypt_footer


def strip_head_foot(c):
    return (c[44:])[:-43]


def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)
    

def mulinv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x%n


def getPrivExp(moduli, gcds):
    factor2 = long(moduli)/long(gcds)
    totient = (factor2 - 1)*(long(gcds) -1)
    d = mulinv(65537, totient)
    return d


def generate_asn_helper(moduli, gcds, i):
    filename = "asn1_" + str(i)
    f = open(filename, "w")
    factor2 = long(moduli)/long(gcds)
    totient = (factor2 - 1)*(long(gcds) - 1)
    d = mulinv(65537, totient)

    f.write("asn1=SEQUENCE:rsa_key\n\n[rsa_key]\n")
    f.write("modulus=INTEGER:%d\n" % moduli)
    f.write("publicExponent=INTEGER:65537\n")
    f.write("privateExponent=INTEGER:%d\n" % d)
    f.write("p=INTEGER:%d\n" % gcds)
    f.write("q=INTEGER:%d\n" % factor2)
    f.write("e1=INTEGER:%d\n" % (d % long(gcds)-1))
    f.write("e2=INTEGER:%d\n" % (d % (factor2 -1)))
    f.write("coeff=INTEGER:%d\n" % (mulinv(factor2, long(gcds))))

    f.close()


def unpad_pkcs_15(padded):
    padded = padded[1:]
    count = 0
    for c in padded:
        count += 1
        if c == '0':
            if padded[count] == '0':
                return padded[count+1:]

def unpad(s, blocksize=AES.block_size):
    last = struct.unpack("B", s[-1])[0]
    return s[:-last]


def generate_asn(s):
    moduli_file = open('vulnerable_moduli.txt', 'r') 
    gcds_file = open('gcds.txt', 'r')
    moduli = []
    for line in moduli_file:
        moduli.append(int(line, 16))
    gcds = []
    for line in gcds_file:
        gcds.append(int(line, 16))
    base64stuff = strip_head_foot(s)
    ciphertext = base64.decodestring(base64stuff)
    rsa_ciphertext, idx = parse_mpi(ciphertext, 0)
    iv = ciphertext[idx:idx+AES.block_size]
    enc_msg = ciphertext[idx+AES.block_size:]
    for i in range(len(gcds)):
        output = "hw5_" + str(i) + ".pdf"
        aeskey_int = int("9a0d6d8767c2ef7a1a6df5cc35cdef0d75f8b39278473bbf9908324dbd65cf37", 16)
        aeskey = int_to_binary(aeskey_int)
        cipher = AES.new(aeskey, AES.MODE_CBC, iv)
        unpadded_msg = unpad(cipher.decrypt(enc_msg))
        f = open(output, 'w')
        f.write(unpadded_msg);
        f.close()
    moduli_file.close()
    gcds_file.close()


def decrypt_blah(s):
    privkey = RSA.importKey(open('key.txt').read())
    pkcs = PKCS1_v1_5.new(privkey)
    sentinel = Random.new().read(256)
    ciphertext = base64.decodestring(strip_head_foot(s))
    aes_ciphertext, idx = parse_mpi(ciphertext, 0);
    iv = ciphertext[idx:idx+AES.block_size]
    aeskey = pkcs.decrypt(aes_ciphertext, sentinel)
    cipher = AES.new(aeskey, AES.MODE_CBC, iv)
    ciphertext = ciphertext[idx+AES.block_size:]
    return unpad(cipher.decrypt(ciphertext))
    

if __name__=='__main__':
    f = open('hw5.pdf.enc.asc','r')
    ciphertext = f.read()
    generate_asn(ciphertext)
    f.close()
