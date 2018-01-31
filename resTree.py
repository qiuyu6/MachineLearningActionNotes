from numpy import *

def main():
	#myData = loadDataset('ex2.txt')
	#myMat = mat(myData)
	#myTree = createTree(myMat, ops = (0,1))
	#myDataTest = loadDataset('ex2test.txt')
	#myMatTest = mat(myDataTest)
	#print(myTree)
	#prune(myTree, myMatTest)
	#print(myTree)
	#myData = loadDataset('exp2.txt')
	#myMat = mat(myData)
	#print createTree(myMat, modelLeaf, modelErr, (1,300))
	trainMat = mat(loadDataset('bikeSpeedVsIq_train.txt'))
	testMat = mat(loadDataset('bikeSpeedVsIq_test.txt'))
	myTree = createTree(trainMat, ops = (1,20))
	yHat = createForeCast(myTree, testMat[:,0])
	print corrcoef(yHat, testMat[:,1], rowvar = 0)[0,1]
	myTree2 = createTree(trainMat, modelLeaf, modelErr, (1,20))
	yHat2 = createForeCast(myTree2, testMat[:,0],modelTreeEval)
	print corrcoef(yHat2, testMat[:,1], rowvar = 0)[0,1]
	ws, X, Y = linearSolve(trainMat)
	print ws

def regTreeEval(model, inDat):
	return float(model)

def modelTreeEval(model, inDat):
	n = shape(inDat)[1]
	X = mat(ones((1, n + 1)))
	X[:,1:n+1] = inDat
	return float(X*model)

def treeForeCast(tree, inDat, modelEval = regTreeEval):
	if not isTree(tree):
		return modelEval(tree, inDat)
	if inDat[tree['spInd']] > tree['spVal']:
		if isTree(tree['left']):
			return treeForeCast(tree['left'], inDat, modelEval)
		else:
			return modelEval(tree['left'], inDat)
	else:
		if isTree(tree['right']):
			return treeForeCast(tree['right'], inDat, modelEval)
		else:
			return modelEval(tree['right'], inDat)

def createForeCast(tree, testData, modelEval = regTreeEval):
	m = len(testData)
	yHat = mat(zeros((m,1)))
	for i in range(m):
		yHat[i,0] = treeForeCast(tree, mat(testData[i]), modelEval)
	return yHat

def linearSolve(dataset):
	m,n = shape(dataset)
	X = mat(ones((m, n)))
	Y = mat(ones((m, 1)))
	X[:,1:n] = dataset[:,0:n-1]
	Y = dataset[:,-1]
	xTx = X.T * X
	if linalg.det(xTx) == 0.0:
		raise NameError('This matrix is singular, cannot do inverse, try increasing the second value of ops')
	ws = xTx.I * (X.T * Y)
	return ws, X, Y

def modelLeaf(dataset):
	ws,X,Y = linearSolve(dataset)
	return ws

def modelErr(dataset):
	ws,X,Y = linearSolve(dataset)
	yHat = X * ws
	return sum(power(Y - yHat, 2))

def isTree(obj):
	return (type(obj).__name__=='dict')

def getMean(tree):
	if isTree(tree['right']):
		tree['right'] = getMean(tree['right'])
	if isTree(tree['left']):
		tree['left'] = getMean(tree['left'])
	return (tree['left'] + tree['right']) / 2.0

def prune(tree, testData):
	if shape(testData)[0] == 0:
		return getMean(tree)
	if isTree(tree['right']) or isTree(tree['left']):
		lSet, rSet = binSplitDataset(testData, tree['spInd'], tree['spVal'])
	if isTree(tree['left']):
		tree['left'] = prune(tree['left'], lSet)
	if isTree(tree['right']):
		tree['right'] = prune(tree['right'], rSet)
	if not isTree(tree['left']) and not isTree(tree['right']):
		lSet, rSet = binSplitDataset(testData, tree['spInd'], tree['spVal'])
		errorNoMerge = sum(power(lSet[:,-1] - tree['left'], 2)) + sum(power(rSet[:,-1] - tree['right'],2))
		treeMean = (tree['left'] + tree['right']) / 2.0
		errorMerge = sum(power(testData[:,-1] - treeMean, 2))
		if errorMerge < errorNoMerge:
			print "merging"
			return treeMean
		else:
			return tree
	else:
		return tree

def regLeaf(dataset):
	return mean(dataset[:,-1])

def regErr(dataset):
	return var(dataset[:,-1]) * shape(dataset)[0]

def chooseBestSplit(dataset, leafType = regLeaf, errType = regErr, ops = (1,4)):
	tolS = ops[0]
	tolN = ops[1]
	if len(set(dataset[:,-1].T.tolist()[0])) == 1:
		#Exit if all values are equal
		return None, leafType(dataset)
	m,n = shape(dataset)
	S = errType(dataset)
	bestS = inf 
	bestIndex = 0
	bestValue = 0
	for featIndex in range(n - 1):
		for splitVal in set(dataset[:, featIndex]):
			mat0, mat1 = binSplitDataset(dataset, featIndex, splitVal)
			if (shape(mat0)[0] < tolN) or (shape(mat1)[0] < tolN): continue
			newS = errType(mat0) + errType(mat1)
			if newS < bestS:
				bestIndex = featIndex
				bestS = newS
				bestValue = splitVal
	if (S - bestS) < tolS:
		#Exit if low error reduction
		return None, leafType(dataset)
	mat0, mat1 = binSplitDataset(dataset, bestIndex, bestValue)
	if (shape(mat0)[0] < tolN) or (shape(mat1)[0] < tolN):
		#Exit if split creates small dataset
		return None, leafType(dataset)
	return bestIndex, bestValue

def loadDataset(filename):
	dataMat = []
	fr = open(filename)
	for line in fr.readlines():
		curLine = line.strip().split('\t')
		fltLine = map(float, curLine) #map everything to float
		dataMat.append(fltLine)
	return dataMat

def binSplitDataset(dataset, feature, value):
	mat0 = dataset[nonzero(dataset[:,feature] > value)[0],:][0]
	mat1 = dataset[nonzero(dataset[:,feature] <= value)[0],:][0]
	return mat0, mat1

def createTree(dataset, leafType = regLeaf, errType = regErr, ops = (1,4)):
	feat, val = chooseBestSplit(dataset, leafType, errType, ops)
	if feat == None:
		#Return leaf value if stopping condition met
		return val
	retTree = {}
	retTree['spInd'] = feat
	retTree['spVal'] = val
	lSet, rSet = binSplitDataset(dataset, feat, val)
	retTree['left'] = createTree(lSet, leafType, errType, ops)
	retTree['right'] = createTree(rSet, leafType, errType, ops)
	return retTree


















class treeNoe():
	def _init_(self, feat, val, right, left):
		featureToSplitOn = feat
		valueOfSplit = val
		rightBranch = right
		leftBranch = left

if __name__ == '__main__':
	main()