from paillier import *
import random
priv, pub = generate_keypair(16)
c = encrypt(pub,1)

print c

#u = g^r * s^N mod N^2
r = random.randrange(1,pub.n)
s = random.randrange(1,pub.n)
print r,s, pub.n, pub.g
u =  pow(pub.g , r, pub.n_sq) * pow(c[0] , pub.n, pub.n_sq) % pub.n_sq
print "u =", u
e = random.randrange(0,100)
print "e =", e

w = s * pow(c[0],e) * pow(pub.g,(r + (e * 1)) / pub.n)
print "w=",w
v = r+ (e * 1)

ans = pow(pub.g, v) * pow(c[1], e) * pow(w, pub.n)
print ans
print ans == u
print pub.g