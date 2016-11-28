from paillier import *
from candidate import *

#fucking around with shit


priv, pub = generate_keypair(128) 


raw_candidates = ["Trump","Clinton","Gary J","Jill Crazy Stein"]
candidates = []
for candidate in raw_candidates:
    candidates.append(Candidate(candidate))
print candidates
votes = []
while True:
    user_input = raw_input("Enter command (VOTE or END) => ")
    if user_input == "END":
        for voter_vote in votes:
            for i in range(len(candidates)):
                if candidates[i].numVotes == 0:
                    candidates[i].numVotes = voter_vote[i]
                else:
                    candidates[i].numVotes = e_add(pub,candidates[i].numVotes,voter_vote[i])

                    

        break
    if user_input == "VOTE":
        user_vote = []
        for key in candidates:
            c_vote = int(raw_input("Do you vote for %s? Enter either 1 or 0 => "%key.name))
            user_vote.append(encrypt(pub, c_vote))
        votes.append(user_vote)

for candidate in candidates:
    print "Number of votes for %s is %d"%(candidate.name, decrypt(priv,pub,candidate.numVotes))