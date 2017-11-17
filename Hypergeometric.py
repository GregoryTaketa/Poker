# -*- coding: utf-8 -*-
"""
Created on Wed Nov 15 18:21:44 2017

@author: greg_000

"""
#CARD COMBINATIONS

#Automated Hypergeometric Distribution (drawn without replacement) for more than 2 Categories, if desired.  While Probability Distribution Functions (PDFs) and Cumulative Distribution Functions (CDFs) for 2 Categories work readily in calculators and Excel, doing CDFs beyond 2 categories could be cumbersome without control loops.

from math import factorial as fact
from functools import reduce
import operator
import re
import itertools

def nCr(n, r):
    """Get nCr combinations"""
    combination = fact(n)/(fact(r)*fact(n-r))
    return combination
    
def prod(iterable):
    """Get the product of a list.  Will use to get the product of a list of combinations to get the numerator of the PDF."""
    return reduce(operator.mul, iterable, 1)
    
def PDF (populations, hand):
    """Get Probability Distribution Function, or probability of exactly those quantities of cards in your hand."""
    categories = list(zip(populations, hand))

    category_combos = []
    for combin in categories:
        category_combos.append(nCr(combin[0],combin[1]))

    pdf = prod(category_combos)/nCr(deck_size, hand_size)
    print("The probability of exactly ",str(hand)," is ",str(pdf))
    return pdf

deck_size = int(input("How many cards in the deck? "))

hand_size = int(input("How many cards will you draw into the hand? "))

population_inputs = input("How many cards in the deck qualify for each part of your combination?  For example, if you want a Poker hand of 3 Aces and 2 Queens (Full House), you would find 4 Aces and 4 Queens in a 52-card Deck.  You would input as '4, 4' or as '4 4': ")

populations_string = re.sub("[^\w]", " ", population_inputs).split() #substitute non (^) anything (\) alphanumeric (w) with " " from user_response, then split by spaces by default

populations = []
for i in populations_string:
    populations.append(int(i))

sample_inputs = input("How many cards do you want to draw for each part of your combination?  For example, if you want a Poker hand of 3 Aces and 2 Queens (Full House), you would input as '3, 2' or '3 2': ")

samples_string = re.sub("[^\w]", " ", sample_inputs).split() #substitute non (^) anything (\) alphanumeric (w) with " " from user_response, then split by spaces by default

samples = []
for j in samples_string:
    samples.append(int(j))
    
print("")
    
#GENERATE ALL POSSIBLE SAMPLE HANDS TO SATISFY CDF
category_limit = [] #initialize list for possible sample hands
sample_limit = hand_size - len(populations) + 1 #if all other categories get 1 card, then this is the maximum number of cards you can draw for a given category.
    
#Form Limits for Each Category
for k in populations:
    if k > sample_limit:
        category_limit.append(sample_limit)
    else:
        category_limit.append(k)
    
#Form a List of Ranges up to the Category Limits
category_ranges = []
for l in category_limit:
    category_ranges.append(list(range(1,l+1)))
        
#Some cards in the Deck may not qualify for any categories you input but could be drawn with your desired cards.
missing_pop = deck_size - sum(populations)
populations.append(missing_pop)
    
if missing_pop > 0:
    category_ranges.append(list(range(0,min(sample_limit,missing_pop)))) #The last element of category_ranges is the undesired stuff of which you can draw 0 or up to the sample limit or the population of undesired stuff, whichever is smaller.
    
#Form the Cartesian Product of all Hands up to Category Limits (tuples)
Cartesian_product = itertools.product(*category_ranges) #category_ranges is 1 list of lists, which does not work well with itertools.product.  Instead, we unpack category_ranges with * to produce list1, list2, list3, etc. which fit the iterable, iterable, iterable *args.  The output is a generator object.
    
#Of the Cartesian Product tuples formed above, only keep the ones which can feasibly form a hand.
feasible = []
for tuple in Cartesian_product:
   if sum(tuple) == hand_size:
       feasible.append(tuple)
    
#Of the feasible hands, only keep the ones which satisfy your requested minimum #s in the hand. 
combos = [] #initialize desired combinations   
for m in feasible:
    pass_count = 0 #count the times each tuple element satisfies the desired quantity.
    for n in range(0, len(samples)):
        if samples[n] <= m[n]:
            pass_count = pass_count + 1
    if pass_count == len(samples):
        combos.append(m)
    
#Get the probabilities of all those combos
pdf_probabilities = []
for hand in combos:
    pdf_probabilities.append(PDF(populations, hand))
        
cdf = sum(pdf_probabilities)

print("")
print("The probability of at least ", str(samples)," is ",str(cdf))
