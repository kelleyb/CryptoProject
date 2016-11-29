class Voter(object):
    def __init__(self, name, voterID):
        self.name = name
        self.voterID = voterID

    def __repr__(self):
        return 'Voter(\'%s\':%s)' % (self.name, self.voterID)
        