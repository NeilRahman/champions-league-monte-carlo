#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  2 18:36:21 2022

@author: neil

This program uses Monte Carlo simulation to estimate the probabilities of each
possible Champions League R16 matchup for the 22/23 edition. The main trick is
with preventing locks since certain combinations are not allowed (same country
and group stage opponent). This is solved by recursive testing in each scenario
to identify all impossible draws.
"""

import random
import copy
import time
import pickle

country = {'Napoli':'Italy',
             'Liverpool':'England',
             'Porto':'Portugal',
             'Brugge':'Belgium',
             'Bayern':'Germany',
             'Inter':'Italy',
             'Spurs':'England',
             'Frankfurt':'Germany',
             'Chelsea':'England',
             'Milan':'Italy',
             'Real':'Spain',
             'Leipzig':'Germany',
             'City':'England',
             'Dortmund':'Germany',
             'Benfica':'Portugal',
             'PSG':'France'}
#will be used to prevent same-country pairings

seeded = ['Napoli', 'Porto', 'Bayern', 'Spurs', 'Chelsea', 'Real', 'City', 'Benfica']
unseeded = ['Liverpool', 'Brugge', 'Inter', 'Frankfurt','Milan','Leipzig','Dortmund','PSG']
#will be used to prevent same-group pairings

'''
planning to add some UI so that this program can be used for any collection of teams
(i.e. for later editions of the Champions League)
'''
    
def test(options, remaining, i, j):
    
    '''

    Parameters
    ----------
    options : list[list[int]]
        matrix of 0s and 1s that represents permitted pairings
    remaining : list[int]
        a list of integers corresponding to unseeded teams yet to be drawn
    i : int
        integer corresponding to unseeded team currently being tested
    j : int
        integer corresponding to seeded team currently being tested

    Returns
    -------
    bool
        boolean for if a full draw is still possible with this pairing

    '''
    
    global memory #dynamic programming cache
    global hit
    global miss
    
    option_hash = tuple(tuple(l) for l in options) #lists converted into tuples so they can be hashed
    rem_hash = tuple(remaining)
    if option_hash in memory and rem_hash in memory[option_hash] and (i,j) in memory[option_hash][rem_hash]:
        hit += 1 #i.e. cache hit
        return memory[option_hash][rem_hash][(i,j)]
    miss += 1
    
    if option_hash not in memory:
        memory[option_hash] = dict() #constructing missing paths in cache
    if rem_hash not in memory[option_hash]:
        memory[option_hash][rem_hash] = dict()
        
    if not options[i][j] or i not in remaining:
        memory[option_hash][rem_hash][(i,j)] = False
        return False
    if len(remaining) == 1:
        memory[option_hash][rem_hash][(i,j)] = True
        return True
    
    options = copy.deepcopy(options)
    for k in range(8):
        options[k][j] = 0
    remaining = remaining[:]
    remaining.remove(i)
    
    origi = i
    origj = j
    i = remaining[0]
    for j in range(8):
        if test(options, remaining, i, j):
            memory[option_hash][rem_hash][(origi,origj)] = True
            return True
    memory[option_hash][rem_hash][(origi,origj)] = False
    return False

while True:
    print('Welcome to the Champions League R16 Draw Monte Carlo Simulator!\n' +
      '\nWould you like to use past data if it exists? Y/N\n'+
      '\n(This would be stored in a file called "cldynamicdata.pkl")')
    past_data = input('\n').lower().strip()
    if past_data in 'yn':
        break
    print('Please type only "Y" or "N"!')

try:
    if past_data == 'n':
        raise AssertionError()
    fobj = open('cldynamicdata.pkl', 'rb')
    memory = pickle.load(fobj)
    fobj.close()
except:
    memory = dict()
 
while True:
    print('\nHow many simulations would you like to run?')
    try:
        num_sim = int(input('\n'))
        break
    except:
        print('\nPlease enter an integer!')
   
start = time.time() #see how long it took

hit = 0 #how many paths were found in memory
miss = 0 #how many paths were newly generated

probs = [[0]*8 for i in range(8)]

state = 0 #for progress checks just to reassure that it's not hanging

checks = [num_sim/10, num_sim/4, num_sim/2, 3*num_sim/4, num_sim]
percentages = [10, 25, 50, 75]

for dummy in range(num_sim):
    
    if dummy > checks[state]:
        print('\n' + str(percentages[state]) + '% complete!')
        state += 1
    
    options = [[1]*8 for i in range(8)] #constructing boolean matrix
    for i in range(8):
        first = unseeded[i]
        for j in range(8):
            second = seeded[j]
            if country[first] == country[second]:
                options[i][j] = 0 #teams from the same country cannot play each other in the R16
        options[i][i] = 0
        #the seeded and unseeded lists were lined up to match teams by group,
        #who cannot play against each other
        
    draw = [i for i in range(8)] #represents the unseeded teams
    while draw:
        i = random.randint(0, len(draw)-1)
        i = draw[i]
        for j in range(8):
            if not test(options, draw, i, j):
                options[i][j] = 0 #remove all options that will result in a lock
        ct = random.randint(1, options[i].count(1))
        j = -1
        while ct:
            j += 1
            if options[i][j] == 1:
                ct -= 1
        for k in range(8):
            options[k][j] = 0
        draw.remove(i)
        probs[i][j] += 1 #using the fundamental law of valid outcomes / total outcomes
        
print('\n100% complete!')

for i in range(8):
    for j in range(8):
        probs[i][j] /= (num_sim//100)
        
probs.insert(0, [''] + seeded) #for formatting purposes
for i in range(8):
    probs[i+1].insert(0, unseeded[i])
    for j in range(8):
        probs[i+1][j+1] = str(round(probs[i+1][j+1], 2)) + '%'
              
def standardize(list_of_s):
    
    '''
    
    Parameters
    ----------
    list_of_s : TYPE
        one-dimensional list of strings to be formatted

    Returns
    -------
    new_s : string
        formatted string for pretty printing

    '''
    
    new_s = ''
    for s in list_of_s:
        new_s += s + (15-len(s))*' '
    return new_s

print('')
for row in probs:
    print(standardize(row))

if past_data == 'y':
    print('\n' + str(hit) + ' tested paths were found in past data\n')
    print(miss, 'tested paths were new')

print('\nThe simulation took approximately', int(time.time()-start), 'seconds')

while True:
    print('\nWould you like to save the dynamic data to "cldynamicdata.pkl"' +
          ' for faster use in later simulations? Y/N' +
          '\n\nWARNING: If you previously chose to not use past data, this option will overwrite' +
          ' any past data with just the memory from these trials!')
    new_data = input('\n').lower().strip()
    if new_data in 'yn':
        break
    print('\nPlease type only "Y" or "N"!')

if new_data == "y":
    fobj = open('cldynamicdata.pkl', 'wb')
    pickle.dump(memory, fobj)
    fobj.close()