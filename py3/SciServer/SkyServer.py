import requests
import pandas
import skimage.io
import urllib
#import json

from io import StringIO
from io import BytesIO
from astropy.io import fits
from py3.SciServer import Authentication, Config
from py3.SciServer import CasJobs
from urllib.parse import urlparse

def sqlSearch(sql, dataRelease=None):
    """
    Executes a SQL query to the SDSS database, and retrieves the result table as a dataframe. Maximum number of rows retrieved is set currently to 500,000.

    :param sql: a string containing the sql query
    :param dataRelease: SDSS data release (string). E.g, 'DR13'. Default value already set in SciServer.Config.DataRelease
    :return: Returns the results table as a Pandas data frame.
    :raises: Throws an exception if the HTTP request to the SkyServer API returns an error.
    :example: df = SkyServer.sqlSearch(sql="select 1")

    .. seealso:: CasJobs.executeQuery, CasJobs.submitJob.
    """
    if(dataRelease):
        if dataRelease != "":
            url = Config.SkyServerWSurl + '/' + dataRelease + '/SkyServerWS/SearchTools/SqlSearch?'
        else:
            url = Config.SkyServerWSurl + '/SkyServerWS/SearchTools/SqlSearch?'
    else:
        if Config.DataRelease != "":
            url = Config.SkyServerWSurl + '/' + Config.DataRelease + '/SkyServerWS/SearchTools/SqlSearch?'
        else:
            url = Config.SkyServerWSurl + '/SkyServerWS/SearchTools/SqlSearch?'

    url = url + 'format=csv&'
    url = url + 'cmd=' + sql + '&'

    if Config.isSciServerComputeEnvironment():
        url = url + "TaskName=Compute.SciScript-Python.SkyServer.sqlSearch&"
    else:
        url = url + "TaskName=SciScript-Python.SkyServer.sqlSearch&"

    #url = urllib.quote_plus(url)
    acceptHeader = "text/plain"
    headers = {'Content-Type': 'application/json', 'Accept': acceptHeader}

    token = Authentication.getToken()
    if token is not None and token != "":
        headers['X-Auth-Token'] = token

    response = requests.get(url,headers=headers, stream=True)
    if response.status_code != 200:
        raise Exception("Error when executing a sql query.\nHttp Response from SkyServer API returned status code " + str(response.status_code) + ":\n" + response.content.decode());

    r=response.content.decode();
    return pandas.read_csv(StringIO(r), comment='#', index_col=None)


