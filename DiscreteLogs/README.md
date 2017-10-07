Use the attack described in the paper (http://citeseerx.ist.psu.edu/viewdoc/download?doi=10.1.1.14.5952&rep=rep1&type=pdf) by van Oorschot and Wiener to compute the discrete log of the public key and use it to decrypt the ciphertext.


STEPS:

I. Pohlig Hellman Algorithm:
	1. Find p,g,y from the public key.
	2. Factor p-1 into a product of primes using Sage factor() method
	3. Run Baby Step Giant step algorithm to find residues, x_i.
	4. Use Chinese Remainder Theorem to solve the system of congruences to obtain x.(crt.py took a long time, hence used the inbuilt crt from sage).

II. Find the private key and use Elgammal decryption scheme to obtain the plaintext.