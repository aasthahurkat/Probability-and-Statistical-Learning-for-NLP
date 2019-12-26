import os
import re
import math
import sys

def read(folder):
    f = open(folder, 'r', encoding='utf-8', errors='ignore')
    lines = f.readlines()
    for line in lines:
        for word in line.split():
            wordslist = word.strip().lower()
    f.close()
    return wordslist

spamtraining = "./train/spam"
spam = {}   
files = os.listdir(spamtraining)
for file in files:     
    words = read(spamtraining + '/' + file)
    for word in words: 
        if word in spam: 
            spam[word] = spam[word] + 1
        else: 
            spam[word] = 1

notspamtraining = "./train/notspam"
notspam = {}   
files = os.listdir(notspamtraining)
for file in files:     
    words = read(notspamtraining+'/'+ file)
    for word in words: 
        if word in notspam: 
            notspam[word] = notspam[word] + 1
        else: 
            notspam[word] = 1


def Probability(word,category):
    if category==spam:
        if word not in spam:
            spam[word] = 0
        numerator1= (spam[word]+1)
        denominator1= sum(spam.values()) + len(spam)
        prob = numerator1/denominator1
        return prob
    if category==notspam:
        if word not in notspam:
            notspam[word] = 0
        numerator1= (notspam[word]+1)
        denominator1= sum(notspam.values())+ len(notspam)
        prob = numerator1/denominator1
        return prob

def classifier(testfile, spam, notspam):
    testwords = read(testfile)
    PS = len(spam)/(len(spam)+len(notspam))
    PNS = len(notspam)/(len(spam)+len(notspam))
    spam_probability = 0
    notspam_probability = 0

    for word in testwords:
        spam_probability += math.log(Probability(word,spam))
        notspam_probability += math.log(Probability(word,notspam))
    
    spam_probability += PS
    notspam_probability+= PNS
    
    if spam_probability > notspam_probability:
        return 'spam'
    else:
        return 'notspam'


if __name__ == "__main__":
    if(len(sys.argv) != 4):
        raise Exception("usage: ./spam.py training-directory testing-directory output-file")
    

    test = sys.argv[2]
    notspamtraining =  sys.argv[1] + "/notspam"
    spamtraining =  sys.argv[1] + "/spam"
    testfiles = os.listdir(test)
    if os.path.exists(sys.argv[3]):
        os.remove(sys.argv[3]) #Delete output file with same name
    with open(sys.argv[3], "a") as outputFile:
        for file_spam in testfiles:
            result = classifier(test + "/" + file_spam, spam, notspam)
            print(file_spam, result)
            print(file_spam, result, file=outputFile)
