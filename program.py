from cmd import PROMPT
import sys
import os
import math
import operator
from collections import Counter
import random

fileToTextDict= {}

def main(funcToCall, query):
    initializeDict()
    query= query.lower()
    print "searching for documents most relative to: "+ query
    scoreArr=[]
    
    if(funcToCall == "bm"):
        avgdl = getAvgdl()
        scoreArr= map(lambda docName: (docName, BM25ScoringFunction(docName, query, avgdl)), fileToTextDict.keys())
#     elif(funcToCall == "ng"):
#         scoreArr.append((doc, NGrams(doc, query)))
#     elif(funcToCall == "ta"):
#         scoreArr.append((doc, TextualAlignment(doc, query)))
    printTopTen(scoreArr)

def initializeDict():
    presDirPath= os.getcwd()+"/Presidents"
    fileList = os.listdir(presDirPath)
    for file in fileList:
        fileToTextDict[file]= open(presDirPath+"/"+file).read().replace('\n', '').lower() 
        
def BM25ScoringFunction(docName, queryWords, avgdl):
    vals=[]
    doc= fileToTextDict[docName]
    for word in queryWords.split(' '):
        idf= getIDF(word)
        termFrequency= Counter(doc.split(' '))[word]
        k1= 2#random.choice([1.2, 2])
        b= .75
        
        numerator= termFrequency*(k1+1)
        denom= termFrequency+ k1 * (1-b+b* (getDocLengthWords(doc)/avgdl))
        vals.append(idf*(numerator/denom))
    return sum(vals)

def getDocLengthWords(doc):
    return len(doc.split(' '))

def getAvgdl():
    return sum(map(lambda doc: getDocLengthWords(doc), fileToTextDict.values()))/len(fileToTextDict.keys())
    
def getIDF(word):
    nq= len([x for x in fileToTextDict.values() if word in x])
    idf=  math.log((len(fileToTextDict.keys())- nq + .5)/(nq+.5))
    return idf
    
def NGrams(doc, query):
    return 0    
    
def TextualAlignment(doc, query):
    return 0

def printTopTen(scoreArr):
    print sorted(scoreArr, key=operator.itemgetter(1))[::-1][:10]
    
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])