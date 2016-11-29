from election_board import *

@Singleton
class BulletinBoard():
    def __init__(self):
        self.eb = ElectionBoard.Instance()

        ## {Voter: list containing the voter's encrypted vote for each candidate}
        ## ex: {Voter('Brian', 1337): [e(1), e(0), e(0)]}
        self.votes = {}

    def vote(self, voter, vote):
        '''
        voter: the voter object
        vote: list of the user's votes 

        Check to make sure the voter is actually valid, they only vote for one
        candidate, and they know who they're voting for

        TODO
        '''
        if self.eb.check_voter(voter):

            ## Need to check if voter voted for more than one person? Or is that done somewhere else? 
            self.votes[voter] = vote
