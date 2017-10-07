#g^x=y mod p

def bsgs(h,g,y):
    baby = [1]
    giant = [h]
    n = 1+floor(sqrt(y-1))
    for i in range(1,n):
        baby.append( Mod(baby[i-1]*g,y) )
    g = Mod(g,y)^-n
    for j in range(1,n):
        giant.append( Mod(giant[j-1]*g,y) )
    for i in set(baby).intersection( set(giant) ):
        return  baby.index(i)+n*giant.index(i)