#!/usr/bin/env sage

from sage.all import *
import struct
import re
import base64
from Crypto.Cipher import AES
from Crypto import Random

key_header = '-----BEGIN PRETTY BAD PUBLIC KEY BLOCK-----\n'
key_footer = '-----END PRETTY BAD PUBLIC KEY BLOCK-----\n'

# Generate ElGamal public key (p,g,y=g^x mod p) in standardized PBP Diffie-Hellman group
def gen_public_key():
    p = 0x3cf2a66e5e175738c9ce521e68361676ff9c508e53b6f5ef1f396139cbd422d9f90970526fd8720467f17999a6456555dda84aa671376ddbe180902535266d383
    R = Integers(p)
    g = R(2)
    x = ZZ.random_element(2**128)
    y = g**x

    key = int_to_mpi(p)+int_to_mpi(g)+int_to_mpi(y)
    return key_header + key.encode('base64') + key_footer

# Our "MPI" format consists of 4-byte integer length l followed by l bytes of binary key
def int_to_mpi(z):
    s = int_to_binary(z)
    return struct.pack('<I',len(s))+s

# Horrible hack to get binary representation of arbitrary-length long int
def int_to_binary(z):
    s = ("%x"%z); s = (('0'*(len(s)%2))+s).decode('hex')
    return s

# Read one MPI-formatted value beginning at s[index]
# Returns value and index + bytes read.
def parse_mpi(s,index):
    length = struct.unpack('<I',s[index:index+4])[0]
    z = Integer(s[index+4:index+4+length].encode('hex'),16)
    return z, index+4+length

# An ElGamal public key consists of a magic header and footer enclosing the MPI-encoded values for p, g, and y.
def parse_public_key(s):
    data = re.search(key_header+"(.*)"+key_footer,s,flags=re.DOTALL).group(1).decode('base64')
    index = 0
    p,index = parse_mpi(data,index)
    g,index = parse_mpi(data,index)
    y,index = parse_mpi(data,index)
    return {'p':p, 'g':g, 'y':y}

encrypt_header = '-----BEGIN PRETTY BAD ENCRYPTED MESSAGE-----\n'
encrypt_footer = '-----END PRETTY BAD ENCRYPTED MESSAGE-----\n'

# PKCS 7 pad message.
def pad(s,blocksize=AES.block_size):
    n = blocksize-(len(s)%blocksize)
    return s+chr(n)*n

def unpad(s,blocksize=AES.block_size):
    last = struct.unpack("B", s[-1])[0]
    return s[:-last]

# Encrypt string s using ElGamal encryption with AES in CBC mode.
# Generate a 128-bit symmetric key, encrypt it using ElGamal, and prepend the MPI-encoded ElGamal ciphertext to the AES-encrypted ciphertext of the message.
def encrypt(pubkey,s):
    p = pubkey['p']; R = Integers(p)
    g = R(pubkey['g']); y = R(pubkey['y'])
    k = ZZ.random_element(2**128)
    m = ZZ.random_element(2**128)

    output = int_to_mpi(g**k)+int_to_mpi(m*(y**k))
    aeskey = int_to_binary(m)
    iv = Random.new().read(AES.block_size)
    cipher = AES.new(aeskey, AES.MODE_CBC, iv)
    output += iv + cipher.encrypt(pad(s))
    return encrypt_header + output.encode('base64') + encrypt_footer

#calculate c1^privkey after stripping off headers
def decrypt(privkey, c):
    no_header = c[44:]
    print c[0:45]
    print no_header[-43:]
    no_footer = no_header[:-43]
    c = base64.decodestring(no_footer)
    c1, mpi_length = parse_mpi(c, 0)
    yk, yk_length = parse_mpi(c, mpi_length)
    iv = c[yk_length:yk_length+AES.block_size]
    s = power_mod(c1, privkey, 51073568366253423420310345125508937772416339915415086570399018230883315969074771647744100130025451846291967857563045828942205360931025287559397568399463299)
    m_prime = (yk * mulinv(s, 51073568366253423420310345125508937772416339915415086570399018230883315969074771647744100130025451846291967857563045828942205360931025287559397568399463299)) % 51073568366253423420310345125508937772416339915415086570399018230883315969074771647744100130025451846291967857563045828942205360931025287559397568399463299
    aeskey = int_to_binary(m_prime)
    cipher = AES.new(aeskey, AES.MODE_CBC, iv)
    enc_msg = c[yk_length+AES.block_size:]
    m = cipher.decrypt(enc_msg)
    f = open("hw4.pdf", 'w')
    f.write(unpad(m))
    f.close

if __name__=='__main__':
    pubkey = parse_public_key(open('key.pub').read())
    print "p: %d" % pubkey['p']
    print "g: %d" % pubkey['g']
    print "y: %d" % pubkey['y']
    ciphertext = open('hw4.pdf.enc.asc').read()
    decrypt(23324220279498140851722058226812548245, ciphertext)
