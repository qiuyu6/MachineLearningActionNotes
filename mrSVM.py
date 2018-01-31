from mrjob.job import MRJob

import pickle
from numpy import *

class  MRsvm(MRJob):
	DEFAULT_INPUT_PROTOCOL = 'json_value'

	def __init__(self, *args, **kwargs):
		super(MRsvm, self).__init__(args, **kwargs)
		self.data = pickle.load(open('/Users/yuq/Dropbox/MachineLearningAction/svmDat27'))
		self.w = 0
		self.eta = 0.69
		self.dataList = []
		self.k = self.options.batchsize
		self.numMappers = 1
		self.t = 1
