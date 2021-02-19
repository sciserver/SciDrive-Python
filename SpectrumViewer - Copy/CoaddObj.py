# This class init with a fits file in the directory and store all the data in the RAM
import numpy as np
class CoaddObj:
    def __init__(self,flux,loglam=None,ivar=None,andMask=None,orMask=None
                 ,wdisp=None,sky=None,model=None):#type can be pfs
        self.flux = flux
        self.loglam = loglam
        self.ivar =ivar
        self.andMask =andMask
        self.orMask = orMask
        self.wdisp = wdisp
        self.sky =sky
        self.model = model
        self.lam = np.power(10,self.loglam)



