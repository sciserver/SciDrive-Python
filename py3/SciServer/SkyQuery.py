import json

import sys
from io import StringIO

import requests
import pandas
import time

from SciServer import Authentication, Config


######################################################################################################################
# Jobs:


def getJobStatus(jobID):
    """
    Gets the status of a job, as well as other related metadata (more info in http://www.voservices.net/skyquery).

    :param jobID: the ID of the job (string), which is obtained at the moment of submitting the job.
    :return: a dictionary with the job status and other related metadata.
    :raises: Throws an exception if the user is not logged into SciServer (use Authentication.login for that purpose). Throws an exception if the HTTP request to the SkyQuery API returns an error.
    :example: status = SkyQuery.getJobStatus(SkyQuery.submitJob("select 1 as foo"))

    .. seealso:: SkyQuery.submitJob, SkyQuery.cancelJob
    """
    token = Authentication.getToken()
    if token is not None and token != "":
        statusURL = Config.SkyQueryUrl + '/Jobs.svc/jobs/' + str(jobID)

        headers = {'Content-Type': 'application/json','Accept': 'application/json'}
        headers['X-Auth-Token']=  token

        response = requests.get(statusURL, headers=headers)

        if response.status_code == 200:
            r = response.json()
            return(r['queryJob'])
        else:
            raise Exception("Error when getting the job status of job " + str(jobID) + ".\nHttp Response from SkyQuery API returned status code " + str(response.status_code) + ":\n" + response.content.decode());
    else:
        raise Exception("User token is not defined. First log into SciServer.")


def cancelJob(jobID):
    """
    Cancels a single job (more info in http://www.voservices.net/skyquery).

    :param jobID: the ID of the job, which is obtained at the moment of submitting the job.
    :return: Returns True if the job was cancelled successfully.
    :raises: Throws an exception if the user is not logged into SciServer (use Authentication.login for that purpose). Throws an exception if the HTTP request to the SkyQuery API returns an error.
    :example: isCanceled = SkyQuery.cancelJob(SkyQuery.submitJob("select 1 as foo"))

    .. seealso:: SkyQuery.submitJob, SkyQuery.getJobStatus
    """
    token = Authentication.getToken()
    if token is not None and token != "":

        statusURL = Config.SkyQueryUrl + '/Jobs.svc/jobs/' + jobID

        headers = {'Content-Type': 'application/json','Accept': 'application/json'}
        headers['X-Auth-Token']=  token

        response = requests.delete(statusURL, headers=headers)

        if response.status_code == 200:
            #r = response.json()
            #try:
            #    status = r['queryJob']["status"]
            #    if status == "canceled":
            #        return True;
            #    else:
            #        return False;
            #except:
            #    return False;
            return True;
        else:
            raise Exception("Error when cancelling job " + str(jobID) + ".\nHttp Response from SkyQuery API returned status code " + str(response.status_code) + ":\n" + response.content.decode());
    else:
        raise Exception("User token is not defined. First log into SciServer.")


def listQueues():
    """
    Returns a list of all available job queues and related metadata (more info in http://www.voservices.net/skyquery).

    :return: a list of all available job queues and related metadata.
    :raises: Throws an exception if the user is not logged into SciServer (use Authentication.login for that purpose). Throws an exception if the HTTP request to the SkyQuery API returns an error.
    :example: queueList = SkyQuery.listQueues()

    .. seealso:: SkyQuery.getQueueInfo, SkyQuery.submitJob, SkyQuery.getJobStatus
    """
    token = Authentication.getToken()
    if token is not None and token != "":
        jobsURL = Config.SkyQueryUrl + '/Jobs.svc/queues'

        headers = {'Content-Type': 'application/json','Accept': 'application/json'}
        headers['X-Auth-Token']=  token

        response = requests.get(jobsURL, headers=headers)

        if response.status_code == 200:
            r = response.json()
            return(r['queues'])
        else:
            raise Exception("Error when listing queues.\nHttp Response from SkyQuery API returned status code " + str(response.status_code) + ":\n" + response.content.decode());
    else:
        raise Exception("User token is not defined. First log into SciServer.")


