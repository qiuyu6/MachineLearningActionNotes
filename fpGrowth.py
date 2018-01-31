from numpy import *

def main():
	#rootNode = treeNode('pyramid', 9, None)
	#rootNode.children['eye'] = treeNode('eye', 13, None)
	#rootNode.children['pheonix'] = treeNode('pheonix', 3, None)
	#rootNode.disp()
	simpDat = loadSimpDat()
	initSet = createInitSet(simpDat)
	myFPtree, myHeaderTable = createTree(initSet, 3)
	myFPtree.disp()
	print findPrefixPath('r', myHeaderTable['r'][1])
	freqItems = []
	mineTree(myFPtree, myHeaderTable, 3, set([]), freqItems)


class treeNode:
	def __init__(self, nameValue, numOccur, parentNode):
		self.name = nameValue
		self.count = numOccur
		self.nodeLink = None 
		self.parent = parentNode
		self.children = {}

	def inc(self, numOccur):
		self.count += numOccur

	def disp(self, ind = 1):
		print '  '*ind, self.name, ' ', self.count
		for child in self.children.values():
			child.disp(ind + 1)

def createTree(dataset, minSup = 1):
	headerTable = {}
	for trans in dataset:
		for item in trans:
			headerTable[item] = headerTable.get(item, 0) + dataset[trans]
	for k in headerTable.keys():
		if headerTable[k] < minSup:
			del(headerTable[k])
	freqItemSet = set(headerTable.keys())
	if len(freqItemSet) == 0:
		return None, None
	for k in headerTable: #Expand the headtable
		headerTable[k] = [headerTable[k], None]
	retTree = treeNode('Null Set', 1, None)
	for tranSet, count in dataset.items():
		localD = {}
		for item in tranSet: #sort transactions by global frequency
			if item in freqItemSet:
				localD[item] = headerTable[item][0]
		if len(localD) > 0:
			orderedItems = [v[0] for v in sorted(localD.items(), key = lambda p:p[1], reverse = True)]
			updateTree(orderedItems, retTree, headerTable, count)
	return retTree, headerTable

def updateTree(items, inTree, headerTable, count):
	if items[0] in inTree.children:
		inTree.children[items[0]].inc(count)
	else:
		inTree.children[items[0]] = treeNode(items[0], count, inTree)
		if headerTable[items[0]][1] == None:
			headerTable[items[0]][1] = inTree.children[items[0]]
		else:
			updateHeader(headerTable[items[0]][1], inTree.children[items[0]])
	if len(items) > 1:
		#Recursively call updateTree on remaining items
		updateTree(items[1::], inTree.children[items[0]], headerTable, count)

def updateHeader(nodeToTest, targetNode):
	while (nodeToTest.nodeLink != None):
		nodeToTest = nodeToTest.nodeLink
	nodeToTest.nodeLink = targetNode

def loadSimpDat():
    simpDat = [['r', 'z', 'h', 'j', 'p'],
               ['z', 'y', 'x', 'w', 'v', 'u', 't', 's'],
               ['z'],
               ['r', 'x', 'n', 'o', 's'],
               ['y', 'r', 'x', 'z', 'q', 't', 'p'],
               ['y', 'z', 'x', 'e', 'q', 's', 't', 'm']]
    return simpDat

def createInitSet(dataset):
	retDict = {}
	for trans in dataset:
		retDict[frozenset(trans)] = 1
	return retDict

def ascendTree(leafNode, prefixPath):
	if leafNode.parent != None:
		prefixPath.append(leafNode.name)
		ascendTree(leafNode.parent, prefixPath)

def findPrefixPath(basePat, treeNode):
	condPats = {}
	while treeNode != None:
		prefixPath = []
		ascendTree(treeNode, prefixPath)
		if len(prefixPath) > 1:
			condPats[frozenset(prefixPath[1:])] = treeNode.count
		treeNode = treeNode.nodeLink
	return condPats

def mineTree(inTree, headertable, minSup, preFix, freqItemList):
	#start from bottom of header table
	bigL = [v[0] for v in sorted(headertable.items(), key = lambda p: p[1])]
	for basePat in bigL:
		newFreqSet = preFix.copy()
		newFreqSet.add(basePat)
		freqItemList.append(newFreqSet)
		condPattBases = findPrefixPath(basePat, headertable[basePat][1])
		#Construt conditional FP-tree from conditional pattern base
		myCondTree, myHead = createTree(condPattBases, minSup)
		if myHead != None:
			print 'conditional tree for: ', newFreqSet
			myCondTree.disp(1)
			#Mine conditional FP-tree
			mineTree(myCondTree,  myHead, minSup, newFreqSet, freqItemList)
















if __name__ == '__main__':
	main()