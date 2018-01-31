def predict(w, x):
	return w*x.T

def batchPegasos(dataset, labels, lam, T, k):
	m,n = shape(dataset)
	w = zeros(n);
	dataIndex = range(m)
	for t in range(1, T+1):
		wDelta = mat(zeros(n))
		eta = 1.0/(lam*t)
		random.shuffle(dataIndex)
		for j in range(k):
			i = dataIndex[j]
			p = predict(w, dataIndex[i,:])
			if labels[i]*p < 1:
				wDelta += labels[i]*dataset[i,:].A
		w = (1.0 - 1/t)*w + (eta/k)*wDelta
	return w
	