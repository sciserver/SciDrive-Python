# show plotting result in a new window interactively
# this is actual user interface all the object are hide away from user
import matplotlib
matplotlib.use("TkAgg")
from SpectrumViewer import SDSSDriver as driver
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2TkAgg
# implement the default mpl key bindings
from matplotlib.backend_bases import key_press_handler
import tkinter as Tk

from SpectrumViewer import SpecUtil as SpecUtil
def view(fileName,fileSource):
    coaddObj, zObj = driver.loadFITS(fileName, fileSource)
    #construn tk window and all components


    root = Tk.Tk()
    root.wm_title("Embedding in TK")
    app = SpecController(root,coaddObj,zObj)
    root.mainloop()

class SpecController:
    #take objs to construct specmodel and specview
    def __init__(self,root,coaddObj,zObj):
        self.model = SpecModel(coaddObj,zObj)
        self.view = SpecView(root,self.model.specUtilObj.shownFig)
        self.view.sidepanel.fluxTogg.bind("<Button>",self.fluxTogg)
        self.view.sidepanel.skylineTogg.bind("<Button>", self.skylineTogg)
        self.view.sidepanel.emissionTogg.bind("<Button>", self.emissionTogg)
        self.view.sidepanel.absorbTogg.bind("<Button>", self.absorbTogg)
        self.view.sidepanel.modelTogg.bind("<Button>", self.modelTogg)

        #self.view.updateFigure(self.model.f)
        # add buttons manage lau out
    # def function change model and tell view.updatefigure(model.figure)
    def fluxTogg(self,event):
        if self.view.sidepanel.fluxTogg.config('text')[-1].endswith('ON'):
            #update the model
            self.model.specUtilObj.removeFlux()
            self.view.updateFigure(self.model.specUtilObj.shownFig)
            self.view.sidepanel.fluxTogg.config(text='FLUX:OFF')
        else:
            self.model.specUtilObj.addFlux()
            self.view.updateFigure(self.model.specUtilObj.shownFig)
            self.view.sidepanel.fluxTogg.config(text='FLUX:ON')
    def skylineTogg(self,event):
        if self.view.sidepanel.skylineTogg.config('text')[-1].endswith('ON'):
            #update the model
            self.model.specUtilObj.removeSkyline()
            self.view.updateFigure(self.model.specUtilObj.shownFig)
            self.view.sidepanel.skylineTogg.config(text='SKYLINE:OFF')
        else:
            self.model.specUtilObj.addSkyline()
            self.view.updateFigure(self.model.specUtilObj.shownFig)
            self.view.sidepanel.skylineTogg.config(text='SKYLINE:ON')
    def emissionTogg(self,event):
        if self.view.sidepanel.emissionTogg.config('text')[-1].endswith('ON'):
            #update the model
            self.model.specUtilObj.removeEmissionLine()
            self.view.updateFigure(self.model.specUtilObj.shownFig)
            self.view.sidepanel.emissionTogg.config(text='EMISSION LINE:OFF')
        else:
            self.model.specUtilObj.addEmissionLine()
            self.view.updateFigure(self.model.specUtilObj.shownFig)
            self.view.sidepanel.emissionTogg.config(text='EMISSION LINE:ON')
    def absorbTogg(self,event):
        if self.view.sidepanel.absorbTogg.config('text')[-1].endswith('ON'):
            #update the model
            self.model.specUtilObj.removeAbsorbLine()
            self.view.updateFigure(self.model.specUtilObj.shownFig)
            self.view.sidepanel.absorbTogg.config(text='ABSORPTION LINE:OFF')
        else:
            self.model.specUtilObj.addAbsorbLine()
            self.view.updateFigure(self.model.specUtilObj.shownFig)
            self.view.sidepanel.absorbTogg.config(text='ABSORPTION LINE:ON')
    def modelTogg(self,event):
        if self.view.sidepanel.modelTogg.config('text')[-1].endswith('ON'):
            #update the model
            self.model.specUtilObj.removeModel()
            self.view.updateFigure(self.model.specUtilObj.shownFig)
            self.view.sidepanel.modelTogg.config(text='BEST FIT MODEL:OFF')
        else:
            self.model.specUtilObj.addModel()
            self.view.updateFigure(self.model.specUtilObj.shownFig)
            self.view.sidepanel.modelTogg.config(text='BEST FIT MODEL:ON')

class SpecModel:
    def __init__(self,coaddObj,zObj):
        self.specUtilObj = SpecUtil.SpecUtil(coaddObj, zObj)
    #take data to self construct
    # this is where plot happens
    #Figure composing
class SidePanel():
    def __init__(self, root):
        self.frame2 = Tk.Frame(root)
        self.frame2.pack(side=Tk.LEFT, fill=Tk.BOTH, expand=1)


        #TODO:put in toggle button for all the function
        self.fluxTogg = Tk.Button(self.frame2, text="FLUX:ON")
        self.fluxTogg.pack(side="top", fill=Tk.BOTH)
        self.skylineTogg = Tk.Button(self.frame2, text="SKYLINE:ON")
        self.skylineTogg.pack(side="top", fill=Tk.BOTH)
        self.emissionTogg = Tk.Button(self.frame2, text="EMISSION LINE:ON")
        self.emissionTogg.pack(side="top", fill=Tk.BOTH)
        self.absorbTogg = Tk.Button(self.frame2, text="ABSORPTION LINE:ON")
        self.absorbTogg.pack(side="top", fill=Tk.BOTH)
        self.modelTogg = Tk.Button(self.frame2, text="BEST FIT MODEL:ON")
        self.modelTogg.pack(side="top", fill=Tk.BOTH)
class SpecView(Tk.Toplevel):
    def __init__(self,master,figure):
        self.sidepanel = SidePanel(master)
        self.figure =figure
        self.canvas = FigureCanvasTkAgg(self.figure, master=master)
        self.canvas.show()
        self.canvas.get_tk_widget().pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)

        toolbar = NavigationToolbar2TkAgg(self.canvas, master)

        toolbar.update()
        self.canvas._tkcanvas.pack(side=Tk.TOP, fill=Tk.BOTH, expand=1)
        self.connectKey()

    def updateFigure(self,figure):
        self.figure = figure
        self.figure.canvas.draw()
    def on_key_event(self,event):
        print('you pressed %s' % event.key)
        key_press_handler(event, self.canvas, self.toolbar)
    def connectKey(self):
        self.canvas.mpl_connect('key_press_event', self.on_key_event)
    # generate
