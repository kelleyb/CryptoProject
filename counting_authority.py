from voter import *
from paillier import *
from candidate import *
from singleton import Singleton
from election_board import *
import random
@Singleton
class CountingAuthority():
    """docstring for ClassName"""
    def __init__(self):

        self.eb = ElectionBoard.Instance()

        self.validVotes = []

    def finalTally(self):
        for x in range(0,random.randint(50,100)):
            random.shuffle(self.validVotes)

        for voter_vote in self.validVotes:

            for i in range(len(self.eb.candidates)):
                self.eb.candidates[i].numVotes = e_add(self.eb.public_key,self.eb.candidates[i].numVotes,voter_vote[i])
        return self.eb.decrypt_votes()
    def verifiyRowSum(self, input):
        for x in range(0,random.randint(0,100)):
            random.shuffle(input)

        for voterVotes in input:
            currentSum = encrypt(self.eb.public_key,0)
            hasVote = False
            valid = True
            for singleVote in voterVotes:
                #encrypt(eb.public_key, v
                temp = decrypt(self.eb.private_key, self.eb.public_key, encrypt(self.eb.public_key, e_add(self.eb.public_key,singleVote, currentSum)))
                # print temp
                if hasVote and temp != 1:
                    valid = False
                    break

                elif not hasVote and (temp == 0 or temp == 1):
                    if temp == 1:
                        hasVote = True
                        currentSum += e_add(self.eb.public_key, singleVote, currentSum)
            # print valid
            if valid:
                self.validVotes.append(voterVotes)
        return self.finalTally()

        