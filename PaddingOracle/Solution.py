import urllib2
import sys
import encodings

def query(q):
	target = 'http://cis556.cis.upenn.edu/hw3?' + urllib2.quote(q)
	req = urllib2.Request(target)
	try:
		f = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
		if e.code == 404:
			return True 
		elif e.code== 200:
			return True
		return False 

def ct():
    return 'p.c\ne\x11\xac\xf4yH>\xe6\xb6i\xb0\x9c\xee\xb8\x943(l\xa6\xa6\xb0N\xc8\xbeu\xc7I\xd6\xf1\x12\xf2\xb52\xf3\xdf\xe5\xeeli\xa7\x1e\xce\x9c\x1d\xcb?0h\xd9\r\xc9\xbc\xd2\xd5\xdf\xd6`}\xa5\xec\xc0\x12-\x9c\x0f$?\xd8:\x0e\xa5\xc7\xff\r;2\x1b\x83qH\xc5OB\xe2\xee)\xff9-\xa1\xff\xb3'

def makelist(s):
    l = []
    for c in s:
        l.append(c)
    return l

def guesses():
    for i in range(0,256):
        yield chr(i)

def check(g, i, l, it, o):
    c = makelist(ct()[0:l])
    c[i+o] = g
    pad = 16 - i
    for x in range(i+1, 16):
        c[o+x] = chr( ord(it[x]) ^ pad )
    c = ''.join(c)
    return query(c)

def fn(b):
    o=b - 32
    it = [" "] * 16
    pt = [" "] * 16
    for i in xrange(15, -1, -1):
        sol = ""
        for g in guesses():
			if check(g, i, b, it, o):
				sol = g
				break
        if sol == "":
			break
        it[i] = chr( (16-i) ^ ord(sol) )
        pt[i] = chr( ord(ct()[i+o]) ^ ord(it[i]) )
    return ''.join(pt)


text=""
for b in (32,48,64,80,96):
    text = text + fn(b)
    print text
