from numpy import *
from numpy import linalg as la

def main():
	#myMat = mat(loadExData())
	#print ecludSim(myMat[:,0], myMat[:,4])
	#print cosSim(myMat[:,0], myMat[:,4])
	#print pearsSim(myMat[:,0], myMat[:,4])
	#print myMat
	#print recommend(myMat, 2, 3, cosSim, standEst)
	#myMat = mat(loadExData2())
	#U, Sigma, VT = la.svd(myMat)
	#print Sigma
	#See the total energy
	#Sig2 = Sigma ** 2
	#print sum(Sig2)
	#See 90% of the total energy
	#print sum(Sig2) * 0.9
	#See how many elements can achieve 90% energy
	#print sum(Sig2[:2]) # first two elements
	#print sum(Sig2[:3]) # first three elements
	#print recommend(myMat, 1, 3, estMethod = svdEst)
	imgCompress(2)

def standEst(dataMat, user, simMeans, item):
	n = shape(dataMat)[1]
	simTotal = 0.0
	ratSimTotal = 0.0
	for j in range(n):
		userRating = dataMat[user, j] #How much given user rated this j item
		if userRating == 0:
			continue;
		#Find items rated by both users
		overLap = nonzero(logical_and(dataMat[:,item].A > 0, dataMat[:,j].A > 0))[0]
		if len(overLap) == 0:
			similarity = 0
		else:
			#Item-based similarity, this item is rated by some users, and j item is also rated by the same group by users
			#we would like to know how similar current item and j item, and use how much user rated j to approach how much user will rate this item
			similarity = simMeans(dataMat[overLap, item], dataMat[overLap, j])
		simTotal += similarity 
		ratSimTotal += similarity * userRating
	if simTotal == 0:
		return 0
	else:
		return ratSimTotal / simTotal

def ecludSim(inA, inB):
	return 1.0 / (1.0 + la.norm(inA - inB))

def pearsSim(inA, inB):
	if len(inA) < 3:
		return 1.0
	return 0.5 + 0.5 * corrcoef(inA, inB, rowvar = 0)[0][1]

def cosSim(inA, inB):
	num = float(inA.T * inB)
	denom = la.norm(inA) * la.norm(inB)
	return 0.5 + 0.5 * num / denom

def svdEst(dataMat, user, simMeans, item):
	n = shape(dataMat)[1]
	simTotal = 0.0
	ratSimTotal = 0.0
	U, Sigma, VT = la.svd(dataMat)
	Sig4 = mat(eye(4) * Sigma[:4])
	xformedItems = dataMat.T * U[:,:4] * Sig4.I
	for j in range(n):
		userRating = dataMat[user, j]
		if userRating == 0 or j == item:
			continue
		similarity = simMeans(xformedItems[item,:].T, xformedItems[j,:].T)
		simTotal += similarity
		ratSimTotal += similarity * userRating
	if simTotal == 0: 
		return 0
	else:
		return ratSimTotal / simTotal

def recommend(dataMat, user, N = 3, simMeans = cosSim, estMethod = standEst):
	#Find unrated item
	unratedItems = nonzero(dataMat[user,:].A == 0)[1]
	if len(unratedItems) == 0:
		return 'you rated everything'
	itemScores = []
	for item in unratedItems:
		estimatedScore = estMethod(dataMat, user, simMeans, item)
		itemScores.append((item, estimatedScore))
	#return top n unrated items
	return sorted(itemScores, key = lambda jj:jj[1], reverse = True)[:N]

def printMat(inMat, thresh = 0.8):
	for i in range(32):
		for k in range(32):
			if float(inMat[i,k]) > thresh:
				print 1,
			else:
				print 0,
		print ' '

def imgCompress(numSv = 3, thresh = 0.8):
	myl = []
	for line in open('0_5.txt').readlines():
		newRow = []
		for i in range(32):
			newRow.append(int(line[i]))
		myl.append(newRow)
	myMat = mat(myl)
	print "****original matrix****"
	printMat(myMat, thresh)
	U, Sigma, VT = la.svd(myMat)
	SigRecon = mat(zeros((numSv, numSv)))
	for k in range(numSv):
		SigRecon[k,k] = Sigma[k]
	reconMat = U[:,:numSv] * SigRecon * VT[:numSv,:]
	print "****reconstructed matrix using %d singular value****" % numSv
	printMat(reconMat, thresh)

def loadExData():
	return [[4,4,0,2,2],[4,0,0,3,3],[4,0,0,1,1],[1,1,1,2,0],[2,2,2,0,0],[1,1,1,0,0],[5,5,5,0,0]]

def loadExData2():
    return[[0, 0, 0, 0, 0, 4, 0, 0, 0, 0, 5],[0, 0, 0, 3, 0, 4, 0, 0, 0, 0, 3],[0, 0, 0, 0, 4, 0, 0, 1, 0, 4, 0],[3, 3, 4, 0, 0, 0, 0, 2, 2, 0, 0],[5, 4, 5, 0, 0, 0, 0, 5, 5, 0, 0],[0, 0, 0, 0, 5, 0, 1, 0, 0, 5, 0],[4, 3, 4, 0, 0, 0, 0, 5, 5, 0, 1],[0, 0, 0, 4, 0, 4, 0, 0, 0, 0, 4],[0, 0, 0, 2, 0, 2, 5, 0, 0, 1, 2],[0, 0, 0, 0, 5, 0, 0, 0, 0, 4, 0],[1, 0, 0, 0, 0, 0, 0, 1, 2, 0, 0]]


if __name__ == '__main__':
	main()
