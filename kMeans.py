from numpy import *

def main():
	#dataMat = mat(loadDataset('testset2.txt'))
	#print randCent(dataMat, 2)
	#print distEclud(dataMat[0], dataMat[1])
	#centroids, clusterAssment = kMeans(dataMat,4)
	#print centroids
	#cenList, myNewAssments = biKmeans(dataMat, 3)
	#print cenList
	#geoResults = geoGrab('1 VA Center','Augusta, ME')
	#print geoResults
	#learnURL()
	clusterClubs(5)

import urllib2
def learnURL():
	response = urllib2.urlopen('http://local.yahooapis.com/MapsService/V1/geocode?appid=dj0yJmk9MmdjNGNlRE9mWHBCJmQ9WVdrOVozQlZURnBLTjJrbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD04Yg--&street=701+First+Ave&city=Sunnyvale&state=CA')
	html = response.read()
	print html


def loadDataset(filename):
	dataMat = []
	fr = open(filename)
	for line in fr.readlines():
		curLine = line.strip().split('\t')
		fltLine = map(float, curLine)
		dataMat.append(fltLine)
	return dataMat

def distEclud(vecA, vecB):
	return sqrt(sum(power(vecA - vecB, 2)))

def randCent(dataset, k):
	n = shape(dataset)[1]
	centroids = mat(zeros((k, n)))
	for j in range(n):
		minJ = min(dataset[:,j])
		rangeJ = float(max(dataset[:,j]) - minJ)
		centroids[:,j] = minJ + rangeJ * random.rand(k, 1)
	return centroids

def kMeans(dataset, k, distMeans = distEclud, createCent = randCent):
	m = shape(dataset)[0]
	clusterAssment = mat(zeros((m,2)))
	centroids = createCent(dataset,k)
	clusterChanged = True
	while clusterChanged:
		clusterChanged = False
		for i in range(m):
			minDist = inf 
			minIndex = -1
			for j in range(k):
				distJI = distMeans(dataset[i,:], centroids[j,:])
				if distJI < minDist:
					minDist = distJI
					minIndex = j
			if clusterAssment[i,0] != minIndex:
				clusterChanged = True
			clusterAssment[i,:] = minIndex,minDist**2
		print centroids
		#Update centroid location
		for cent in range(k):
			ptsInClust = dataset[nonzero(clusterAssment[:,0].A==cent)[0]]
			centroids[cent,:] = mean(ptsInClust, axis = 0)
	return centroids, clusterAssment

def biKmeans(dataset, k, distMeans = distEclud):
	m = shape(dataset)[0]
	clusterAssment = mat(zeros((m,2)))
	centroid0 = mean(dataset, axis = 0).tolist()[0]
	centList = [centroid0] #create a list with one centroid
	for j in range(m): #calc initial Error
		clusterAssment[j,1] = distMeans(mat(centroid0), dataset[j,:])**2
	while (len(centList) < k):
		lowestSSE = inf 
		for i in range(len(centList)):
			ptsInCurrCluster = dataset[nonzero(clusterAssment[:,0].A == i)[0],:] #get the data points currently in cluster i
			centroidMat, splitClustAss = kMeans(ptsInCurrCluster, 2, distMeans)
			sseSplit = sum(splitClustAss[:,1])
			sseNotSplit = sum(clusterAssment[nonzero(clusterAssment[:,0].A != i)[0],1])
			print "sseSplit, and notSplit: ", sseSplit, sseNotSplit
			if (sseSplit + sseNotSplit) < lowestSSE:
				bestCentToSplit = i 
				bestNewCents = centroidMat
				bestClustAss = splitClustAss.copy()
				lowestSSE = sseSplit + sseNotSplit
		# When you applied kMeans() with two clusters, you had two clusters returned labeled 0 and 1. 
		# change these cluster numbers to the cluster number you're splitting 
		bestClustAss[nonzero(bestClustAss[:,0].A == 0)[0],0] = bestCentToSplit
		# and the next cluster to be added.		
		bestClustAss[nonzero(bestClustAss[:,0].A == 1)[0],0] = len(centList)
		print 'the bestCentToSplit is: ', bestCentToSplit
		print 'the len of bestClustAss is: ', len(bestClustAss)
		#replace a centroid with two best centroids 
		centList[bestCentToSplit] = bestNewCents[0,:].tolist()[0] 
		centList.append(bestNewCents[1,:].tolist()[0])
		# update the clusterAssment with two new clusters and SSE
		clusterAssment[nonzero(clusterAssment[:,0].A == bestCentToSplit)[0],:] = bestClustAss
	return mat(centList), clusterAssment

