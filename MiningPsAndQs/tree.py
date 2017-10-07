import urllib
# from sage.all import *
from pbp import *

def gcd(a, b):
    while b != 0:
       t = b 
       b = a % b
       a = t
    return a


def strip_head_foot(c):
    return (c[44:])[:-43]


def init_vec(moduli):
    index = 0
    v = []
    while index < len(moduli):
        n, index = parse_mpi(moduli, index)
        v.append(n)
    return v


def product_tree(moduli, tree):
    index = 0
    tree = []
    w = []
    v = moduli
    tree.append(v)
    while len(v) > 1:
        w_length = len(v)/2
        for i in range(w_length):
            w.append(v[2*i]*v[2*i+1])
        if (len(v) % 2 == 1):
            w.append(v[len(v)-1])
        tree.append(w)
        v = w
        w = []
    return tree

def sq_product_tree(moduli, tree):
    index = 0
    tree = []
    w = []
    v = [m**2 for m in moduli]
    tree.append(v)
    while len(v) > 1:
        w_length = len(v)/2
        for i in range(w_length):
            w.append(v[2*i]*v[2*i+1])
        if (len(v) % 2 == 1):
            w.append(v[len(v)-1])
        tree.append(w)
        v = w
        w = []
    return tree


def remainder_tree(sq_tree, tree):
    sq_tree_height = len(sq_tree) - 1
    tree_height = len(tree) -1
    r = tree[tree_height]
    sq_tree_height -= 1
    s = []
    while sq_tree_height >= 0:
        v = sq_tree[sq_tree_height]
        for i in range(len(v)):
            s.append(Mod(r[i/2],(v[i])))
        r = s
        s = []
        sq_tree_height = sq_tree_height - 1
    return r


def all_pairs_gcd(remainders, moduli):
    gcds = []
    for i in range(len(moduli)):
        gcd_i = gcd(long(moduli[i]), long(remainders[i])/long(moduli[i]))
        gcds.append(gcd_i)
    return gcds


def main():
    tree = []
    moduli = []
    moduli_file = open('moduli.sorted')
    vul_moduli_file = open('vulnerable_moduli.txt', 'w')
    gcds_file = open('gcds.txt', 'w')
    for line in moduli_file:
        moduli.append(int(line, 16))

    p_tree = product_tree(moduli, tree)
    sq_p_tree = sq_product_tree(moduli, tree)
    remainders = remainder_tree(sq_p_tree, p_tree)
    apg = all_pairs_gcd(remainders, moduli)
    for i in range(len(apg)):
        if apg[i] != 1:
            gcds_file.write("{:x}".format(apg[i])+"\n")
            print (moduli[i])
            vul_moduli_file.write("{:x}".format(moduli[i])+"\n")
    vul_moduli_file.close()
    gcds_file.close()

main()
