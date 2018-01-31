
from numpy import *
from os import listdir
import operator

def main():
	handwritingClassTest()


def img2Vector(filename):
	returnVect = zeros((1,1024))
	fr = open(filename)
	for i in range(32):
		lineStr = fr.readline()
		for j in range(32):
			returnVect[0,32 * i + j] = int(lineStr[j]) 
	return returnVect

def classify0(inX, dataset, labels, k):
	datasetSize = dataset.shape[0]
	diffMat = tile(inX, (datasetSize, 1)) - dataset
	sqDiffMat = diffMat**2
	sqDistance = sqDiffMat.sum(axis=1)
	distances = sqDistance**0.5
	sortedDistIndicies = distances.argsort()
	classCount={}
	for i in range(k):
		voteLabel = labels[sortedDistIndicies[i]]
		classCount[voteLabel] = classCount.get(voteLabel,0) + 1
	sortedClassCount = sorted(classCount.iteritems(), key=operator.itemgetter(1), reverse=True)
	return sortedClassCount[0][0]

def handwritingClassTest():
	hwLabels = []
	trainingFileList = listdir('digits/trainingDigits')
	m = len(trainingFileList)
	trainingMat = zeros((m, 1024))
	for i in range(m):
		filenameStr = trainingFileList[i]
		fileStr = filenameStr.split('.')[0]
		classNumStr = int(fileStr.split('_')[0])
		hwLabels.append(classNumStr)
		trainingMat[i,:] = img2Vector('digits/trainingDigits/%s' % filenameStr)
	testFileList = listdir('digits/testDigits')
	erorrCount = 0.0
	mTest = len(testFileList)
	for i in range(mTest):
		filenameStr = testFileList[i]
		fileStr = filenameStr.split('.')[0]
		classNumStr = int(fileStr.split('_')[0])
		vectorUnderTest = img2Vector('digits/testDigits/%s' % filenameStr)
		classifierResult = classify0(vectorUnderTest, trainingMat, hwLabels, 3)
		print "the classifier came back with: %d, the real answer is: %d" % (classifierResult, classNumStr)
		if (classifierResult != classNumStr):
			erorrCount += 1.0
	print "\nthe total number of errors is: %d" % erorrCount
	print "\nthe total error rate is: %f" % (erorrCount/float(mTest))






if __name__ == '__main__':
	main()
