import SpectrumViewer.SpecUtil_inline as inline

import SpectrumViewer.SDSSDriver as driver
fileName = 'example_lite.fits'
fileSource = 'SDSS'
coaddObj, zObj = driver.loadFITS(fileName, fileSource)
spec=inline.SpecUtil(coaddObj, zObj)
spec.showfig()


