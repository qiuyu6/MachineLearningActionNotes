from math import log

def calcShannonEnt(dataset):
	numEntries = len(dataset)
	labelCounts = {}
	for featVec in dataset:
		currentLabel = featVec[-1]
		if currentLabel not in labelCounts.keys():
			labelCounts[currentLabel] = 0
		labelCounts[currentLabel] += 1
	shannonEnt = 0.0
	for key in labelCounts:
		prob = float(labelCounts[key])/numEntries
		shannonEnt -= prob * log(prob, 2)
	return shannonEnt

def createDataset():
  dataset = [[1,1,'yes'],
            [1,1,'yes'],
            [1,0,'no'],
            [0,1,'no'],
            [0,1,'no']]
  labels = ['no surfacing', 'flippers']
  return dataset, labels

def splitDataset(dataset, axis, value):
  retDataset = []
  for featVec in dataset:
    if featVec[axis] == value:
      reducedFeatVec = featVec[:axis]
      reducedFeatVec.extend(featVec[axis+1:])
      retDataset.append(reducedFeatVec)
  return retDataset

def chooseBestFeatureToSplit(dataset):
  numFeatures = len(dataset[0]) - 1
  baseEntropy = calcShannonEnt(dataset)
  bestInfoGain = 0
  bestFeature = -1;
  for i in range(numFeatures):
    featList = [example[i] for example in dataset]
    uniqueVals = set(featList)
    newEntropy = 0.0
    for value in uniqueVals:
      subDataset = splitDataset(dataset, i, value)
      prob = len(subDataset) / float(len(dataset))
      newEntropy += prob * calcShannonEnt(subDataset)
    infoGain = baseEntropy - newEntropy
    if (infoGain > bestInfoGain):
      bestInfoGain = infoGain
      bestFeature = i
  return bestFeature

import operator

def majorityCnt(classList):
  classCount = {}
  for vote in classList:
    if vote not in classCount.keys(): 
      classCount[vote] = 0
    classCount[vote] += 1
  sortedClassCCount = sorted(classCount.iteritems(), 
                             key = operator.itemgetter(1),
                             reverse = True)
  return sortedClassCount[0][0]

def createTree(dataset, labels):
  classList = [example[-1] for example in dataset]
  if classList.count(classList[0]) == len(classList):
    return classList[0] #stop when all classes are equal
  if len(dataset[0]) == 1:
    return majorityCnt(classList) #stop when no more features
  bestFeat = chooseBestFeatureToSplit(dataset)
  bestFeatLabel = labels[bestFeat]
  myTree = {bestFeatLabel:{}}
  del(labels[bestFeat])
  featValues = [example[bestFeat] for example in dataset]
  uniqueVals = set(featValues)
  for value in uniqueVals:
    subLabels = labels[:]
    myTree[bestFeatLabel][value] = createTree(splitDataset(dataset, bestFeat, value), subLabels)
  return myTree