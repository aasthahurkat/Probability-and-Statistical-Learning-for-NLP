#!/usr/local/bin/python3
# CSCI B551 Fall 2019
#
# Authors: [Rohit Rokde-rrokde, Bhumika Agrawal-bagrawal, Aastha Hurkat-aahurkat]
#
# based on skeleton code by D. Crandall, 11/2019
#
# ./break_code.py : attack encryption
#

#Usage: python3 break_code.py encrypted-text-3.txt corpus.txt output

import random
import math
import copy 
import sys
import encode
import itertools
import concurrent.futures
import time
from heapq import heappop, heappush

# put your code here!
global_string = ""
solution_found = False
dictOfDict = {}

def break_code(string, corpus):
    global global_string
    global dictOfDict
    global_string = string
    # letters = list(range(ord('a'), ord('z')+1))
    # random.shuffle(letters)
    # replace_table = dict(zip(map(chr, range(ord('a'), ord('z')+1)), map(chr, letters)))
    counts = {'a':0, 'b':0, 'c':0, 'd':0, 'e':0, 'f':0, 'g':0, 'h':0, 'i':0, 'j':0, 'k':0,
            'l':0, 'm':0, 'n':0, 'o':0, 'p':0, 'q':0, 'r':0, 's':0, 't':0, 'u':0, 'v':0,
            'w':0, 'x':0, 'y':0, 'z':0}
    for i in counts.keys():
        dictOfDict[i] = copy.deepcopy(counts)
    #dictOfDict[' '] = copy.deepcopy(counts)

    for word in corpus.split(' '):
        if len(word) > 1:
            prev = word[0]
            for letter in word[1:]:
                dictOfDict[prev][letter] += 1
                prev = letter
    for previous in dictOfDict.keys():
        summ = 0
        for i in dictOfDict[previous].items():
            summ += i[1]
        for i in dictOfDict[previous].items():
            dictOfDict[previous][i[0]] /= summ
    #Below commented code used for debugging
    # import os
    # os.remove('dictOfDict')
    # import pickle
    # with open('dictOfDict', 'wb') as fp:
    #     pickle.dump(dictOfDict, fp)
    # with open ('dictOfDict', 'rb') as fp:
    #     dictOfDict = pickle.load(fp)
    rearrange_tables = list(itertools.permutations(list(range(0,4))))
    fringe = []
    heappush(fringe, (999, ""))
    #Following block is derived from https://docs.python.org/3/library/concurrent.futures.html
    with concurrent.futures.ThreadPoolExecutor(max_workers=len(rearrange_tables)+1) as executor:
        for rearrange_table, tuple_data in zip(rearrange_tables, executor.map(decrypt_function, rearrange_tables)):
    #Above block is derived from https://docs.python.org/3/library/concurrent.futures.html
            #print("Probability = ", tuple_data[1])
            #print("Message: ", tuple_data[0])
            probability = tuple_data[1]
            heappush(fringe, (1-probability, tuple_data[0]))
    (probability, decoded) = heappop(fringe)
    return decoded

