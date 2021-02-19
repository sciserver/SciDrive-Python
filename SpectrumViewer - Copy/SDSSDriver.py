#load SDSS into workable object
from astropy.io import fits
#from py3.SciServer import Authentication, Config
#from py3.SciServer import CasJobs
from urllib.parse import urlparse
import SpectrumViewer.CoaddObj as Coadd
import SpectrumViewer.ZObj as Z
# def getSpecObjID(ra, dec, width, height, context=None, URL=True):
#     leftBoundry = ra - width / 2
#     rightBoundry = ra + width / 2
#     upperBoundry = dec + height / 2
#     lowerBoundry = dec - height / 2
#     sqlQuery = 'select specObjID from dr7.specobjall Where (ra >' + str(leftBoundry) + ' and ra<' + str(
#         rightBoundry) + ') and (dec>' + str(lowerBoundry) + ' and dec<' + str(upperBoundry) + ')'
#     return CasJobs.executeQuery(sqlQuery, context='dr7', format='pandas')
# def getRawFITSPathInDAS(SpecObjID):
#     sqlQuery = 'select dr7.fGetUrlFitsSpectrum('+SpecObjID+')'
#     response = CasJobs.executeQuery(sqlQuery, context='dr7', format='pandas')
#     url= response['Column1'][0]
#     parseResult = urlparse(url)
#     prefix = '/home/idies/workspace/sdss_das/das2'
#     path = prefix+parseResult.path
#     return path

def loadFITS(filename,fileSource):

    if fileSource=='SDSS':
        coaddData =1
        zData =3
        hdulist = fits.open(filename)
        c=hdulist[coaddData].data
        z=hdulist[zData].data
        coaddObj = Coadd.CoaddObj(
            flux=c['flux'],
            loglam=c['loglam'],
            ivar=c['ivar'],
            andMask=c['and_Mask'],
            orMask=c['or_Mask'],
            wdisp=c['wdisp'],
            sky = c['sky'],
            model=c['model'])
        zObj = Z.ZObj(
            LINENAME=z['LINENAME'],
            LINEWAVE=z['LINEWAVE'],
            LINEZ=z['LINEZ'],
            LINEEW=z['LINEEW'],
            LINEZ_ERR=z['LINEZ_ERR'],
            LINEEW_ERR=z['LINEEW_ERR'])
        return coaddObj,zObj

    else:
        print('Sorry, we are loyal to SDSS ONLY, for the time being. ')