def getJpegImgCutout(ra, dec, scale=0.7, width=512, height=512, opt="", query="", dataRelease=None):
    """
    Gets a rectangular image cutout from a region of the sky in SDSS, centered at (ra,dec). Return type is numpy.ndarray.\n

    :param ra: Right Ascension of the image's center in floating point ICRS J2000 coordinates.
    :param dec: Declination of the image's center in floating point ICRS J2000 coordinates.
    :param scale: Scale of the image, measured in [arcsec/pix]
    :param width: Width of image, measured in pixels (width in arcsec = width * scale). If larger than 2048, silently truncated to 2048.
    :param height: Height of image, measured in pixels (width in arcsec = width * scale). If larger than 2048, silently truncated to 2048.
    :param opt: Optional drawing options, expressed as concatenation of letters (string). The letters options are \n
    \t"G": Grid. Draw a N-S E-W grid through the center\n
    \t"L": Label. Draw the name, scale, ra, and dec on image.\n
    \t"P PhotoObj. Draw a small cicle around each primary photoObj.\n
    \t"S: SpecObj. Draw a small square around each specObj.\n
    \t"O": Outline. Draw the outline of each photoObj.\n
    \t"B": Bounding Box. Draw the bounding box of each photoObj.\n
    \t"F": Fields. Draw the outline of each field.\n
    \t"M": Masks. Draw the outline of each mask considered to be important.\n
    \t"Q": Plates. Draw the outline of each plate.\n
    \t"I": Invert. Invert the image (B on W).\n
    \t(see http://skyserver.sdss.org/public/en/tools/chart/chartinfo.aspx)\n
    :param query: Optional string. Marks with inverted triangles on the image the position of user defined objects. The (RA,Dec) coordinates of these object can be given by three means:\n
    \t1) query is a SQL command of format "SELECT Id, RA, Dec, FROM Table".
    \t2) query is list of objects. A header with RA and DEC columns must be included. Columns must be separated by tabs, spaces, commas or semicolons. The list may contain as many columns as wished.
    \t3) query is a string following the pattern: ObjType Band (low_mag, high_mag).
    \t\tObjType: S | G | P marks Stars, Galaxies or PhotoPrimary objects.\n
    \t\tBand: U | G | R | I | Z | A restricts marks to objects with Band BETWEEN low_mag AND high_mag Band 'A' will mark all objects within the specified magnitude range in any band (ORs composition).\n
    \tExamples:\n
    \t\tS\n
    \t\tS R (0.0, 23.5)\n
    \t\tG A (20, 30)\n
    \t\t(see http://skyserver.sdss.org/public/en/tools/chart/chartinfo.aspx)\n
    :param dataRelease: SDSS data release string. Example: dataRelease='DR13'. Default value already set in SciServer.Config.DataRelease
    :return: Returns the image as a numpy.ndarray object.
    :raises: Throws an exception if the HTTP request to the SkyServer API returns an error.
    :example: img = SkyServer.getJpegImgCutout(ra=197.614455642896, dec=18.438168853724, width=512, height=512, scale=0.4, opt="OG", query="SELECT TOP 100 p.objID, p.ra, p.dec, p.r FROM fGetObjFromRectEq(197.6,18.4,197.7,18.5) n, PhotoPrimary p WHERE n.objID=p.objID")
    """
    if(dataRelease):
        if dataRelease != "":
            url = Config.SkyServerWSurl + '/' + dataRelease + '/SkyServerWS/ImgCutout/getjpeg?'
        else:
            url = Config.SkyServerWSurl + '/SkyServerWS/ImgCutout/getjpeg?'
    else:
        if Config.DataRelease != "":
            url = Config.SkyServerWSurl + '/' + Config.DataRelease + '/SkyServerWS/ImgCutout/getjpeg?'
        else:
            url = Config.SkyServerWSurl + '/SkyServerWS/ImgCutout/getjpeg?'

    url = url + 'ra=' + str(ra) + '&'
    url = url + 'dec=' + str(dec) + '&'
    url = url + 'scale=' + str(scale) + '&'
    url = url + 'width=' + str(width) + '&'
    url = url + 'height=' + str(height) + '&'
    url = url + 'opt=' + opt + '&'
    url = url + 'query=' + query + '&'

    if Config.isSciServerComputeEnvironment():
        url = url + "TaskName=Compute.SciScript-Python.SkyServer.getJpegImgCutout&"
    else:
        url = url + "TaskName=SciScript-Python.SkyServer.getJpegImgCutout&"

    #url = urllib.quote_plus(url)
    acceptHeader = "text/plain"
    headers = {'Content-Type': 'application/json', 'Accept': acceptHeader}

    token = Authentication.getToken()
    if token is not None and token != "":
        headers['X-Auth-Token'] = token

    response = requests.get(url,headers=headers, stream=True)
    if response.status_code != 200:
        if response.status_code == 404 or response.status_code == 500:
            raise Exception("Error when getting an image cutout.\nHttp Response from SkyServer API returned status code " + str(response.status_code) + ". " + response.reason);
        else:
            raise Exception("Error when getting an image cutout.\nHttp Response from SkyServer API returned status code " + str(response.status_code) + ":\n" + response.content.decode());

    return skimage.io.imread( BytesIO( response.content))

