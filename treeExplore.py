from numpy import *

from Tkinter import *

import resTree

import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

def reDraw(tolS, tolN):
	reDraw.f.clf() #clear the figure
	reDraw.a = reDraw.f.add_subplot(111)
	if chkBtnVar.get(): 
		#see if check box has been seleted
		if tolN < 2:
			tolN = 2
		myTree = resTree.createTree(reDraw.rawData, resTree.modelLeaf, resTree.modelErr, (tolS, tolN))
		yHat = resTree.createForeCast(myTree, reDraw.testData, resTree.modelTreeEval)
	else:
		myTree = resTree.createTree(reDraw.rawData, ops = (tolS, tolN))
		yHat = resTree.createForeCast(myTree, reDraw.testData)
	reDraw.a.scatter(reDraw.rawData[:,0], reDraw.rawData[:,1], s = 5)
	reDraw.a.plot(reDraw.testData, yHat, linewidth = 2.0)
	reDraw.canvas.show()

def getInputs():
	try:
		tolN = int(tolNentry.get())
	except:
		tolN = 10
		print "enter Integer for tolN"
		tolNentry.delete(0, END)
		tolNentry.insert(0, '10')
	try:
		tolS = float(tolSentry.get())
	except:
		tolS = 1.0
		print "enter Integer for tolS"
		tolSentry.delete(0, END)
		tolSentry.insert(0,'10')
	return tolN, tolS

def drawNewTree():
	tolN, tolS = getInputs()
	reDraw(tolS, tolN)

root = Tk() #A small window will appear

#To fill out the window with text

#Label(root, text = "Plot Place Holder").grid(row = 0, columnspan = 3)

#This code creates a Matplotlib figure and assigns it to the global variable reDraw.f.
reDraw.f = Figure(figsize = (5,4), dpi = 100)
reDraw.canvas = FigureCanvasTkAgg(reDraw.f, master = root)
reDraw.canvas.show()
reDraw.canvas.get_tk_widget().grid(row = 0, columnspan = 3)

Label(root, text = "tolN").grid(row = 1, column = 0)
tolNentry = Entry(root)
tolNentry.grid(row = 1, column = 1)
tolNentry.insert(0,'10')

Label(root, text = "tolS").grid(row = 2, column = 0)
tolSentry = Entry(root)
tolSentry.grid(row = 2, column = 1)
tolSentry.insert(0,'10')

Button(root, text = "reDraw", command = drawNewTree).grid(row = 1, column = 2, rowspan = 3)

Button(root, text = "Quit", fg = "black", command = root.quit).grid(row = 1, column = 2)

chkBtnVar = IntVar()
chkBtn = Checkbutton(root, text = "Model Tree", variable = chkBtnVar)
chkBtn.grid(row = 3, column = 0, columnspan = 2)

reDraw.rawData = mat(resTree.loadDataset('sine.txt'))
reDraw.testData = arange(min(reDraw.rawData[:,0]), max(reDraw.rawData[:,0]), 0.01)
reDraw(1.0, 1.0)


root.mainloop() #Kicks off the event loop









if __name__ == '__main__':
	main()