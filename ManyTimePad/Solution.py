import string
import collections

def strxor(a, b):     # xor two strings (trims the longer input)
    return "".join([chr(ord(x) ^ ord(y)) for (x, y) in zip(a, b)])

c1 = "76842603702b18fee1098209005614c2acb0228e1df22c8b0b9b4d4168d02acd02bc5b1bee679fec46269344754f8d40438152a383985696d15b55ad7984120de0c603103db5f52979ccf1ed861940f3fe68df93178ca0162f9d584df9572d58bb80ae7d875611da395b9a9a529e5c98f50b91596660920e122ae8e666b669849de0703f168e281334"
c2 = "7584261c356c19efa35acc1b025b159e8b"
c3 = "0fc26100636e1eb6f041895c1f5505d9eeb82a8702ba2c990c9a1b4c2dd73a8856b75155f86385f6032fd65973008840539d4eb68a930299d11852ac629c1148a3920d1c2abcb1622185d7ea9c5746bdaa69d4c72497b30a28d3520cf9147e5cb7c2aa78894a1cda365a8ccf50db1a91e846935b7b77c203173ce2f426ec67ef"
c4 = "78833a4f666e09ffea4ecc1d034d13dfe5af74e1"
c5 = "7584261c35621ff8a35dcc1618470590e0b4249e05b6609910995e0926cc348f13a61e4fe46783ea1f65d67969079a4041964fa492d64188d10b4aac71811d51a8cb457f"
c6 = "78833a4f786e0df8a44a831808474eba"
c7 = "68cc220a74654ce3ea4b9e190c5f10d2edb36b881ef2698b4cf4"
c8 = "68986f187a7e00f2a44b895c0c1413c2e4b7209f19e4638d05961b4b2e991e8c03a74d52ed6ccce81424865f6f54800f4e8700b08892029bc41751b436860f01b4dd4b142ca1a02573c0a2ed9d5c01eeb16dc4930c8aa9432f9d1f0ca95c2c4abf83b3788d430496261485d541db1a9ce14d95557d60dc1f5e22eee966a73bcbe7"
c9 = "609e2a4f6c6419b6f74c891503535f9eafdc"
c10 = "72992c07356a02b6e5599c0e025512d8a1bf38cb01e37e9d0e871b5020dc369f13a05758ed6ec2b83524d6567c52c5404e9b00be88930292c9081ea173961201a1d007106fa4ba6c60c6e1f698494df4ad6991941086af43259c511efd4a2b48a68ba87f9d02119f2b1ae2"
c11 = "75842a4f7b7e01f4e15b9f5c0c461490f2b96b9e1ff469940b9b4d452ad520cd14bd5917ac6380f4463f9e553d43860d508154b494850293c65b4aab73d30b4eb2de0f552cbfa0206585ecf6811943efbb60dac7118da20e6697501ae71654"
c12 = "63993b4f786a15f4e105cc1618470590ecb7328914ba2c8c0a9b49416fca798c56a75654fe768fed1265d6793a4c8540429154f19f9957dac91547b77e9a1246e0da0e523cf0b32374cbe6b99c4d0f97"
c13 = "688a6f07702b04f7f705cc05024156c2e4f6228551f97a9d10de424b3dcb798513b55a15ac4bcbf40a6b91556900841900974fb092d828"
c14 = "6f99220d70791fb6f04189111e511dc6e4a56b8610ef2c9a07de54513a993b8805a01e4fe36d80eb4865d83a"
c15 = "0fc2610274724cf4e1098d1e015151c4eef6388e14b678900b905c5768d037cd19a0565efe2282ed0b2993426e009d08418000a683d6419bc65c4aed1c"
c16 = "2b"
c17 = "01cc6f2c7a650be4e55d99100c4018dfefa567cb08f979d80a9f4d4168de369902b1501bf86a85eb462d97423300c922558000a889830588cd5b50ac62d3184eaed74b0c2aa4f446"
c18 = "01cc6f367a7e4cf5e547cc1a045a1590f5be2ecb03f37f8c42915d043cd13ccd1ebb535efb6d9ef3463b845f7f4c8c0d53d448b4949318f0"
c19 = "01cc6f07617f1ce5be06c30b1a435fd3e8a5659e01f362964c9b5f5167c73a8405e10b0da36a9ba94923810133508d062a"

ciphertexts = [c1, c2, c3, c4, c5, c6, c7, c8, c9, c10, c11, c12, c13, c14, c15, c16,c17, c18, c19]
target_cipher = "01cc6f07617f1ce5be06c30b1a435fd3e8a5659e01f362964c9b5f5167c73a8405e10b0da36a9ba94923810133508d062a"
key=[]*274
key_found=[]*274

