from election_board import *
from paillier import *
from counting_authority import *

@Singleton
class BulletinBoard():
    def __init__(self):
        self.eb = ElectionBoard.Instance()
        self.ca = CountingAuthority.Instance()

        ## {Voter: list containing the voter's encrypted vote for each candidate}
        ## ex: {Voter('Brian', 1337): [e(1), e(0), e(0)]}
        self.votes = []
        

    def addVote(self,vote):
        self.votes.append(vote)

    def endElection(self):
        self.ca.verifiyRowSum(self.votes)



    


