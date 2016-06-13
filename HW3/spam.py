from collections import Counter
from math import log

spamTraining = []   #a list of spam emails' names
hamTraining = []
spamWrds = {}       # a dictionary, w/ words in spam emails and their occurance time
hamWrds = {}
spamLike = {}       # a dictionary, w/ words in spam emails and their likelihood
hamLike = {}
totalSpamWord = 0
totalHamWord = 0
k = 40
m = 50

probSpam = 0
probHam = 0

spamTesting = []
hamTesting = []


def setFileNameLst():
    global spamTraining,hamTraining,spamTesting,hamTesting
    fileName = "spamtraining.txt"
    spamTrainFile = open(fileName,"r")
    for line in spamTrainFile:
        spamTraining.append(line.rstrip('\n'))
    fileName = "hamtraining.txt"
    hamTrainFile = open(fileName,"r")
    for line in hamTrainFile:
        hamTraining.append(line.rstrip('\n'))

def readWords(trainingLst):
    c = Counter()
    totalWord = 0
    tmpWrdLst = []
    for i in trainingLst:
        tmpFile = open(i,"r")
        for word in tmpFile.read().split():
            # tmpWrdLst.append(word)
            # totalWord += 1
            if word.isalpha():
                tmpWrdLst.append(word)
                totalWord += 1
    for word in tmpWrdLst:
        c[word] += 1
    tmp = {}
    for key,value in c.iteritems():
        if c[key] > k:
            tmp.update({key:value})
    return tmp,totalWord

def calcLike(dict,wrdCount):
    tmp = {}
    for key,value in dict.iteritems():
        tmp.update({key:(float(value) / wrdCount)})
    return tmp

def calcSmoothLike(dict,wrdCount):
    tmp = {}
    for key,value in dict.iteritems():
        tmp.update({key:((float(value)+m) / (wrdCount + m * wrdCount))})
    return tmp

def readTestEmail(testEmail):
    fileName = testEmail
    testEmail = open(fileName,"r")
    testWrdLst = []
    c = Counter()
    totalWord = 0
    for word in testEmail.read().split():
    #     testWrdLst.append(word)
    #     totalWord += 1
        if word.isalpha():
            testWrdLst.append(word)
            totalWord += 1
    for word in testWrdLst:
        c[word] += 1
    tmp = {}
    for key,value in c.iteritems():
        tmp.update({key:(float(value) / totalWord)})
    return tmp

def posteriorSpam(wrdLst,sLikelihood):
    global probSpam
    postValue = log(probSpam)
    for key in wrdLst:
        if key in sLikelihood:
            postValue += log(sLikelihood[key])
    return postValue

def posteriorHam(wrdLst,hLikelihood):
    global probHam
    postValue = log(probHam)
    for key in wrdLst:
        if key in hLikelihood:
            postValue += log(hLikelihood[key])
    return postValue

def classification(wrdLst,sLikelihood,hLikelihood):
    tmpS = posteriorSpam(wrdLst,sLikelihood)
    tmpH =posteriorHam(wrdLst,hLikelihood)
    if tmpS > tmpH :
        return "spam"
    else:
        return "ham"

def scanALot(sLikelihood,hLikelihood):
    result = {}
    sTest = []
    spamCount = 0
    fileName = "spamtesting.txt"    # star
    spamTrainFile = open(fileName,"r")
    for line in spamTrainFile:
        sTest.append(line.rstrip('\n'))
    for i in sTest:
        tmpDict = readTestEmail(i)
        emailType = classification(tmpDict,sLikelihood,hLikelihood)
        if (emailType == "spam"):
            spamCount += 1
        result.update({i:emailType})
    print "totalCount:",len(sTest)
    print "spamCount:",spamCount
    print "hamCount:",100 - spamCount
    return result

def main():
    setFileNameLst()
    print spamTraining
    spamWrds,totalSpamWord = readWords(spamTraining)
    print spamWrds
    hamWrds,totalHamWord = readWords(hamTraining)
    print hamWrds
    print "totalSWord:", totalSpamWord
    print "totalHW:", totalHamWord
    spamLike = calcLike(spamWrds,totalSpamWord)
    hamLike = calcLike(hamWrds,totalHamWord)
    print spamLike
    print hamLike
    sNum = len(spamTraining)
    hNum = len(hamTraining)
    global probSpam,probHam
    probSpam = float(sNum)/ (sNum+hNum)
    probHam = float(hNum)/ (sNum+hNum)
    print probSpam, probHam
    print "========================================"
    spamSmooL = calcSmoothLike(spamWrds,totalSpamWord)
    hamSmooL = calcSmoothLike(hamWrds,totalHamWord)
    print spamSmooL
    print hamSmooL
    print "========================================"
# ===========================================================================
    testResult = scanALot(spamSmooL,hamSmooL)
    print testResult

if __name__ == '__main__':
    main()
