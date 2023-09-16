# -*- coding: utf-8 -*-
"""
Created on Mon Feb 28 09:27:30 2022

@author: 1531402
"""
from math import log
import random
import sys

def read_frequencies():
    freq = {}
    f = open("ngrams.txt", 'r')
    for line in f:
        kline = line.split(" ")
        freq[kline[0].strip()] = int(kline[1].strip())
    return freq

ENGLISH_ALPH = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
FREQUENCY_LIST = read_frequencies()
POPULATION_SIZE = 500
NUM_CLONES = 3
TOURNAMENT_SIZE = 20
TOURNAMENT_WIN_PROBABILITY = .75
CROSSOVER_LOCATIONS = 7
MUTATION_RATE = 0.85

def encode(message, cipher_alphabet):
    message = message.upper()
    result = ""
    for ch in message:
        if(not ch.isalpha()):
            result+=ch
        else:
            result+=cipher_alphabet[ENGLISH_ALPH.index(ch)]
    return result

def decode(message, cipher_alphabet):
    message = message.upper()
    result = ""
    for ch in message:
        if(not ch.isalpha()):
            result+=ch
        else:
            result+=ENGLISH_ALPH[cipher_alphabet.index(ch)]
    return result

def fitness(n, message, cipher_alphabet):
    n_grams = []
    frequencies = []
    decoded = decode(message, cipher_alphabet)
    for i in range(len(decoded)):
        if(i+n<=len(decoded)):
           substring = decoded[i:i+n]
           if(substring.isalpha()):
               n_grams.append(substring)
    for n in n_grams:
        if(n in FREQUENCY_LIST):
            num = FREQUENCY_LIST[n]
            frequencies.append(log(num, 2))
    return sum(frequencies)

def generate_alph():
    alph = ""
    for i in range(26):
        num = random.randint(0, 25)
        while(ENGLISH_ALPH[num] in alph):
            num = random.randint(0, 25)
        alph+=ENGLISH_ALPH[num]
    return alph

def hill_climbing(text):
    cipher_alph = generate_alph()
    score = fitness(3, text, cipher_alph)
    currentscore = score
    currentresult = decode(text, cipher_alph)
    currentcipher = cipher_alph
    while(True):
        #swap two letters
        letter1 = random.randint(0, 25)
        letter2 = letter1
        while(letter2==letter1):
            letter2 = random.randint(0, 25)
        if(letter2>letter1):
            ciph = currentcipher[0:letter1] + currentcipher[letter2] + currentcipher[letter1+1:letter2] + currentcipher[letter1] + currentcipher[letter2+1:]
        else:
            ciph = currentcipher[0:letter2] + currentcipher[letter1] + currentcipher[letter2+1:letter1] + currentcipher[letter2] + currentcipher[letter1+1:]
        #test new alph
        score = fitness(3, text, ciph)
        if(score>currentscore):
            currentscore = score
            currentcipher = ciph
            currentresult = decode(text, currentcipher)
        print(currentresult)
        #if score is greater, that's the new alphabet
     
def breed(parent1, parent2):
    child = [None for i in range(26)]
    indexes = [i for i in range(26)]
    crossovers = random.sample(indexes, CROSSOVER_LOCATIONS)
    for i in range(len(crossovers)):
        child[crossovers[i]] = parent1[crossovers[i]]
    pardex = []
    for i in range(len(parent2)):
        if(not parent2[i] in child):
            pardex.append(parent2[i])
    par = 0
    for i in range(len(child)):
        if(child[i]==None):
            child[i] = pardex[par]
            par+=1
    s=""
    for i in range(len(child)):
        s+=child[i]
    return s

def mutate(child):
    indexes = [i for i in range(26)]
    swappers = random.sample(indexes, 2)
    letter1 = swappers[0]
    letter2 = swappers[1]
    if(letter2>letter1):
        ciph = child[0:letter1] + child[letter2] + child[letter1+1:letter2] + child[letter1] + child[letter2+1:]
    else:
        ciph = child[0:letter2] + child[letter1] + child[letter2+1:letter1] + child[letter2] + child[letter1+1:]
    return ciph
    
    
def genetic(text):
    population = []
    while(len(population)<POPULATION_SIZE):
        cciph = generate_alph()
        if(not cciph in population):
            population.append(cciph)
    for i in range(500):
        new_gen = []
        strategies_ranked = []
        strategies_dic = {}
        for strategy in population:
            fit = fitness(3, text, strategy)
            strategies_ranked.append((fit, strategy))
            strategies_dic[strategy] = fit
        strategies_ranked = sorted(strategies_ranked, reverse=True)
        print(decode(text, strategies_ranked[0][1]))
        print()
        #^^ greatest to least, best functions first
        for i in range(NUM_CLONES):
            new_gen.append(strategies_ranked[i][1])
        while(len(new_gen)<len(population)):
            tournament_all = random.sample(population, 2*TOURNAMENT_SIZE)
            tournament1 = []
            tournament2 = []
            for i in range(len(tournament_all)):
                if(i%2==0):
                    tournament1.append(tournament_all[i])
                else:
                    tournament2.append(tournament_all[i])
            t1strats = []
            t2strats = []
            for i in range(len(tournament1)):
                t1strats.append((strategies_dic[tournament1[i]], tournament1[i]))
                t2strats.append((strategies_dic[tournament2[i]], tournament2[i]))
            t1strats = sorted(t1strats, reverse=True)
            t2strats = sorted(t2strats, reverse=True)
            selectedstrat1 = None
            selectedstrat2 = None
            for i in range(len(t1strats)):
                if(random.random()<TOURNAMENT_WIN_PROBABILITY):
                    selectedstrat1 = t1strats[i][1]
                    break
            if(selectedstrat1==None): selectedstrat1 = t1strats[0][1]
            for i in range(len(t2strats)):
                if(random.random()<TOURNAMENT_WIN_PROBABILITY):
                    selectedstrat2 = t2strats[i][1]
                    break
            if(selectedstrat2==None): selectedstrat2 = t2strats[0][1]
            child = breed(selectedstrat1, selectedstrat2)
            if(random.random()<MUTATION_RATE): child = mutate(child)
            if(child not in new_gen): new_gen.append(child)
        population = new_gen
    
genetic(sys.argv[1])
#print(breed(ENGLISH_ALPH, "BACDZFGHIJLMKNQPROSTUVWXYE"))