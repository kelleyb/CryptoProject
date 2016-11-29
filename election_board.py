from voter import *
from paillier import *
from candidate import *

class CandidateException(Exception):
    pass

class ElectionBoard():
    def __init__(self, registered_voters, candidates=[]):
        '''
        candidates: list of Candidate objects
        registered_voters: dict with str key (SSN/VoterID) and Voter value
        '''
        self.candidates = candidates
        self.registered_voters = registered_voters

        self.candidate_names = set([candidate.name for candidate in candidates])

        priv, pub = generate_keypair(128) 
        self.private_key = priv
        self.public_key = pub

    def register_candidate(self, candidate):
        self.candidates.append(candidate)
        self.candidate_names.add(candidate.name)

    def register_candidates(self, candidates):
        for c in candidates:
            self.register_candidate(c)

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

