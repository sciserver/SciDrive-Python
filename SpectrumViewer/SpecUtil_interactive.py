# this file hold utility functions that generate the plot and actual data
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
import numpy as np
from ipywidgets import interactive
class SpecUtil:
    def __init__(self,coaddObj,zObj):
        self.coaddObj = coaddObj
        self.zObj=zObj
        # self.totalFig = plt.figure()
        # self.shownFig = plt.figure()
        #self.totalFig = Figure(figsize=(5, 4), dpi=100)
        #self.shownFig = Figure(figsize=(5, 4), dpi=100)
        #self.shownFig = plt.figure()
        self.plotDict = {0: True,
                         1: True,
                         2: True,
                         3: True,
                         4: True}
        #0 flux 1 skyline 2 emission 3 absorb 4 model
        #self.totalAx = self.totalFig.add_subplot(111)
        #fluxLine,=self.totalAx.plot(self.coaddObj.lam,self.coaddObj.flux)
        #skyLine, = self.totalAx.plot(self.coaddObj.lam,self.coaddObj.sky)

        #self.shownAx = self.shownFig.add_subplot(111)
        #self.updateFig()
        #self.shownAx = self.totalAx
        self.interactive_plot = interactive(self.showfig, flux=True,skyline=True,emission=True,absorb=True,model=True)
        self.interactive_plot.children[0].layout.display = 'flex'
        output = self.interactive_plot.children[-1]
        output.layout.height = '550px'

    def showfig(self,flux,skyline,emission,absorb,model):
        self.plotDict[0] = flux
        self.plotDict[1] =skyline
        self.plotDict[2] =emission
        self.plotDict[3] =absorb
        self.plotDict[4] =model
        self.updateFig()
    def updateFig(self):
        #self.shownAx.lines=[]
        figure = plt.figure(figsize=(8, 4), dpi=100)
        shownAx=figure.add_subplot(111)

        #self.shownAx.clear()
        shownAx.set_xlabel('lambda/Å')
        shownAx.set_ylabel('10-17 ergs/s/cm2/Å')
        for key in self.plotDict.keys():
            if self.plotDict[key]:
                try:
                    self.plotLines(shownAx,key)
                except IndexError:
                    pass
        #line1, = ax.plot(x, y, 'b-')
        shownAx.legend()
        #for phase in np.linspace(0, 10 * np.pi, 100):
         #   line1.set_ydata(np.sin(0.5 * x + phase))
          #  fig.canvas.draw()

        plt.show()
    def format_coord(self,x,y):
        return 'x=%1.4f, y=%1.4f'%(x, y)
    def addFlux(self):
        self.plotDict[0]=True
        self.updateFig()
    def removeFlux(self):
        self.plotDict[0] = False
        self.updateFig()

    def addSkyline(self):
        self.plotDict[1] = True
        self.updateFig()
    def removeSkyline(self):
        self.plotDict[1] = False
        self.updateFig()
    def addEmissionLine(self):
        self.plotDict[2] = True
        self.updateFig()
    def removeEmissionLine(self):
        self.plotDict[2] = False
        self.updateFig()
    def addAbsorbLine(self):
        self.plotDict[3] = True
        self.updateFig()
    def removeAbsorbLine(self):
        self.plotDict[3] = False
        self.updateFig()
    def addModel(self):
        self.plotDict[4] = True
        self.updateFig()
    def removeModel(self):
        self.plotDict[4] = False
        self.updateFig()
    def plotLines(self,axes,actionIndex):
        if actionIndex==0:
            axes.plot(self.coaddObj.lam, self.coaddObj.flux,'C0',label='flux')
        elif actionIndex==1:
            axes.plot(self.coaddObj.lam, self.coaddObj.sky,'C1',label='skyline')
        elif actionIndex==2:
            #plot emission line
            self.plotSegment(axes,actionIndex)

        elif actionIndex ==3:
            #plot absorption line
            self.plotSegment(axes,actionIndex)


        elif actionIndex ==4:

            #plot best fit model
            axes.plot(self.coaddObj.lam, self.coaddObj.model, 'C3', label='best fit model')
        else:

            pass
    def plotSegment(self,axes,actionIndex):

        # read e/a line from zobj and plot it on axes with function from axhspan
        if actionIndex==2:#emissiaon line
            for lineIndex in range(0,len(self.zObj.LINENAME)):

                width = self.zObj.LINEEW[lineIndex]
                if width >0:
                    #print(width)
                    position = self.zObj.LINEWAVE[lineIndex]
                    startPostition = position-width/2
                    endPostition = position + width / 2
                    name= self.zObj.LINENAME[lineIndex]
                    #print(name)
                    axes.axvspan(xmin=startPostition,xmax=endPostition, facecolor='C4')
                    axes.text(position,0,name , rotation=90)
        elif actionIndex==3:#absorption line
            for lineIndex in range(0,len(self.zObj.LINENAME)):
                width = self.zObj.LINEEW[lineIndex]
                if width >0:
                    #print(width)
                    position = self.zObj.LINEWAVE[lineIndex]
                    startPostition = position-width/2
                    endPostition = position + width / 2
                    name= self.zObj.LINENAME[lineIndex]
                    #print(name)
                    axes.axvspan(xmin=startPostition,xmax=endPostition, facecolor='C4')
                    axes.text(position,0,name , rotation=90)
