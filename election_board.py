from voter import *
from paillier import *
from candidate import *
from singleton import Singleton

class CandidateException(Exception):
    pass

@Singleton
class ElectionBoard():
    def __init__(self):
        '''
        candidates: list of Candidate objects
        registered_voters: dict with str key (SSN/VoterID) and Voter value
        '''
        self.candidates = []
        self.registered_voters = {}

        self.candidate_names = set()

        priv, pub = generate_keypair(128) 
        self.private_key = priv
        self.public_key = pub

    def register_voter(self, voter):
        self.registered_voters[voter.voterID] = voter

    def register_voters(self, voters):
        for v in voters:
            self.register_voter(voters[v])

    def register_candidate(self, candidate):
        self.candidates.append(candidate)
        self.candidate_names.add(candidate.name)

    def register_candidates(self, candidates):
        for c in candidates:
            self.register_candidate(c)

    def check_voter(self, voter):
        '''
        Given a voter object, check they're registered and that all info matches up.

        Return True if it's all good, otherwise False
        '''
        if voter.voterID not in self.registered_voters or self.registered_voters[voter.voterID] != voter:
            return False
        return True

    def blind_sign(self, vote):
        '''
        TBD
        '''
        pass

    def decrypt_votes(self, final_tally):
        '''
        final_tally: list of candidates with the final vote counts

        print out the number of votes for each candidate. 
        Requires that the votes have been encrypted with the generated public key
        '''

        unencrypted = []
        for candidate in final_tally:
            if candidate.name not in self.candidate_names:
                raise CandidateException('Candidate in list not registered!')

            unencrypted.append(Candidate(candidate.name, decrypt(self.private_key, self.public_key, candidate.numVotes)))
        
        ## All candidates given to us are registered. Print stuff out now
        for candidate in unencrypted:
            print 'Number of votes for %s is %d'%(candidate.name, candidate.numVotes)

