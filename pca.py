from numpy import *

def main():
	#dataMat = loadDataset('testset.txt')
	#lowDDataMat, reconMat = pca(dataMat, 1)
	#plotPCA(dataMat, reconMat)
	dataMat = replaceNanWithMean()
	meanVals = mean(dataMat, axis = 0)
	meanRemoved = dataMat - meanVals
	covMat = cov(meanRemoved, rowvar = 0)
	eigVals, eigVects = linalg.eig(mat(covMat))
	print eigVals


def replaceNanWithMean():
	dataMat = loadDataset('secom.data',' ')
	numFeat = shape(dataMat)[1]
	for i in range(numFeat):
		meanVal = mean(dataMat[nonzero(~isnan(dataMat[:,i].A))[0],i])
		dataMat[nonzero(isnan(dataMat[:,i].A))[0],i] = meanVal
	return dataMat


import matplotlib
import matplotlib.pyplot as plt 

def plotPCA(dataMat, reconMat):
	fig = plt.figure()
	ax = fig.add_subplot(111)
	ax.scatter(dataMat[:,0].flatten().A[0], dataMat[:,1].flatten().A[0], marker = '^', s = 90)
	ax.scatter(reconMat[:,0].flatten().A[0], reconMat[:,1].flatten().A[0], marker = 'o', s = 50, c = 'red')
	plt.show()

def loadDataset(filename, delim = '\t'):
	fr = open(filename)
	stringArr = [line.strip().split(delim) for line in fr.readlines()]
	dataArr = [map(float, line) for line in stringArr]
	return mat(dataArr)

def pca(dataMat, topNfeat = 9999999):
	meanVals = mean(dataMat, axis = 0)
	meanRemoved = dataMat - meanVals
	covMat = cov(meanRemoved, rowvar = 0)
	eigVals, eigVects = linalg.eig(mat(covMat))
	eigValInd = argsort(eigVals) #sort, goes from smallest to largest
	#sort top N smallest to largest
	eigValInd = eigValInd[:-(topNfeat + 1):-1] #cut off unwanted dimensions
	redEigVects = eigVects[:,eigValInd] #reorganize eig vects largest to smallest
	#transform data into new dimensions
	lowDDataMat = meanRemoved * redEigVects
	reconMat = (lowDDataMat * redEigVects.T) + meanVals
	return lowDDataMat, reconMat







if __name__ == '__main__':
	main()