def decrypt_function(rearrange_table):
    global solution_found
    global global_string
    global dictOfDict
    T = {'a':'a', 'b':'b', 'c':'c', 'd':'d', 'e':'e', 'f':'f', 'g':'g', 'h':'h', 'i':'i', 'j':'j', 'k':'k',
            'l':'l', 'm':'m', 'n':'n', 'o':'o', 'p':'p', 'q':'q', 'r':'r', 's':'s', 't':'t', 'u':'u', 'v':'v',
            'w':'w', 'x':'x', 'y':'y', 'z':'z'}
    #visited = {}
    #visited[str(T)] = 1
    decrypt_T_string = global_string
    while not solution_found:
        T_dash = switch(T)
    #    while str(T_dash) in visited.keys():
    #        T_dash = switch(T)
    #    visited[str(T_dash)] = 1

        decrypt_T_string = decode(global_string, T, rearrange_table)

        decrypt_T_dash_string = decode(global_string, T_dash, rearrange_table)

        total_count = 0
        T_probability = 0
        for decrypt_T in decrypt_T_string.split(' '):
            if len(decrypt_T) > 1:
                prev = decrypt_T[0]
                for letter in decrypt_T[1:]:
                    T_probability += dictOfDict[prev][letter]
                    prev = letter
                    total_count += 1
        T_probability = T_probability / total_count

        total_count = 0
        T_dash_probability = 0
        for decrypt_T_dash in decrypt_T_dash_string.split(' '):
            if len(decrypt_T_dash) > 1:
                prev = decrypt_T_dash[0]
                for letter in decrypt_T_dash[1:]:
                    T_dash_probability += dictOfDict[prev][letter]
                    prev = letter
                    total_count += 1
        T_dash_probability = T_dash_probability / total_count

        if T_probability < T_dash_probability:
            T = copy.deepcopy(T_dash)
            decrypt_T_string = decrypt_T_dash_string

        #Below commented code used for debugging
        # appd = str(rearrange_table).replace(',', '').replace('[', '').replace(']', '').replace(' ', '').replace('(', '').replace(')', '')
        # filename = "decoded_output_" + appd + ".txt"
        # with open(filename, "a") as file:
        #     print("Rearrangement table ", file=file)
        #     print(rearrange_table, file=file)
        #     print("Replacement table ", file=file)
        #     print(T, file=file)
        #     print(decrypt_T_string, file=file)
        #     print("\n", file=file)

        elapsed_time = time.time() - start_time
        if elapsed_time > 595:#Time should be less than 10 min. Kept a 5 second buffer so the program wraps up in time.
            solution_found = True
            return (decrypt_T_string, T_probability)

    #Maybe the solution was found in some other thread. So return the best estimate found in this thread.
    if solution_found:
        return (decrypt_T_string, T_probability)

def switch(T):
    T_dash = copy.deepcopy(T)
    replace_index1 = chr(random.randint(97,122))
    replace_index2 = chr(random.randint(97,122))
    while replace_index1 == replace_index2:
        replace_index2 = chr(random.randint(97,122))
    temp = T_dash[replace_index1]
    T_dash[replace_index1] = T_dash[replace_index2]
    T_dash[replace_index2] = temp
    return T_dash
# This function takes a string str, and encodes it using two
#  strategies: a replacement table, where every instance of each
#  character is replaced with another character (e.g. all a's 
#  replaced with b's), and a rearrangement table, in which
#  groups of n characters are rearranged (e.g., hello -> olhel)
#
# replace_table : This should be a has mapping characters to characters,
#                 e.g. { 'a':'q', 'b':'l', 'c':'m', ... }
#
# rearrange_table : This should be a permutation of the integers from
#                   0 to n-1. For example, (3, 2, 1, 0) would
#                   reverse every sequence of 4 characters, e.g.
#                   "csci is easy" -> "icsc si ysae"
#
def decode(str, replace_table, rearrange_table):
    # apply replace table
    str2 = str.translate({ ord(i):ord(replace_table[i]) for i in replace_table })

    # pad with spaces to even multiple of rearrange table
    str2 +=  ' ' * (len(rearrange_table)-(len(str2) %  len(rearrange_table)))

    # and apply rearrange table
    return "".join(["".join([str2[rearrange_table[j] + i] for j in range(0, len(rearrange_table))]) for i in range(0, len(str), len(rearrange_table))])

start_time = 0
if __name__== "__main__":
    start_time
    start_time = time.time()#Note down the start time of the program.
    if(len(sys.argv) != 4):
        raise Exception("usage: ./break_code.py coded-file corpus output-file")

    encoded = encode.read_clean_file(sys.argv[1])
    corpus = encode.read_clean_file(sys.argv[2])
    decoded = break_code(encoded, corpus)

    with open(sys.argv[3], "w") as file:
        print(decoded, file=file)
    print(decoded)
