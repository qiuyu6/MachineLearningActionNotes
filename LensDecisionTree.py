
import trees
import treePlotter

def main():
	fr = open('lenses.txt')
	lenses = []
	for inst in fr.readlines():
		lenses.append(inst.strip().split('\t'))
	lensesLabels = ['age', 'prescript', 'astigmatic', 'tearRate']
	lensesTree = trees.createTree(lenses, lensesLabels)
	lensesTree
	treePlotter.createPlot(lensesTree)

if __name__ == '__main__':
	main()