import SciServer.SepctrumViewer.SDSSDriver as driver
import SciServer.SepctrumViewer.WindowViewer as viewer
objID= 'please replace this with an objID from SDSS DR7'
filesource='SDSS'
path=driver.getRawFITSPathInDAS(objID)
viewer.view(path,filesource)
