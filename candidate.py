class Candidate(object):
    def __init__(self, name, numVotes):
        self.name = name
        self.numVotes = numVotes
        
    def __repr__(self):
        return 'Candidate(\'%s\')' % self.name