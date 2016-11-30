from election_board import *
from paillier import *
from counting_authority import *
import blind_signature as bs

class VotingException(Exception):
    pass

@Singleton
class BulletinBoard():
    def __init__(self):
        self.eb = ElectionBoard.Instance()
        self.ca = CountingAuthority.Instance()

        ## {Voter: list containing the voter's encrypted vote for each candidate}
        ## ex: {Voter('Brian', 1337): [e(1), e(0), e(0)]}
        self.__votes = []
        

    def addVote(self,voterID, vote, signed_vote):
        ## signed_vote is really (signed_vote, blinding_factor)

        if self.eb.has_voter_voted(voterID):
            raise VotingException('Voter already voted, and seemingly got around the safeguards!')

        if len(vote) != len(signed_vote):
            raise VotingException('Number of signed votes does not match number of unsigned votes')

        for i in range(len(vote)):
            if bs.verify(signed_vote[i][0], signed_vote[i][1], self.eb.public_signing_key) != vote[i]:
                raise VotingException('Signed vote doesn\'t match unsigned')

        self.eb.voter_voted(voterID)
        self.__votes.append(vote)

    def endElection(self):
        self.ca.verifiyRowSum(self.__votes)



    