def radialSearch(ra, dec, radius=1, coordType="equatorial", whichPhotometry="optical", limit="10", dataRelease=None):
    """
    Runs a query in the SDSS database that searches for all objects within a certain radius from a point in the sky, and retrieves the result table as a Panda's dataframe.\n

    :param ra: Right Ascension of the image's center.\n
    :param dec: Declination of the image's center.\n
    :param radius: Search radius around the (ra,dec) coordinate in the sky. Measured in arcminutes.\n
    :param coordType: Type of celestial coordinate system. Can be set to "equatorial" or "galactic".\n
    :param whichPhotometry: Type of retrieved data. Can be set to "optical" or "infrared".\n
    :param limit: Maximum number of rows in the result table (string). If set to "0", then the function will return all rows.\n
    :param dataRelease: SDSS data release string. Example: dataRelease='DR13'. Default value already set in SciServer.Config.DataRelease
    :return: Returns the results table as a Pandas data frame.
    :raises: Throws an exception if the HTTP request to the SkyServer API returns an error.
    :example: df = SkyServer.radialSearch(ra=258.25, dec=64.05, radius=3)

    .. seealso:: SkyServer.sqlSearch, SkyServer.rectangularSearch.
    """
    if(dataRelease):
        if dataRelease != "":
            url = Config.SkyServerWSurl + '/' + dataRelease + '/SkyServerWS/SearchTools/RadialSearch?'
        else:
            url = Config.SkyServerWSurl + '/SkyServerWS/SearchTools/RadialSearch?'
    else:
        if Config.DataRelease != "":
            url = Config.SkyServerWSurl + '/' + Config.DataRelease + '/SkyServerWS/SearchTools/RadialSearch?'
        else:
            url = Config.SkyServerWSurl + '/SkyServerWS/SearchTools/RadialSearch?'

    url = url + 'format=csv&'
    url = url + 'ra=' + str(ra) + '&'
    url = url + 'dec=' + str(dec) + '&'
    url = url + 'radius=' + str(radius) + '&'
    url = url + 'coordType=' + coordType + '&'
    url = url + 'whichPhotometry=' + whichPhotometry + '&'
    url = url + 'limit=' + limit + '&'

    if Config.isSciServerComputeEnvironment():
        url = url + "TaskName=Compute.SciScript-Python.SkyServer.radialSearch&"
    else:
        url = url + "TaskName=SciScript-Python.SkyServer.radialSearch&"

    #url = urllib.quote_plus(url)
    acceptHeader = "text/plain"
    headers = {'Content-Type': 'application/json', 'Accept': acceptHeader}

    token = Authentication.getToken()
    if token is not None and token != "":
        headers['X-Auth-Token'] = token

    response = requests.get(url,headers=headers, stream=True)
    if response.status_code != 200:
        raise Exception("Error when executing a radial search.\nHttp Response from SkyServer API returned status code " + str(response.status_code) + ":\n" + response.content.decode());

    r=response.content.decode();
    return pandas.read_csv(StringIO(r), comment='#', index_col=None)