def getQueueInfo(queue):
    """
 	Returns information about a particular job queue (more info in http://www.voservices.net/skyquery).

 	:param queue: queue name (string)
    :return: a dictionary containing information associated to the queue.
    :raises: Throws an exception if the user is not logged into SciServer (use Authentication.login for that purpose). Throws an exception if the HTTP request to the SkyQuery API returns an error.
    :example: queueInfo = SkyQuery.getQueueInfo('quick')

    .. seealso:: SkyQuery.listQueues, SkyQuery.submitJob, SkyQuery.getJobStatus
 	"""
    token = Authentication.getToken()
    if token is not None and token != "":

        jobsURL = Config.SkyQueryUrl + '/Jobs.svc/queues/' + queue

        headers = {'Content-Type': 'application/json','Accept': 'application/json'}
        headers['X-Auth-Token']=  token

        response = requests.get(jobsURL, headers=headers)

        if response.status_code == 200:
            r = response.json()
            return(r['queue'])
        else:
            raise Exception("Error when getting queue info of " + str(queue) + ".\nHttp Response from SkyQuery API returned status code " + str(response.status_code) + ":\n" + response.content.decode());
    else:
        raise Exception("User token is not defined. First log into SciServer.")


def submitJob(query, queue='quick'):
    """
    Submits a new job (more info in http://www.voservices.net/skyquery).

    :param query: sql query (string)
    :param queue: queue name (string). Can be set to 'quick' for a quick job, or 'long' for a long job.
    :return: returns the jobID (string), unique identifier of the job.
    :raises: Throws an exception if the user is not logged into SciServer (use Authentication.login for that purpose). Throws an exception if the HTTP request to the SkyQuery API returns an error.
    :example: jobId = SkyQuery.submitJob('select 1 as foo', "quick")

    .. seealso:: SkyQuery.getJobStatus, SkyQuery.listQueues
    """
    token = Authentication.getToken()
    if token is not None and token != "":

        jobsURL = Config.SkyQueryUrl + '/Jobs.svc/queues/' + queue + '/jobs'

        headers = {'Content-Type': 'application/json','Accept': 'application/json'}
        headers['X-Auth-Token']=  token

        body={"queryJob":{"query":query}}

        data=json.dumps(body).encode()

        response = requests.post(jobsURL,data=data,headers=headers)

        if response.status_code == 200:
            r = response.json()
            return(r['queryJob']['guid'])
        else:
            raise Exception("Error when submitting job on queue " + str(queue) + ".\nHttp Response from SkyQuery API returned status code " + str(response.status_code) + ":\n" + response.content.decode());
    else:
        raise Exception("User token is not defined. First log into SciServer.")


def waitForJob(jobid, verbose=True):
    """
    Queries the job status from SkyQuery every 2 seconds and waits for the SkyQuery job to be completed.

    :param jobid: id of job (integer)
    :param verbose: if True, will print "wait" messages on the screen while the job is not done. If False, will suppress printing messages on the screen.
    :return: After the job is finished, returns a dictionary object containing the job status and related metadata.
    :raises: Throws an exception if the user is not logged into SciServer (use Authentication.login for that purpose). Throws an exception if the HTTP request to the SkyQuery API returns an error.
    :example: SkyQuery.waitForJob(SkyQuery.submitJob("select 1"))

    .. seealso:: SkyQuery.submitJob, SkyQuery.getJobStatus.
    """
    try:
        complete = False

        waitingStr = "Waiting..."
        back = "\b" * len(waitingStr)
        if verbose:
            print(waitingStr, end="")

        while not complete:
            if verbose:
                #print(back, end="")
                print(waitingStr, end="")
            jobDesc = getJobStatus(jobid)
            if jobDesc['status'] == 'completed':
                complete = True
                if verbose:
                    #print(back, end="")
                    print "Done!"
            else:
                time.sleep(2)

        return jobDesc
    except Exception as e:
        raise e;