for i, ct1 in enumerate(ciphertexts):
	c = collections.Counter()
	for j, ct2 in enumerate(ciphertexts):
		if i != j:
			chex=strxor(ct1.decode('hex'), ct2.decode('hex'))
			for k, char in enumerate(chex):
				if char in string.printable and char.isalpha(): 
					c[k] += 1
	s = []
	for l, val in c.items():
		if val >= 6: #took 6 after trial and error; maximum letters were figured from the target_cipher.
			s.append(l) 
	xos = strxor(ct1.decode('hex'),' '*274)
	for i in s:
		key.append(xos[i].encode('hex'))
		key_found.append(i)

key_hex = ''.join([val if val is not None else '00' for val in key])
strg = strxor(target_cipher.decode('hex'),key_hex.decode('hex'))
print(''.join([char if i in key_found else '?' for i, char in enumerate(strg)]))

# From the output, guess the letters and words
#1
target_plaintext = "   https://www.cis.upenn.edu/~cis556/hp /fy .pdf"
key = strxor(target_cipher.decode('hex'),target_plaintext)
for cipher in ciphertexts:
    print(strxor(cipher.decode('hex'),key))
#2
c=0;
target_p = "   You can find the rest of the homework problems"
target_c= "01cc6f367a7e4cf5e547cc1a045a1590f5be2ecb03f37f8c42915d043cd13ccd1ebb535efb6d9ef3463b845f7f4c8c0d53d448b4949318f0"
key = strxor(target_c.decode('hex'),target_p)
for cipher in ciphertexts:
	c=c+1
	print(c)
	print(strxor(cipher.decode('hex'),key))	
#3
c=0;
target_p = "The numbers are so unbelievably big, all the computers"
target_c ="75842a4f7b7e01f4e15b9f5c0c461490f2b96b9e1ff469940b9b4d452ad520cd14bd5917ac6380f4463f9e553d43860d508154b494850293c65b4aab73d30b4eb2de0f552cbfa0206585ecf6811943efbb60dac7118da20e6697501ae71654"
key = strxor(target_c.decode('hex'),target_p)
for cipher in ciphertexts:
	c=c+1
	print(c)
	print(strxor(cipher.decode('hex'),key))	
#4
c=0;
target_p = "While the number-field sieve is the best method currently"
target_c ="76842603702b18fee1098209005614c2acb0228e1df22c8b0b9b4d4168d02acd02bc5b1bee679fec46269344754f8d40438152a383985696d15b55ad7984120de0c603103db5f52979ccf1ed861940f3fe68df93178ca0162f9d584df9572d58bb80ae7d875611da395b9a9a529e5c98f50b91596660920e122ae8e666b669849de0703f168e281334"
key = strxor(target_c.decode('hex'),target_p)
for cipher in ciphertexts:
	c=c+1
	print(c)
	print(strxor(cipher.decode('hex'),key))
#5
c=0;
target_p = "This isn't just about large-number theory. It's about cryptography"
target_c ="7584261c35621ff8a35dcc1618470590e0b4249e05b6609910995e0926cc348f13a61e4fe46783ea1f65d67969079a4041964fa492d64188d10b4aac71811d51a8cb457f"
key = strxor(target_c.decode('hex'),target_p)
for cipher in ciphertexts:
	c=c+1
	print(c)
	print(strxor(cipher.decode('hex'),key))	
#6
c=0;
target_p = "While the number-field sieve is the best method currently known, the"
target_c ="76842603702b18fee1098209005614c2acb0228e1df22c8b0b9b4d4168d02acd02bc5b1bee679fec46269344754f8d40438152a383985696d15b55ad7984120de0c603103db5f52979ccf1ed861940f3fe68df93178ca0162f9d584df9572d58bb80ae7d875611da395b9a9a529e5c98f50b91596660920e122ae8e666b669849de0703f168e281334"
key = strxor(target_c.decode('hex'),target_p)
for cipher in ciphertexts:
	c=c+1
	print(c)
	print(strxor(cipher.decode('hex'),key))
#7
c=0;
target_p = "Such an approach is purely theoretical. So far, no one has been able to accomplish"
target_c= "72992c07356a02b6e5599c0e025512d8a1bf38cb01e37e9d0e871b5020dc369f13a05758ed6ec2b83524d6567c52c5404e9b00be88930292c9081ea173961201a1d007106fa4ba6c60c6e1f698494df4ad6991941086af43259c511efd4a2b48a68ba87f9d02119f2b1ae2"
key = strxor(target_c.decode('hex'),target_p)
for cipher in ciphertexts:
	c=c+1
	print(c)
	print(strxor(cipher.decode('hex'),key))	