import urllib
import urllib2
import json

def geoGrab(stAddress, city):
	apiStem = 'http://where.yahooapis.com/geocode?'  #create a dict and constants for the goecoder
	params = {}
	params['flags'] = 'J' #JSON return type
	params['appid'] = 'dj0yJmk9MmdjNGNlRE9mWHBCJmQ9WVdrOVozQlZURnBLTjJrbWNHbzlNQS0tJnM9Y29uc3VtZXJzZWNyZXQmeD04Yg--'
	params['location'] = '%s %s' % (stAddress, city)
	url_params = urllib.urlencode(params)
	yahooApi = apiStem + url_params      #print url_params
	print yahooApi
	c=urllib.urlopen(yahooApi)
	return json.loads(c.read())


from time import sleep

def massPlaceFind(filename):
	fw = open('places.txt','w')
	for line in open(filename).readlines():
		line = line.strip()
		lineArr = line.split('\t')
		retDict = geoGrab(lineArr[1], lineArr[2])
		if retDict['ResultSet']['Error'] == 0:
			lat = float(retDict['ResultSet']['Results'][0]['latitude'])
			lng = float(retDict['ResultSet']['Results'][0]['longtitude'])
			print "%s\t%f\t%f\n" % (line, lat, lng)
		else:
			print "error fetching"
		sleep(1)
	fw.close()

def distSLC(vecA, vecB):
	a = sin(vecA[0,1] * pi / 180) * sin(vecB[0,1] * pi / 180)
	b = cos(vecA[0,1] * pi / 180) * cos(vecB[0,1] * pi / 180) * cos(pi * (vecB[0,0] - vecA[0,0]) / 180)
	return arccos(a + b) * 6371.0

import matplotlib
import matplotlib.pyplot as plt 

def clusterClubs(numClust = 5):
	dataList = []
	for line in open('places.txt').readlines():
		lineArr = line.split('\t')
		dataList.append([float(lineArr[4]), float(lineArr[3])])
	dataMat = mat(dataList)
	myCentroids, clustAsing = biKmeans(dataMat, numClust, distMeans = distSLC)
	fig = plt.figure()
	rect = [0.1, 0.1, 0.8, 0.8]
	scatterMarkers = ['s', 'o', '^', '8', 'p', 'd', 'v', 'h', '>', '<']
	axprops = dict(xticks = [], yticks = [])
	ax0 = fig.add_axes(rect, label = 'ax0', **axprops)
	imgP = plt.imread('Portland.png')
	ax0.imshow(imgP)
	ax1 = fig.add_axes(rect, label = 'ax1', frameon = False)
	for i in range(numClust):
		ptsInCurrCluster = dataMat[nonzero(clustAsing[:,0].A == i)[0],:]
		markerStyle = scatterMarkers[i % len(scatterMarkers)]
		ax1.scatter(ptsInCurrCluster[:,0].flatten().A[0], ptsInCurrCluster[:,1].flatten().A[0], marker = markerStyle, s = 90)
	ax1.scatter(myCentroids[:,0].flatten().A[0], myCentroids[:,1].flatten().A[0], marker = '+', s = 300)
	plt.show()













































if __name__ == '__main__':
	main()