def rectangularSearch(min_ra, max_ra, min_dec, max_dec, coordType="equatorial", whichPhotometry="optical", limit="10", dataRelease=None):
    """
    Runs a query in the SDSS database that searches for all objects within a certain rectangular box defined on the the sky, and retrieves the result table as a Panda's dataframe.\n

    :param min_ra: Minimum value of Right Ascension coordinate that defines the box boundaries on the sky.\n
    :param max_ra: Maximum value of Right Ascension coordinate that defines the box boundaries on the sky.\n
    :param min_dec: Minimum value of Declination coordinate that defines the box boundaries on the sky.\n
    :param max_dec: Maximum value of Declination coordinate that defines the box boundaries on the sky.\n
    :param coordType: Type of celestial coordinate system. Can be set to "equatorial" or "galactic".\n
    :param whichPhotometry: Type of retrieved data. Can be set to "optical" or "infrared".\n
    :param limit: Maximum number of rows in the result table (string). If set to "0", then the function will return all rows.\n
    :param dataRelease: SDSS data release string. Example: dataRelease='DR13'. Default value already set in SciServer.Config.DataRelease
    :return: Returns the results table as a Pandas data frame.
    :raises: Throws an exception if the HTTP request to the SkyServer API returns an error.
    :example: df = SkyServer.rectangularSearch(min_ra=258.2, max_ra=258.3, min_dec=64,max_dec=64.1)

    .. seealso:: SkyServer.sqlSearch, SkyServer.radialSearch.
    """
    if(dataRelease):
        if dataRelease != "":
            url = Config.SkyServerWSurl + '/' + dataRelease + '/SkyServerWS/SearchTools/RectangularSearch?'
        else:
            url = Config.SkyServerWSurl + '/SkyServerWS/SearchTools/RectangularSearch?'
    else:
        if Config.DataRelease != "":
            url = Config.SkyServerWSurl + '/' + Config.DataRelease + '/SkyServerWS/SearchTools/RectangularSearch?'
        else:
            url = Config.SkyServerWSurl + '/SkyServerWS/SearchTools/RectangularSearch?'

    url = url + 'format=csv&'
    url = url + 'min_ra=' + str(min_ra) + '&'
    url = url + 'max_ra=' + str(max_ra) + '&'
    url = url + 'min_dec=' + str(min_dec) + '&'
    url = url + 'max_dec=' + str(max_dec) + '&'
    url = url + 'coordType=' + coordType + '&'
    url = url + 'whichPhotometry=' + whichPhotometry + '&'
    url = url + 'limit=' + limit + '&'

    if Config.isSciServerComputeEnvironment():
        url = url + "TaskName=Compute.SciScript-Python.SkyServer.rectangularSearch&"
    else:
        url = url + "TaskName=SciScript-Python.SkyServer.rectangularSearch&"

    #url = urllib.quote_plus(url)
    acceptHeader = "text/plain"
    headers = {'Content-Type': 'application/json', 'Accept': acceptHeader}

    token = Authentication.getToken()
    if token is not None and token != "":
        headers['X-Auth-Token'] = token

    response = requests.get(url,headers=headers, stream=True)
    if response.status_code != 200:
        raise Exception("Error when executing a rectangular search.\nHttp Response from SkyServer API returned status code " + str(response.status_code) + ":\n" + response.content.decode());

    r=response.content.decode();
    return pandas.read_csv(StringIO(r), comment='#', index_col=None)


