
#  Author:  Daniel Morvay
#  Creator Email:  morvayd@gmail.com
#  Description:  Find where installed packages are located on the hard drive.  
#  Edit strPackList and enter package names you would like to search for.  

#
#  ---------- Install ----------
#

#  ----- Base Libraries -----
import copy
import datetime
import getpass
import itertools
import os
import platform
import site
import sys
import sysconfig

#  ----- Additional Libraries -----
import pandas

#  ----- Custom Libraries -----
import PythonLog

#
#  ---------- Setup ----------
#
strPythonScript = "PythonPackageLocations.py"
strModified = "2024.11.22"

#  Python Version
strPyVer = platform.python_version()
#  OS - Windows or Linux or Mac
strOS = platform.system()
#  OS Version 
strOSVer = platform.platform()
#  PC Name
strPC = platform.node()
#  UserID
strUser = getpass.getuser()

#  Today's Date
strStartTime = datetime.datetime.today()
strDateNow = strStartTime.strftime("%Y.%m.%d")

#  Search for libraries of interest on the hard drive.
strPackList = ["copy", "datetime", "getpass", "itertools", "os", "platform", "site", "sys", "pandas"]

#
#  ---------- Python Log Start ----------
#
#  Note:  strLogPath, strLogOut are created & returned at the start of Logging
strReturn = PythonLog.PyLogStart(strPythonScript, strModified, strPyVer, strOS, strOSVer, strPC, strUser, strStartTime, strDateNow)

#  Load the Path and Filename from the function return
strLogPath = strReturn[0]
strLogOut = strReturn[1]

#
#  ---------- Determine Base Libraries ----------
#
#  List base Libraries
strBaseLib = sys.builtin_module_names
strStdLib = sys.stdlib_module_names
strStdLocation = sysconfig.get_path('stdlib')

strUserLocation = site.getusersitepackages()

#
#  ---------- Python Log Update ----------
#
strUpdate = "\n"+str(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))+" Scanning library folders ..."
PythonLog.PyLogUpdate(strUpdate, strLogOut)

#
#  ---------- Create Libraries List ----------
#

#  Library Folders Loaded
strFolders = ""
strFolders = copy.copy(sys.path)

#  ----- Clean Up -----

#  Remove non-folders
for i in range(len(strFolders)-1, -1, -1):
    if (not os.path.isdir(strFolders[i])):
        #  Found match - add to rows list
        strResult = strFolders.pop(i)

#  Remove lib-dynload - no libraries here
for i in range(len(strFolders)-1, -1, -1):
    if ('lib-dynload' in strFolders[i]):
        #  Found match - add to rows list
        strResult = strFolders.pop(i)

#
#  ---------- Determine Libraries Installed ----------
#

dfFolder = pandas.DataFrame({"Path":[], "Folder":[]})
dfFile = pandas.DataFrame({"Path":[], "File":[]})

for i in range(0, len(strFolders)):
    lstTemp = list(os.scandir(path=strFolders[i]))
    
    #  List only folders
    for strTemp in lstTemp:
        #  strTemp is a posix dictionary - convert to string & clean up
        if (os.path.isdir(strFolders[i]+"/"+strTemp.name)):
            #  print ("Folder: "+str(strTemp))
            if (len(dfFolder)==0):
                dfFolder = pandas.DataFrame({"Path":[strFolders[i]], "Folder":[strTemp.name]})
            else:
                dfTemp = pandas.DataFrame({"Path":[strFolders[i]], "Folder":[strTemp.name]})
                dfFolder = pandas.concat([dfFolder, dfTemp])

    #  List only Files
    for strTemp in lstTemp:
        if (os.path.isfile(strFolders[i]+"/"+strTemp.name)):
            #  print ("File: "+str(strTemp))
            if (len(dfFile)==0):
                dfFile = pandas.DataFrame({"Path":[strFolders[i]], "File":[strTemp.name]})
            else:
                dfTemp = pandas.DataFrame({"Path":[strFolders[i]], "File":[strTemp.name]})
                dfFile = pandas.concat([dfFile, dfTemp])

