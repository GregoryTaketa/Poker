# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 14:25:14 2017

@author: greg_000
"""

import random
import re #regular expressions

#NUMBER OF STARTING PLAYERS
starting_players = int(input("Welcome to the 5-Card Draw Simulation!  How many Players (2 to 8)? "))
while starting_players < 2 or starting_players > 8:
    starting_players = int(input("Very funny.  Pick a number of 2 to 8. "))
starting_players_list = list(range(0,starting_players))

#Form the 54-card Deck
def form_deck():
    """Form 54 Cards"""
    numbers = list(range(2,11))
    faces = ["J", "Q", "K", "A"]
    values = numbers + faces
    suites = ["D", "C", "H", "S"]
    new_deck = [(v,s) for s in suites for v in values]
    new_deck.append(('Joker','Black'))
    new_deck.append(('Joker','Color'))
    return new_deck

#Store form_deck() results as new_deck to reset deck w/o re-running
new_deck = form_deck()

#Computer's propensity to Fold
they_fold = 0.35

#Form option to Fold
def fold ():
    global folded
    global players
    removal = []
    for player in players:
        if len(players)-len(removal) == 1: #len(players) does not update with each iteration of this loop, it seems.  But removal does.
            print("Player ", str(player+1)," wins.")
            break
        #You decide whether to fold
        elif player == you:
            you_fold = input("Do you want to fold (y/n)? ")
            if you_fold == 'y':
                print("You have folded from this game.")
                folded.append(player+1)
                #players.remove(player) #Skips you when previous player folds.
                removal.append(player)
        #Computers randomly fold based on pre-determined propensity
        else:
            if random.random() < they_fold:
                print("Player ",str(player+1)," has folded.")
                folded.append(player+1)
                #players.remove(player)
                removal.append(player)
    #Separate for loop for removing players because previous version skips you when previous players is removed.
    for person in removal:
        players.remove(person)
    return players, folded

def deal ():
     """Deal 1st hand."""
     global all_hands
     global deck
     global players
     
     #Set of all cards for the first hands   
     first_draws = random.sample(deck, len(players)*5)
     #Remove drawn cards from deck
     for card in first_draws:
            deck.remove(card)
    #Deal 1 Card Each Player Until 5.  
     for player in players:
        hand = []
        for i in range(0,5):
            hand.append(first_draws[player+len(players)*i])
        all_hands.append(hand)
    
    #Only you can see your hand.
     print("Your hand is: ", str(all_hands[you]))
    
def draw():
    """Discard up to 3 cards (or 4 if possessing an Ace or Joker).  Then re-draw."""
    global all_hands
    global deck
    global discard
    global players
    
    for player in players:
        if player != you:
            high = 0 #initialize to count Aces or Jokers to discard up to 4
    #Count Aces and Jokers to discard up to 4
            for card in all_hands[player]:
                if card[0] == 'A' or card[0] == 'Joker':
                    high = high + 1
            if high > 0:
                i = 4
            else:
                i = 3
            
            #Randomly decide number to replace depending on constraint and then discard
            quantity_replace = random.randrange(0,i+1)
            replace = random.sample(all_hands[player],quantity_replace)
            for card in replace:
                discard.append(card)
                print("Player ", str(starting_players_list[player+1]),"discards ", str(card))
                all_hands[player].remove(card)
            
            #Re-draw but combine discard with deck if deck empty
            for j in range(0,quantity_replace):
                if len(deck) == 0:
                    for card in discard:
                        deck.append(card)
                    discard = []
                new_card = random.sample(deck, 1)
                all_hands[player].append(new_card[0])
                deck.remove(new_card[0])
            print("")
                
        else: #i.e. the player is you
            high = 0 #initialize to count Aces or Jokers to discard up to 4
    #Count Aces and Jokers to discard up to 4
            for card in all_hands[player]:
                if card[0] == 'A' or card[0] == 'Joker':
                    high = high + 1
            if high > 0:
                i = 4
            else:
                i = 3
            print("You may discard up to ", str(i), " cards.")
            print("Discard Pile: ", str(discard))
            print("")
            for index, value in enumerate(all_hands[player]):
                print(index, value)
            print("")
            user_response = input("Enter the numbers left of any card(s) you wish to replace via the 2nd draw (e.g. 0, 2, 4 or 0 2 4)  ")
            print("")
            user_list = re.sub("[^\w]", " ",  user_response).split() #substitute non (^) anything (\) alphanumeric (w) with " " from user_response, then split by spaces by default
            choice_list = []
            for i in user_list:
                choice_list.append(int(i)) #creating integer list from user inputs
            choice_list.sort(reverse=True) #remove from rear first to avoid changing index during for loop
            for j in choice_list:
                print("Discarding " + str(all_hands[player][j]))
                print("")
                discard.append(all_hands[player][j])
                all_hands[player].remove(all_hands[player][j])
            
            for a in range(0, len(choice_list)):
                if len(deck) == 0:
                    for card in discard:
                        deck.append(card)
                    discard = []
                new_card = random.sample(deck, 1)
                all_hands[player].append(new_card[0])
                deck.remove(new_card[0])
            print("Your Hand: ",str(all_hands[player]))
            print("")

go = 'y'
while go != 'n':
    players = list(starting_players_list) #Reset the number of players
    you = random.randrange(0,len(players))  #Reset your position
    print("")
    print("This game, you are Player ", str(you+1))
    print("")
    folded = [] #Reset the folded players
    deck = list(new_deck) #Reset the deck
    all_hands = [] #Reset the hands
    discard= [] #Reset the discard pile
    deal()
    print("")
    fold()
    print("Folded Players: ",str(folded))
    print("")
    if len(players) > 1:
        draw()
        fold()
    for player in players:
        if player == you:
            print("Last Round Player: ",str(player+1),"(you)")
        else:
            print("Last Round Player: ",str(player+1))
    for final_hand in all_hands:
        print("Player ", str(all_hands.index(final_hand)+1),"'s Hand: ", str(final_hand))
    print("Discard pile: ", str(discard))
    go = input("Wanna play again (y/n)? ") #Since the 'Enter' key is not 'n', you could just hit 'Enter' to draw again lazily.
    print("")

  