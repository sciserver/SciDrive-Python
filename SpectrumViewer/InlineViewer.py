import SpectrumViewer.SpecUtil_inline as inline
import SpectrumViewer.SDSSDriver as driver
def view(filename, filesource):
    coaddObj,zObj=driver.loadFITS(filename, filesource)
    spec = inline.SpecUtil(filename, coaddObj, zObj)
    spec.showfig()
