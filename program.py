from cmd import PROMPT
import sys
import os
import operator

from macpath import realpath
from random import random

dictArr= [];

def main(funcToCall, query):
    initializePresidentsArr()
    print "searching for documents most relative to: "+ query
    if(funcToCall == "bm"):
        BM25ScoringFunction()
    elif(funcToCall == "ng"):
        NGrams()
    elif(funcToCall == "ta"):
        TextualAlignment()
    printTopTen()

def initializePresidentsArr():
    fileList = os.listdir(os.getcwd()+"/Presidents")
    for file in fileList:
        dictArr.append((file, 0))
        
def BM25ScoringFunction():
    print "bm25"
    
def NGrams():
    print "ngrams"
    
    
def TextualAlignment():
    print "textAlign"

def printTopTen():
    print sorted(dictArr, key=operator.itemgetter(1))[:10]
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])