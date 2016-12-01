#!/usr/bin/python
from paillier import *
from candidate import *
from voter  import *
from election_board import *
from bulletin_board import *
import sys
import os

from Tkinter import * 
import traceback



def submitVote():
    global userPick
    global userPIN
    # print voters
    if str(userPIN.get()).strip() in voters and (userPick.get()) != '':
        if not voters[str(userPIN.get()).strip()].voted:
            u_vote = []
            for c in range(len(candidates)):
                v = 0
                if int(userPick.get()) == c:
                    v = 1
                u_vote.append(encrypt(eb.public_key, v))

            blind_signed_vote = []
            for v in u_vote:
                ## We want to blind sign each vote. So blind it, 
                blinding_factor, blinded_msg = bs.blind(v, eb.public_signing_key)
                signed = eb.blind_sign(blinded_msg)
                unblinded = bs.unblind(signed, blinding_factor, eb.public_signing_key)
                blind_signed_vote.append((unblinded, blinding_factor))

            if not eb.has_voter_voted(str(userPIN.get().strip())):
                bb.addVote(userPIN.get().strip(), u_vote, blind_signed_vote)

            voters[str(userPIN.get()).strip()].voted = True
            userPick = StringVar()
            userPIN = StringVar()
            toplevel.destroy()

def castVote():
    global canCast
    if canCast:
        
        global toplevel 

        toplevel = Toplevel()
        toplevel.geometry("600x800+200+200")
        toplevel.focus_force()
        label = Label(toplevel, text="Enter your voting ID", height=0, width=100)
        label.pack()
       
        e = Entry(toplevel,textvariable=userPIN)
        e.pack()

        

        for c in range(len(candidates)):
             b = Radiobutton(toplevel, text=candidates[c].name, variable=userPick, value=c)
             b.pack(anchor=W)
        toplevel.focus_force()
        b = Button(toplevel, text="Submit Vote", width=20, command=submitVote)
        b.pack(side='bottom',padx=0,pady=0)

def endVoting():
    global isOver
    global canCast
    global b
    global button1

    if not isOver:
    
        isOver = True
        canCast = False
        e = bb.endElection()
        final = ''
        global resultsLabel
        for candidate in e:
            final += 'Number of votes for %s is %d\n'%(candidate.name, candidate.numVotes)
        resultsLabel  = Label(app, text=final, height=0, width=100)
        resultsLabel.pack()

        b.pack_forget()
        button1.pack_forget()




if __name__ == "__main__":
      
## Get an instance of the election board
    isOver = False
    canCast = True
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

    app = Tk()
    toplevel = None
    app.title("Totally Secure and Legit Voting Machine 3000")
    app.geometry("300x200+200+200")
    userPick = StringVar()
    userPIN = StringVar()

    resultsLabel = None
    b = Button(app, text="End Voting", width=20, command=endVoting)
    button1 = Button(app, text="Cast Your Vote", width=20, command=castVote)
    
    b.pack(side='bottom',padx=0,pady=0)
    button1.pack(side='bottom',padx=5,pady=5)

    app.mainloop() 


   