#
#  ---------- Scan Libraries ----------
#

#
#  ---------- Python Log Update ----------
#
strUpdate = "\n"+str(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))+" Searching for installed libraries of interest ..."
PythonLog.PyLogUpdate(strUpdate, strLogOut)

strTempPath = []
strTempLib = []
strSearchLib = []
dfSubSet = pandas.DataFrame({"Path":[], "Folder":[]})

#  Search for Libraries
for i in range(0, len(strPackList)):
    strCheck = []
    strCheck = list(dfFolder["Folder"].str.contains(strPackList[i]))
    strRows = []
    strRows = list(itertools.compress(range(len(strCheck)), strCheck))
    if (len(strRows)!=0):
        for j in range(0, len(strRows)):
            #  strTempPath.append(dfFolder["Path"].iloc[strRows[j]])
            #  strTempLib.append(dfFolder["Folder"].iloc[strRows[j]])
            #  strSearchLib.append(strPackList[i])
            if (len(dfSubSet)==0): 
                dfSubSet = pandas.DataFrame({"Hard Drive Path":[dfFolder["Path"].iloc[strRows[j]]], "Matched Folder":[dfFolder["Folder"].iloc[strRows[j]]], "Requested Library":strPackList[i]})
            else:
                dfTemp = pandas.DataFrame({"Hard Drive Path":[dfFolder["Path"].iloc[strRows[j]]], "Matched Folder":[dfFolder["Folder"].iloc[strRows[j]]], "Requested Library":strPackList[i]})
                dfSubSet = pandas.concat([dfSubSet, dfTemp])           

if (len(dfSubSet)!=0):
    #
    #  ---------- Python Log Update ----------
    #
    strUpdate = "\n"+str(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))+" Saving found libraries of interest to .csv ..."
    PythonLog.PyLogUpdate(strUpdate, strLogOut)

    #
    #  ---------- Save as .csv ----------
    #

    #  Save to disk
    if (strOS=="Windows"):
        dfSubSet.to_csv("C:\\Users\\"+strUser+"\\Documents\\LibraryLocations.csv", index=False)
        #
        #  ---------- Python Log Update ----------
        #
        strUpdate = "\nSuccess - LibraryLocations.csv written to C:\\Users\\"+strUser+"\\Documents\\"
        PythonLog.PyLogUpdate(strUpdate, strLogOut)

    if (strOS=="Linux"):
        dfSubSet.to_csv("/home/"+strUser+"/Documents/LibraryLocations.csv", index=False)
        #
        #  ---------- Python Log Update ----------
        #
        strUpdate = "\nSuccess - LibraryLocations.csv written to /home/"+strUser+"/Documents/"
        PythonLog.PyLogUpdate(strUpdate, strLogOut)

    if (strOS=="Darwin"):
        dfSubSet.to_csv("/Users/"+strUser+"/Documents/LibraryLocations.csv", index=False)
        #
        #  ---------- Python Log Update ----------
        #
        strUpdate = "\nSuccess - LibraryLocations.csv written to /Users/"+strUser+"/Documents/"
        PythonLog.PyLogUpdate(strUpdate, strLogOut)

else:
        #
    #  ---------- Python Log Update ----------
    #
    strUpdate = "\n"+str(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))+"No libraries of interest found on the hard drive ..."
    PythonLog.PyLogUpdate(strUpdate, strLogOut)

#
#  ---------- Python Log End ----------
#
strEndTime = datetime.datetime.today()
strTimeDelta = strEndTime-strStartTime
strTimeDelta = str(strTimeDelta.total_seconds())

strUpdate="\n-----------------------------------------------------------"
strUpdate=strUpdate+"\nPython Script End:          "+str(strEndTime)
strUpdate=strUpdate+"\n-----------------------------------------------------------"
strUpdate=strUpdate+"\nCompleted Python Script Elapsed Time: "+str(strTimeDelta)
strUpdate=strUpdate+"\n***********************************************************\n"

PythonLog.PyLogEnd(strUpdate, strLogOut)
