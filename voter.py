from paillier import *

class Voter(object):
    def __init__(self, name, voterID):
        self.name = name
        self.voterID = voterID
        self.voted = False
        priv, pub = generate_keypair(128) 
        self.private_key = priv
        self.public_key = pub

    def __repr__(self):
        return 'Voter(\'%s\',%s,voted:%s)' % (self.name, self.voterID,str(self.voted))

    def __eq__(self, other):
    	return self.voterID == other.voterID
        