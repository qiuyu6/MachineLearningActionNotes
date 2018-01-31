
from numpy import *

def main():
  spamTest()

def trainNB0(trainMatrix, trainCategory):
  numTrainDocs = len(trainMatrix)
  numWords = len(trainMatrix[0])
  pAbusive = sum(trainCategory) / float(numTrainDocs)
  #initialize probabilities
  p0Num = ones(numWords)
  p1Num = ones(numWords)
  p0Demon = 2.0
  p1Demon = 2.0
  for i in range(numTrainDocs):
    if trainCategory[i] == 1:
      p1Num += trainMatrix[i]
      p1Demon += sum(trainMatrix[i])
    else:
      p0Num += trainMatrix[i]
      p0Demon += sum(trainMatrix[i])
  p1Vect = log(p1Num/p1Demon)
  p0Vect = log(p0Num/p0Demon)
  return p0Vect, p1Vect, pAbusive

def classifyNB(vec2Classify, p0Vec, p1Vec, pClass1):
  p1 = sum(vec2Classify * p1Vec) + log(pClass1)
  p0 = sum(vec2Classify * p0Vec) + log(1.0 - pClass1)
  if p1 > p0:
    return 1
  else:
    return 0

def testingNB():
  listOfPosts, listClasses = loadDataset()
  myVocabList = createVocabList(listOfPosts)
  trainMat = []
  for postinDoc in listOfPosts:
    trainMat.append(setOfWords2Vec(myVocabList, postinDoc))
  p0V,p1V,pAb = trainNB0(array(trainMat), array(listClasses))
  testEntry = ['love','my','dalmation']
  thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
  print testEntry,'classified as: ',classifyNB(thisDoc, p0V, p1V, pAb)
  testEntry = ['stupid','garbage']
  thisDoc = array(setOfWords2Vec(myVocabList, testEntry))
  print testEntry,'classified as: ',classifyNB(thisDoc, p0V, p1V, pAb)

def textParse(bigString):
  import re
  listOfTokens = re.split(r'\W*', bigString)
  return [tok.lower() for tok in listOfTokens if len(tok) > 2]

def bagOfWords2VecMN(vocabList, inputSet):
  returnVec = [0]*len(vocabList)
  for word in inputSet:
    if word in vocabList:
      returnVec[vocabList.index(word)] += 1
  return returnVec

def createVocabList(dataset):
  vocabSet = set([])
  for document in dataset:
    vocabSet = vocabSet | set(document)
  return list(vocabSet)

def setOfWords2Vec(vocabList, inputSet):
  returnVec = [0]*len(vocabList)
  for word in inputSet:
    if word in vocabList:
      returnVec[vocabList.index(word)] = 1
    else: print "the word: %s is not in my vocabulary!" % word
  return returnVec

def spamTest():
  docList = []
  classList = []
  fullText = []
  #load and parse text files
  for i in range(1,26):
    wordList = textParse(open('email/spam/%d.txt' % i).read())
    docList.append(wordList)
    fullText.extend(wordList)
    classList.append(1)
    wordList = textParse(open('email/ham/%d.txt' % i).read())
    docList.append(wordList)
    fullText.extend(wordList)
    classList.append(0)
  vocabList = createVocabList(docList)
  trainingSet = range(50)
  testSet = []
  #randomly create the training set
  for i in range(10):
    randIndex = int(random.uniform(0, len(trainingSet)))
    testSet.append(trainingSet[randIndex])
    del(trainingSet[randIndex])
  trainMat = []
  trainClasses = []
  for docIndex in trainingSet:
    trainMat.append(setOfWords2Vec(vocabList, docList[docIndex]))
    trainClasses.append(classList[docIndex])
  p0V,p1V,pSpam = trainNB0(array(trainMat),array(trainClasses))
  errorCount = 0
  #classify the test set
  for docIndex in testSet:
    wordVector = setOfWords2Vec(vocabList, docList[docIndex])
    if classifyNB(array(wordVector), p0V, p1V, pSpam) != classList[docIndex]:
      errorCount += 1
  print 'the error rate is: ', float(errorCount) / len(testSet)

if __name__ == '__main__':
  main()