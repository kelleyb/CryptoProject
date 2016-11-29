class Voter(object):
    def __init__(self, name, voterID):
        self.name = name
        self.voterID = voterID
        self.voted = False

    def __repr__(self):
        return 'Voter(\'%s\':%s)' % (self.name, self.voterID)

    def __eq__(self, other):
    	return self.name == other.name and self.voterID == other.voterID
        