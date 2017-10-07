
Implementation of a side channel attack described in https://www.iacr.org/archive/eurocrypt2002/23320530/cbc02_e02d.pdf

An oracle attempts to decrypt the URL-encoded string passed into it using 128-bit AES in CBC mode with a fixed key, remove the PKCS 7 and confirm whether the decrypted plain-text corresponds to the location of your next homework assignment. It will throw an error if it encounters any problems in this process. The plain-text is obtained by craftily designing the payload to exploit this feature.