The GNU C Library's implementation of the C rand() function uses a linear congruential generator if the state is initialized with sufficiently small parameters. The solution involves implementing the following algorithm that breaks the linear congruential generator. 

The LCG is of the form x_n = ( a*X_(n-1) + b ) mod m
1. Since the plaintext is a latex source, I assumed "\\newcommand{\\settitl" to be a part of the plaintext.
2. Xoring the cipher with the plaintext one character at a time, and grouping 4 characters together to form an integer, get 5 integers, say, pi,qi,ri,si and ti.
3. Calculate the determinant of |pi qi 1|
                                |qi ri 1|
                                |ri si 1| (source : http://www.reteam.org/papers/e59.pdf)
4. The determinant is an integral multiple of m.
5. Thus, find the factors of the determinant and solve for a and b. Check if a,b and m are predicted right by determining the value of ti from si.

The findabm() module works perfectly fine when I input the five integers manually( generated from a random LCG). The glitch is in converting the 4 byte character array to an integer.
