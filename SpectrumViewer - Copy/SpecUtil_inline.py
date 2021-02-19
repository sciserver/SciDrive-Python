# this file hold utility functions that generate the plot and actual data
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from astropy.io import fits
class SpecUtil(object):
    def __init__(self,filename,coaddObj,zObj):
        self.coaddObj = coaddObj
        self.zObj=zObj
        self.plotDict = {0: True,
                         1: True,
                         2: True,
                         3: True,
                         4: True}
        #0 flux 1 skyline 2 emission 3 absorb 4 model
        #self.updateFig()
        self.figure = plt.figure(filename,figsize=(10, 8), dpi=100)
        self.shownAx = self.figure.add_subplot(111)
        plt.subplots_adjust(bottom=0.2)

        self.axfluxbutton = plt.axes([0.1, 0.05, 0.1, 0.075])
        self.fluxbutton = Button(self.axfluxbutton, 'flux')
        self.fluxbutton.on_clicked(self.fluxClicked)

        self.axskylinebutton = plt.axes([0.2, 0.05, 0.1, 0.075])
        self.skylinebutton = Button(self.axskylinebutton, 'skyline')
        self.skylinebutton.on_clicked(self.skylineClicked)

        self.axabsorbbutton = plt.axes([0.3, 0.05, 0.1, 0.075])
        self.absorbbutton = Button(self.axabsorbbutton, 'absorption')
        self.absorbbutton.on_clicked(self.absorbClicked)

        self.axemission = plt.axes([0.4, 0.05, 0.1, 0.075])
        self.emissionbutton = Button(self.axemission, 'emission')
        self.emissionbutton.on_clicked(self.emissionClicked)

        self.axmodelbutton = plt.axes([0.5, 0.05, 0.1, 0.075])
        self.modelbutton = Button(self.axmodelbutton, 'model')
        self.modelbutton.on_clicked(self.modelClicked)

    def showfig(self):
        self.updateFig()
    def updateFig(self):

        # figure = plt.figure(figsize=(8, 4), dpi=100)
        # shownAx=figure.add_subplot(111)
        # plt.subplots_adjust(bottom=0.2)

        self.shownAx.clear()
        self.shownAx.set_xlabel('lambda/Å')
        self.shownAx.set_ylabel('10-17 ergs/s/cm2/Å')
        for key in self.plotDict.keys():
            if self.plotDict[key]:
                try:
                    self.plotLines(self.shownAx,key)
                except IndexError:
                    pass

        self.shownAx.legend()
        plt.show()
    def fluxClicked(self,event):
        if self.plotDict[0]:
            self.plotDict[0]=False
        else:
            self.plotDict[0] = True

        self.updateFig()
    def skylineClicked(self,event):
        if self.plotDict[1]:
            self.plotDict[1]=False
        else:
            self.plotDict[1] = True
        self.updateFig()
    def emissionClicked(self, event):
        if self.plotDict[2]:
            self.plotDict[2] = False
        else:
            self.plotDict[2] = True
        self.updateFig()
    def absorbClicked(self, event):
        if self.plotDict[3]:
            self.plotDict[3] = False
        else:
            self.plotDict[3] = True
        self.updateFig()
    def modelClicked(self, event):
        if self.plotDict[4]:
            self.plotDict[4] = False
        else:
            self.plotDict[4] = True
        self.updateFig()
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