def listJobs(queue="quick"):
    """
    Lists the jobs in the queue in descending order by submission time. Only jobs of the authenticated user are listed (more info in http://www.voservices.net/skyquery).

    :param queue: queue name (string). Can be set to 'quick' for a quick job, or 'long' for a long job.
    :return: returns job definitions as a list object.
    :raises: Throws an exception if the user is not logged into SciServer (use Authentication.login for that purpose). Throws an exception if the HTTP request to the SkyQuery API returns an error.
    :example: jobsList = SkyQuery.listJobs('quick')

    .. seealso:: SkyQuery.getJobStatus, SkyQuery.listQueues
    """
    token = Authentication.getToken()
    if token is not None and token != "":
        jobsURL = Config.SkyQueryUrl + '/Jobs.svc/queues/' + queue + '/jobs?'

        headers = {'Content-Type': 'application/json','Accept': 'application/json'}
        headers['X-Auth-Token']=  token

        response = requests.get(jobsURL,headers=headers)

        if response.status_code == 200:
            r = response.json()
            return(r['jobs'])
        else:
            raise Exception("Error when listing jobs on queue " + str(queue) + ".\nHttp Response from SkyQuery API returned status code " + str(response.status_code) + ":\n" + response.content.decode());

    else:
        raise Exception("User token is not defined. First log into SciServer.")


######################################################################################################################
# Schema:


def listAllDatasets():
    """
    Lists all available datasets (more info in http://www.voservices.net/skyquery).

    :return: returns dataset definitions as a list object.
    :raises: Throws an exception if the user is not logged into SciServer (use Authentication.login for that purpose). Throws an exception if the HTTP request to the SkyQuery API returns an error.
    :example: datasets = SkyQuery.listAllDatasets()

    .. seealso:: SkyQuery.listQueues, SkyQuery.getDatasetInfo, SkyQuery.listDatasetTables, SkyQuery.getTableInfo, SkyQuery.listTableColumns, SkyQuery.getTable, SkyQuery.dropTable
    """

    token = Authentication.getToken()
    if token is not None and token != "":

        schemaURL = Config.SkyQueryUrl + '/Schema.svc/datasets'

        headers = {'Content-Type': 'application/json','Accept': 'application/json'}
        headers['X-Auth-Token']=  token

        response = requests.get(schemaURL, headers=headers)

        if response.status_code == 200:
            r = response.json()
            return(r['datasets'])
        else:
            raise Exception("Error when listing all datasets.\nHttp Response from SkyQuery API returned status code " + str(response.status_code) + ":\n" + response.content.decode());
    else:
        raise Exception("User token is not defined. First log into SciServer.")


def getDatasetInfo(datasetName="MyDB"):
    """
    Gets information related to a particular dataset (more info in http://www.voservices.net/skyquery).

    :param datasetName: name of dataset (string).
    :return: returns a dictionary containing the dataset information.
    :raises: Throws an exception if the user is not logged into SciServer (use Authentication.login for that purpose). Throws an exception if the HTTP request to the SkyQuery API returns an error.
    :example: info = SkyQuery.getDatasetInfo("MyDB")

    .. seealso:: SkyQuery.listQueues, SkyQuery.listAllDatasets, SkyQuery.listDatasetTables, SkyQuery.getTableInfo, SkyQuery.listTableColumns, SkyQuery.getTable, SkyQuery.dropTable
    """
    token = Authentication.getToken()
    if token is not None and token != "":
        schemaURL = Config.SkyQueryUrl + '/Schema.svc/datasets/' +  datasetName

        headers = {'Content-Type': 'application/json','Accept': 'application/json'}
        headers['X-Auth-Token']=  token

        response = requests.get(schemaURL, headers=headers)

        if response.status_code == 200:
            return(response.json())
        else:
            raise Exception("Error when getting info from dataset " + str(datasetName) + ".\nHttp Response from SkyQuery API returned status code " + str(response.status_code) + ":\n" + response.content.decode());
    else:
        raise Exception("User token is not defined. First log into SciServer.")


def listDatasetTables(datasetName="MyDB"):
    """
    Returns a list of all tables within a dataset (more info in http://www.voservices.net/skyquery).

    :param datasetName: name of dataset (string).
    :return: returns a list containing the tables and associated descriptions/metadata.
    :raises: Throws an exception if the user is not logged into SciServer (use Authentication.login for that purpose). Throws an exception if the HTTP request to the SkyQuery API returns an error.
    :example: tables = SkyQuery.listDatasetTables("MyDB")

    .. seealso:: SkyQuery.listQueues, SkyQuery.listAllDatasets, SkyQuery.getDatasetInfo, SkyQuery.getTableInfo, SkyQuery.listTableColumns, SkyQuery.getTable, SkyQuery.dropTable
    """
    token = Authentication.getToken()
    if token is not None and token != "":
        url = Config.SkyQueryUrl + '/Schema.svc/datasets/' + datasetName +'/tables'

        headers = {'Content-Type': 'application/json','Accept': 'application/json'}
        headers['X-Auth-Token']=  token

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            r = response.json()
            return(r['tables'])
        else:
            raise Exception("Error when listing tables in dataset " + str(datasetName) + ".\nHttp Response from SkyQuery API returned status code " + str(response.status_code) + ":\n" + response.content.decode());
    else:
        raise Exception("User token is not defined. First log into SciServer.")


