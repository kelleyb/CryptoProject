from paillier import *
from candidate import *
from voter  import *
from election_board import *
from bulletin_board import *
import blind_signature as bs
import sys
import os

import traceback

## Get an instance of the election board
eb = ElectionBoard.Instance()
bb = BulletinBoard.Instance()
ca = CountingAuthority.Instance()
## Register voters and candidates
voters = {}
for line in open('voters.txt'):
    parsed = line.strip().split(',')
    voters[parsed[1].strip()] = Voter(parsed[0].strip(),parsed[1].strip())

candidates = []
for line in open("candidates.txt"):
    candidates.append(Candidate(line.strip(), encrypt(eb.public_key, 0)))

eb.register_voters(voters)
eb.register_candidates(candidates)

votes = []
while True:
    print 'Candidates:'

    for c in range(len(candidates)):
        print '    %d) %s' % (c + 1, candidates[c].name)
    user_input = raw_input('Enter command (VOTE or END) => ').lower()
    if user_input == 'end' or user_input == 'e':
        # for voter_vote in votes:
        #     for i in range(len(candidates)):
        #         candidates[i].numVotes = e_add(eb.public_key,candidates[i].numVotes,voter_vote[i])
        # break
        bb.endElection()
        break

    if user_input == 'vote' or user_input == 'v':

        voterID = raw_input('Enter your voter ID => ')

        if voterID in voters:
            if not eb.has_voter_voted(voterID):
                print 'Enter the ID of the candidate you want to vote for (1-%d)' % (len(candidates)),
                while True:
                    try:
                        print '==>',
                        vote = int(raw_input()) - 1

                        if vote not in xrange(0, len(candidates)):
                            print 'Please enter a number between 1 and %d' % len(candidates),

                        u_vote = []
                        for c in range(len(candidates)):
                            v = 0
                            if vote == c:
                                v = 1
                            # print encrypt(eb.public_key, v)
                            u_vote.append(encrypt(eb.public_key, v))

                        blind_signed_vote = []
                        for v in u_vote:
                            ## We want to blind sign each vote. So blind it, 
                            blinding_factor, blinded_msg = bs.blind(v, eb.public_signing_key)
                            signed = eb.blind_sign(blinded_msg)
                            unblinded = bs.unblind(signed, blinding_factor, eb.public_signing_key)
                            blind_signed_vote.append((unblinded, blinding_factor))

                        if not eb.has_voter_voted(voterID):
                            bb.addVote(voterID, u_vote, blind_signed_vote)
                            os.system('cls' if os.name == 'nt' else 'clear')
                        
                        break

                    except ValueError:
                        ## Goddamn users, trying to break our system
                        print 'Please enter a number between 1 and %d.' % len(candidates),

                    except KeyboardInterrupt:
                        # kbye
                        print '\nExiting'
                        sys.exit(1)

                    except:
                        print 'Dammit, you broke our program in an unexpected way. Good for you. Send this to a programmer:'
                        traceback.print_exc()
                        sys.exit(1)
            else:
                print 'You have already voted'
        else:
            print "You are not a registered voter"


# eb.decrypt_votes(candidates)