def objectSearch(objId=None, specObjId=None, apogee_id=None, apstar_id=None, ra=None, dec=None, plate=None, mjd=None, fiber=None, run=None, rerun=None, camcol=None, field=None, obj=None, dataRelease=None):
    """
    Gets the properties of the the object that is being searched for. Search parameters:\n

    :param objId: SDSS ObjId.\n
    :param specObjId: SDSS SpecObjId.\n
    :param apogee_id: ID idetifying Apogee target object.\n
    :param apstar_id: unique ID for combined apogee star spectrum.\n
    :param ra: right ascention.\n
    :param dec: declination.\n
    :param plate: SDSS plate number.\n
    :param mjd: Modified Julian Date of observation.\n
    :param fiber: SDSS fiber number.\n
    :param run: SDSS run number.\n
    :param rerun: SDSS rerun number.\n
    :param camcol: SDSS camera column.\n
    :param field: SDSS field number.\n
    :param obj: The object id within a field.\n
    :param dataRelease: SDSS data release string. Example: dataRelease='DR13'. Default value already set in SciServer.Config.DataRelease
    :return: Returns a list containing the properties and metadata of the astronomical object found.
    :raises: Throws an exception if the HTTP request to the SkyServer API returns an error.
    :example: object = SkyServer.objectSearch(ra=258.25, dec=64.05)

    .. seealso:: SkyServer.sqlSearch, SkyServer.rectangularSearch, SkyServer.radialSearch.
    """
    if(dataRelease):
        if dataRelease != "":
            url = Config.SkyServerWSurl + '/' + dataRelease + '/SkyServerWS/SearchTools/ObjectSearch?query=LoadExplore&'
        else:
            url = Config.SkyServerWSurl + '/SkyServerWS/SearchTools/ObjectSearch?query=LoadExplore&'
    else:
        if Config.DataRelease != "":
            url = Config.SkyServerWSurl + '/' + Config.DataRelease + '/SkyServerWS/SearchTools/ObjectSearch?query=LoadExplore&'
        else:
            url = Config.SkyServerWSurl + '/SkyServerWS/SearchTools/ObjectSearch?query=LoadExplore&'

    url = url + 'format=json&'
    if(objId):
        url = url + 'objid=' + str(objId) + '&';
    if(specObjId):
        url = url + 'specobjid=' + str(specObjId) + '&';
    if(apogee_id):
        url = url + 'apid=' + str(apogee_id) + '&';
    else:
        if(apstar_id):
            url = url + 'apid=' + str(apstar_id) + '&';
    if(ra):
        url = url + 'ra=' + str(ra) + '&';
    if(dec):
        url = url + 'dec=' + str(dec) + '&';
    if(plate):
        url = url + 'plate=' + str(plate) + '&';
    if(mjd):
        url = url + 'mjd=' + str(mjd) + '&';
    if(fiber):
        url = url + 'fiber=' + str(fiber) + '&';
    if(run):
        url = url + 'run=' + str(run) + '&';
    if(rerun):
        url = url + 'rerun=' + str(rerun) + '&';
    if(camcol):
        url = url + 'camcol=' + str(camcol) + '&';
    if(field):
        url = url + 'field=' + str(field) + '&';
    if(obj):
        url = url + 'obj=' + str(obj) + '&';

    if Config.isSciServerComputeEnvironment():
        url = url + "TaskName=Compute.SciScript-Python.SkyServer.objectSearch&"
    else:
        url = url + "TaskName=SciScript-Python.SkyServer.objectSearch&"

    #url = urllib.quote_plus(url)
    acceptHeader = "text/plain"
    headers = {'Content-Type': 'application/json', 'Accept': acceptHeader}

    token = Authentication.getToken()
    if token is not None and token != "":
        headers['X-Auth-Token'] = token

    response = requests.get(url,headers=headers, stream=True)
    if response.status_code != 200:
        raise Exception("Error when doing an object search.\nHttp Response from SkyServer API returned status code " + str(response.status_code) + ":\n" + response.content.decode());

    #r=response.content.decode();
    r = response.json()
    #r = json.loads(response.content.decode())
    #return pandas.read_csv(StringIO(r), comment='#')
    return r;

    # TODO: get a list of FITS path given a list of object ID and
    # TODO: make a new function that return a hdu object from FITS file after solve the fits.open() warning problem
#1: use casjobs to query for the specobjid by the coordinate
#2: use dr7.fgeturlfitsspectrum(specobjid) to have the http url:
# like this http://das.sdss.org/spectro/1d_26/1472/1d/spSpec-52913-1472-269.fit
# then append sdss_das/das2/ in the front


def getSpecObjID(ra, dec, width, height, context=None, URL=True):
    leftBoundry = ra - width / 2
    rightBoundry = ra + width / 2
    upperBoundry = dec + height / 2
    lowerBoundry = dec - height / 2
    sqlQuery = 'select specObjID from dr7.specobjall Where (ra >' + str(leftBoundry) + ' and ra<' + str(
        rightBoundry) + ') and (dec>' + str(lowerBoundry) + ' and dec<' + str(upperBoundry) + ')'
    return CasJobs.executeQuery(sqlQuery, context='dr7', format='pandas')
def getRawFITSPathInDAS(SpecObjID):
    sqlQuery = 'select dr7.fGetUrlFitsSpectrum('+SpecObjID+')'
    response = CasJobs.executeQuery(sqlQuery, context='dr7', format='pandas')
    url= response['Column1'][0]
    parseResult = urlparse(url)
    prefix = '/home/idies/workspace/sdss_das/das2'
    path = prefix+parseResult.path
    return path