def getTableInfo(tableName, datasetName="MyDB"):
    """
    Returns info about a particular table belonging to a dataset (more info in http://www.voservices.net/skyquery).

    :param tableName: name of table (string) within dataset.
    :param datasetName: name of dataset (string).
    :return: returns a dictionary containing the table properties and associated info/metadata.
    :raises: Throws an exception if the user is not logged into SciServer (use Authentication.login for that purpose). Throws an exception if the HTTP request to the SkyQuery API returns an error.
    :example: info = SkyQuery.getTableInfo("myTable", datasetName="MyDB")

    .. seealso:: SkyQuery.listQueues, SkyQuery.listAllDatasets, SkyQuery.getDatasetInfo, SkyQuery.listDatasetTables, SkyQuery.listTableColumns, SkyQuery.getTable, SkyQuery.dropTable
    """
    token = Authentication.getToken()
    if token is not None and token != "":
        url = Config.SkyQueryUrl + '/Schema.svc/datasets/' + datasetName +'/tables/' + tableName

        headers = {'Content-Type': 'application/json','Accept': 'application/json'}
        headers['X-Auth-Token']=  token

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return(response.json())
        else:
            raise Exception("Error when getting info of table " + str(tableName) + " in dataset " + str(datasetName) + ".\nHttp Response from SkyQuery API returned status code " + str(response.status_code) + ":\n" + response.content.decode());
    else:
        raise Exception("User token is not defined. First log into SciServer.")


def listTableColumns(tableName, datasetName="MyDB"):
    """
    Returns a list of all columns in a table belonging to a particular dataset (more info in http://www.voservices.net/skyquery).

    :param tableName: name of table (string) within dataset.
    :param datasetName: name of dataset (string).
    :return: returns a list containing the columns and associated descriptions.
    :raises: Throws an exception if the user is not logged into SciServer (use Authentication.login for that purpose). Throws an exception if the HTTP request to the SkyQuery API returns an error.
    :example: columns = SkyQuery.listTableColumns("myTable", datasetName="MyDB")

    .. seealso:: SkyQuery.listQueues, SkyQuery.listAllDatasets, SkyQuery.getDatasetInfo, SkyQuery.listDatasetTables, SkyQuery.getTableInfo, SkyQuery.getTable, SkyQuery.dropTable
    """
    token = Authentication.getToken()
    if token is not None and token != "":
        url = Config.SkyQueryUrl + '/Schema.svc/datasets/' + datasetName +'/tables/' + tableName + '/columns'

        headers = {'Content-Type': 'application/json','Accept': 'application/json'}
        headers['X-Auth-Token']=  token

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            r = response.json()
            return(r['columns'])
        else:
            raise Exception("Error when listing columns of table " + str(tableName) + " in dataset " + str(datasetName) + ".\nHttp Response from SkyQuery API returned status code " + str(response.status_code) + ":\n" + response.content.decode());
    else:
        raise Exception("User token is not defined. First log into SciServer.")


######################################################################################################################
# Data:

