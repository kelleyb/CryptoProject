from paillier import *
from candidate import *
from voter  import *
from election_board import *
import sys
import traceback


voters = {}
for line in open('voters.txt'):
    parsed = line.strip().split(',')
    voters[parsed[1].strip()] = Voter(parsed[0],parsed[1])

eb = ElectionBoard(voters)

candidates = []
for line in open("candidates.txt"):
    eb.register_candidate(Candidate(line.strip(), encrypt(eb.public_key, 0)))
    candidates.append(Candidate(line.strip(), encrypt(eb.public_key, 0)))

print 'Candidates:'

for c in range(len(candidates)):
    print '    %d) %s' % (c + 1, candidates[c].name)


votes = []
while True:
    user_input = raw_input('Enter command (VOTE or END) => ').lower()
    if user_input == 'end' or user_input == 'e':
        for voter_vote in votes:
            for i in range(len(candidates)):
                candidates[i].numVotes = e_add(eb.public_key,candidates[i].numVotes,voter_vote[i])
        break

    if user_input == 'vote' or user_input == 'v':
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

                votes.append(u_vote)
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


eb.decrypt_votes(candidates)