#8
c=0;
target_p = "The numbers are so unbelievably big, all the computers in the world could not break"
target_c ="75842a4f7b7e01f4e15b9f5c0c461490f2b96b9e1ff469940b9b4d452ad520cd14bd5917ac6380f4463f9e553d43860d508154b494850293c65b4aab73d30b4eb2de0f552cbfa0206585ecf6811943efbb60dac7118da20e6697501ae71654"
key = strxor(target_c.decode('hex'),target_p)
for cipher in ciphertexts:
	c=c+1
	print(c)
	print(strxor(cipher.decode('hex'),key))	
#9
c=0;
target_p = "It would be a breakthrough of Gaussian proportions and allow us to acquire the solution"
target_c ="68986f187a7e00f2a44b895c0c1413c2e4b7209f19e4638d05961b4b2e991e8c03a74d52ed6ccce81424865f6f54800f4e8700b08892029bc41751b436860f01b4dd4b142ca1a02573c0a2ed9d5c01eeb16dc4930c8aa9432f9d1f0ca95c2c4abf83b3788d430496261485d541db1a9ce14d95557d60dc1f5e22eee966a73bcbe7"
key = strxor(target_c.decode('hex'),target_p)
for cipher in ciphertexts:
	c=c+1
	print(c)
	print(strxor(cipher.decode('hex'),key))	
#10
c=0;
target_p = "While the number-field sieve is the best method currently known, there exists an intriguing"
target_c ="76842603702b18fee1098209005614c2acb0228e1df22c8b0b9b4d4168d02acd02bc5b1bee679fec46269344754f8d40438152a383985696d15b55ad7984120de0c603103db5f52979ccf1ed861940f3fe68df93178ca0162f9d584df9572d58bb80ae7d875611da395b9a9a529e5c98f50b91596660920e122ae8e666b669849de0703f168e281334"
key = strxor(target_c.decode('hex'),target_p)
for cipher in ciphertexts:
	c=c+1
	print(c)
	print(strxor(cipher.decode('hex'),key))
#11
c=0;	
target_p = "The numbers are so unbelievably big, all the computers in the world could not break them down"
target_c ="75842a4f7b7e01f4e15b9f5c0c461490f2b96b9e1ff469940b9b4d452ad520cd14bd5917ac6380f4463f9e553d43860d508154b494850293c65b4aab73d30b4eb2de0f552cbfa0206585ecf6811943efbb60dac7118da20e6697501ae71654"
key = strxor(target_c.decode('hex'),target_p)
for cipher in ciphertexts:
	c=c+1
	print(c)
	print(strxor(cipher.decode('hex'),key))	
#12
c=0;
target_p = "...over the rationals, and hence contained in a single cyclotomic field.  Using the Artin map,"
target_c= "0fc26100636e1eb6f041895c1f5505d9eeb82a8702ba2c990c9a1b4c2dd73a8856b75155f86385f6032fd65973008840539d4eb68a930299d11852ac629c1148a3920d1c2abcb1622185d7ea9c5746bdaa69d4c72497b30a28d3520cf9147e5cb7c2aa78894a1cda365a8ccf50db1a91e846935b7b77c203173ce2f426ec67ef"
key = strxor(target_c.decode('hex'),target_p)
for cipher in ciphertexts:
	c=c+1
	print(c)
	print(strxor(cipher.decode('hex'),key))	
#13
c=0;
target_p = "Such an approach is purely theoretical. So far, no one has been able to accomplish such constru"
target_c= "72992c07356a02b6e5599c0e025512d8a1bf38cb01e37e9d0e871b5020dc369f13a05758ed6ec2b83524d6567c52c5404e9b00be88930292c9081ea173961201a1d007106fa4ba6c60c6e1f698494df4ad6991941086af43259c511efd4a2b48a68ba87f9d02119f2b1ae2"
key = strxor(target_c.decode('hex'),target_p)
for cipher in ciphertexts:
	c=c+1
	print(c)
	print(strxor(cipher.decode('hex'),key))	
#14
c=0;
target_p = "While the number-field sieve is the best method currently known, there exists an intriguing possibility"
target_c ="76842603702b18fee1098209005614c2acb0228e1df22c8b0b9b4d4168d02acd02bc5b1bee679fec46269344754f8d40438152a383985696d15b55ad7984120de0c603103db5f52979ccf1ed861940f3fe68df93178ca0162f9d584df9572d58bb80ae7d875611da395b9a9a529e5c98f50b91596660920e122ae8e666b669849de0703f168e281334"
key = strxor(target_c.decode('hex'),target_p)
for cipher in ciphertexts:
	c=c+1
	print(c)
	print(strxor(cipher.decode('hex'),key))

