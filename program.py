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
    elif(funcToCall == "ptm"):
        scoreArr= map(lambda docName: (docName, PassageTermMatch(docName, query)), fileToTextDict.keys())
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
        idf= getB25IDF(word)
        termFrequency= Counter(doc.split(' '))[word]
        #print docName +" qw:"+word+" idf: ", idf#termFrequency#" val:",(idf*(numerator/denom))
        
        k1= 2#random.choice([1.2, 2])
        b= .75
        
        numerator= termFrequency*(k1+1)
        denom= termFrequency+ k1 * ((1-b)+b* (getDocLengthWords(doc)/avgdl))
        vals.append(idf*(numerator/denom))
    return sum(vals)

def getDocLengthWords(doc):
    return len(doc.split(' '))

def getAvgdl():
    return sum(map(lambda doc: getDocLengthWords(doc), fileToTextDict.values()))/len(fileToTextDict.keys())
    
def getB25IDF(word):
    nq= len([x for x in fileToTextDict.values() if word in x.split(' ')])
    
    idf=  math.log((len(fileToTextDict.keys())- nq + .5)/(nq+.5))
    return idf

#===========================================================================================================================
    
def NGrams(doc, query):
    return 0    

#============================================================================================================================    

def PassageTermMatch(docName, query):
    w_ij_vals=map(lambda term: getPTMIDF(term) if (term in fileToTextDict[docName].split(' ')) else 0, query.split(' '))
    numer = sum(w_ij_vals)
    denom = sum(map(lambda term: getPTMIDF(term), query.split(' ')))
    
    return numer/denom if numer and denom != 0.0 else 0.0
    
def getPTMIDF(term):
    N= len(fileToTextDict.keys())
    ct= len([x for x in fileToTextDict.values() if term in x.split(' ')])
    return math.log(N/(ct+1))

def printTopTen(scoreArr):
    print sorted(scoreArr, key=operator.itemgetter(1))[::-1][:10]
    
if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])