def getTable(tableName, datasetName="MyDB", top = None):
    """
    Returns a dataset table as a pandas DataFrame (more info in http://www.voservices.net/skyquery).

    :param tableName: name of table (string) within dataset.
    :param datasetName: name of dataset or database context (string).
    :param top: number of top rows retrieved (integer).
    :return: returns the table as a Pandas dataframe.
    :raises: Throws an exception if the user is not logged into SciServer (use Authentication.login for that purpose). Throws an exception if the HTTP request to the SkyQuery API returns an error.
    :example: table = SkyQuery.getTable("myTable", datasetName="MyDB", top=10)

    .. seealso:: SkyQuery.listQueues, SkyQuery.listAllDatasets, SkyQuery.getDatasetInfo, SkyQuery.listDatasetTables, SkyQuery.getTableInfo, SkyQuery.dropTable, SkyQuery.submitJob
    """
    token = Authentication.getToken()
    if token is not None and token != "":

        url = Config.SkyQueryUrl + '/Data.svc/' + datasetName +'/' + tableName
        if top != None and top != "":
            url = url + '?top=' + str(top)

        headers = {'Content-Type': 'application/json','Accept': 'application/json'}
        headers['X-Auth-Token']=  token

        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            return(pandas.read_csv(StringIO(response.content.decode()), sep="\t"))
        else:
            raise Exception("Error when getting table " + str(tableName) + " from dataset " + str(datasetName) + ".\nHttp Response from SkyQuery API returned status code " + str(response.status_code) + ":\n" + response.content.decode());
    else:
        raise Exception("User token is not defined. First log into SciServer.")


def dropTable(tableName, datasetName="MyDB"):
    """
    Drops (deletes) a table from the user database (more info in http://www.voservices.net/skyquery).

    :param tableName: name of table (string) within dataset.
    :param datasetName: name of dataset or database context (string).
    :return: returns True if the table was deleted successfully.
    :raises: Throws an exception if the user is not logged into SciServer (use Authentication.login for that purpose). Throws an exception if the HTTP request to the SkyQuery API returns an error.
    :example: result = SkyQuery.dropTable("myTable", datasetName="MyDB")

    .. seealso:: SkyQuery.listQueues, SkyQuery.listAllDatasets, SkyQuery.getDatasetInfo, SkyQuery.listDatasetTables, SkyQuery.getTableInfo, SkyQuery.getTable, SkyQuery.submitJob
    """
    token = Authentication.getToken()
    if token is not None and token != "":
        url = Config.SkyQueryUrl + '/Data.svc/' + datasetName +'/' + tableName

        headers = {'Content-Type': 'application/json','Accept': 'application/json'}
        headers['X-Auth-Token']=  token

        response = requests.delete(url, headers=headers)

        if response.status_code == 200:
            return (True)
        else:
            raise Exception("Error when dropping table " + str(tableName) + " from dataset " + str(datasetName) + ".\nHttp Response from SkyQuery API returned status code " + str(response.status_code) + ":\n" + response.content.decode());
    else:
        raise Exception("User token is not defined. First log into SciServer.")


def uploadTable(uploadData, tableName, datasetName="MyDB", format="csv"):
    """
    Uploads a data table into a database (more info in http://www.voservices.net/skyquery).

    :param uploadData: data table, for now accepted in CSV string format.
    :param tableName: name of table (string) within dataset.
    :param datasetName: name of dataset or database context (string).
    :param format: format of the 'data' parameter. Set to 'csv' for now.
    :return: returns True if the table was uploaded successfully.
    :raises: Throws an exception if the user is not logged into SciServer (use Authentication.login for that purpose). Throws an exception if the HTTP request to the SkyQuery API returns an error.
    :example: result = SkyQuery.uploadTable("Column1,Column2\n4.5,5.5\n", tableName="myTable", datasetName="MyDB", format="csv")

    .. seealso:: SkyQuery.listQueues, SkyQuery.listAllDatasets, SkyQuery.getDatasetInfo, SkyQuery.listDatasetTables, SkyQuery.getTableInfo, SkyQuery.getTable, SkyQuery.submitJob
    """
    token = Authentication.getToken()
    if token is not None and token != "":
        url = Config.SkyQueryUrl + '/Data.svc/' + datasetName +'/' + tableName
        ctype = ""
        if format == "csv":
            ctype = 'text/csv'
        else:
            ctype = 'text/csv'

        headers = {'Content-Type': ctype ,'Accept': 'application/json'}
        headers['X-Auth-Token']=  token

        response = requests.put(url, data=uploadData, headers=headers)

        if response.status_code == 200:
            return (True)
        else:
            raise Exception("Error when uploading data to table " + str(tableName) + " in dataset " + str(datasetName) + ".\nHttp Response from SkyQuery API returned status code " + str(response.status_code) + ":\n" + response.content.decode());
    else:
        raise Exception("User token is not defined. First log into SciServer.")


