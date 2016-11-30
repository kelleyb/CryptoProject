from voter import *
from paillier import *
from candidate import *
from singleton import Singleton
import blind_signature as bs

class CandidateException(Exception):
    pass

class VoterException(Exception):
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

        #############################################
        ## FUCK IT WE'RE DOING IT LIVE
        #############################################
        pub_sign, priv_sign = bs.keygen(2**256)
        self.public_signing_key = pub_sign
        self.private_signing_key = priv_sign

    def register_voter(self, voter):
        self.registered_voters[voter.voterID] = voter

    def register_voters(self, voters):
        for v in voters:
            self.register_voter(voters[v])

    def voter_voted(self, voterID):
        '''
        Set the voted flag for the voter to True. If they're not registered or already voted,
        raise an exception
        '''

        if voterID in self.registered_voters:
            if not self.registered_voters[voterID].voted:
                self.registered_voters[voterID].voted = True
            else:
                raise VoterException('Voter %s has already voted!' % voterID)
        else:
            raise VoterException('Voter %s is not registered!' % voterID)

    def has_voter_voted(self, voterID):
        '''
        Returns whether or not the voter has voted. Raises exception if not registered
        '''
        if voterID in self.registered_voters:
            return self.registered_voters[voterID].voted
        else:
            raise VoterException('Voter %s is not registered!' % voterID)

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
        if voter.voterID not in self.registered_voters:
            return False
        return True

    def blind_sign(self, vote):
        '''
        TBD
        '''
        return bs.signature(vote, self.private_signing_key)

    def decrypt_votes(self):
        '''
        final_tally: list of candidates with the final vote counts

        print out the number of votes for each candidate. 
        Requires that the votes have been encrypted with the generated public key
        '''

        unencrypted = []
        for candidate in self.candidates:
            if candidate.name not in self.candidate_names:
                raise CandidateException('Candidate in list not registered!')

            unencrypted.append(Candidate(candidate.name, decrypt(self.private_key, self.public_key, candidate.numVotes)))
        
        ## All candidates given to us are registered. Print stuff out now
        for candidate in unencrypted:
            print 'Number of votes for %s is %d'%(candidate.name, candidate.numVotes)

