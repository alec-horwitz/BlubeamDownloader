from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time     # for printing time stamps
import os       # for checking and manipulating file paths
import sys      # for forcefully exiting this program
import codecs   # for opening unicode files
import shutil   # for moving files to different directories
import datetime

settingsFile = "Data/BluebeamDownloaderSettings.txt"

USERNAME_LINE_NAME = "USERNAME"
PASSWORD_LINE_NAME = "PASSWORD"
LOGIN_URL_LINE_NAME = "LOGIN_URL"
PROJECTS_URL_LINE_NAME = "PROJECTS_URL"
SESSIONS_URL_LINE_NAME = "SESSIONS_URL"
USERS_URL_LINE_NAME = "USERS_URL"
PROJECT_FILE_NAME_LINE_NAME = "PROJECT_FILE_NAME"
SESSION_FILE_NAME_LINE_NAME = "SESSION_FILE_NAME"
USER_FILE_NAME_LINE_NAME = "USER_FILE_NAME"
DRIVER_PATH_LINE_NAME = "DRIVER_PATH"
DESTINATION_FOLDER_LINE_NAME = "DESTINATION_FOLDER"
ARCHIVE_FOLDER_LINE_NAME = "ARCHIVE_FOLDER"
SLEEPTIME_LINE_NAME = "SLEEPTIME"
DAYS_LINE_NAME = "DAYS"

projSel = False
sessSel = False
userSel = True

def main():
  print("################# COMMENCING ##################\n")
  projSuc = False
  sessSuc = False
  userSuc = False
  downFoldPath = get_download_folder().replace("\\", "/")

  print("\n############# Reading in Settings #############")
  settingLines = readInSettingsFile()
  # settingLines, settingFormat = getSettingsDat()
  USERNAME, PASSWORD, LOGIN_URL = getLoginDat(settingLines)
  PROJECTS_URL, SESSIONS_URL, USERS_URL = getActivityURLs(settingLines)
  PROJECT_FILE_NAME, SESSION_FILE_NAME, USER_FILE_NAME = getFileNames(settingLines)
  DRIVER_PATH, DESTINATION_FOLDER, ARCHIVE_FOLDER = getPaths(settingLines)
  SLEEPTIME = int(readInSetting(settingLines,SLEEPTIME_LINE_NAME))
  DAYS = readInSetting(settingLines,DAYS_LINE_NAME)
  print("[Complete] Settings Read in")

  driver = driverOps(DRIVER_PATH, LOGIN_URL, USERNAME, PASSWORD)
  print("\n######### Requesting Activity Reports #########")
  while not (projSuc and sessSuc and userSuc): 
      projSuc = requestCSVDownload(driver, SLEEPTIME, DAYS, projSuc, downFoldPath, PROJECT_FILE_NAME, PROJECTS_URL, usersSelect=projSel)
      sessSuc = requestCSVDownload(driver, SLEEPTIME, DAYS, sessSuc, downFoldPath, SESSION_FILE_NAME, SESSIONS_URL, usersSelect=sessSel)
      userSuc = requestCSVDownload(driver, SLEEPTIME, DAYS, userSuc, downFoldPath, USER_FILE_NAME, USERS_URL, usersSelect=userSel)    
  driver.quit()

  print("\n##### Moving Files to " + DESTINATION_FOLDER + " #####\n")
  fileMover(PROJECT_FILE_NAME, DESTINATION_FOLDER, downFoldPath, ARCHIVE_FOLDER)
  fileMover(SESSION_FILE_NAME, DESTINATION_FOLDER, downFoldPath, ARCHIVE_FOLDER)
  fileMover(USER_FILE_NAME, DESTINATION_FOLDER, downFoldPath, ARCHIVE_FOLDER)
  print("[Complete] Files Moved\n")

  time.sleep( 3 )
  print("\n######### All Operations Complete!!! ##########")
  time.sleep( 3 )

def getSettingsDat():
  settingLines = readInSettingsFile()
  settingFormat = readInSetting(settingLines[1],"FORMAT:").split(",")
  return settingLines, settingFormat

def getLoginDat(settingLines):
  USERNAME = readInSetting(settingLines, USERNAME_LINE_NAME)
  PASSWORD = readInSetting(settingLines, PASSWORD_LINE_NAME)
  LOGIN_URL = readInSetting(settingLines, LOGIN_URL_LINE_NAME)
  return USERNAME, PASSWORD, LOGIN_URL

def getActivityURLs(settingLines):
  PROJECTS_URL = readInSetting(settingLines,PROJECTS_URL_LINE_NAME)
  SESSIONS_URL = readInSetting(settingLines,SESSIONS_URL_LINE_NAME)
  USERS_URL = readInSetting(settingLines,USERS_URL_LINE_NAME)
  return PROJECTS_URL, SESSIONS_URL, USERS_URL

def getFileNames(settingLines):
  PROJECT_FILE_NAME = readInSetting(settingLines,PROJECT_FILE_NAME_LINE_NAME).encode('utf-8')
  SESSION_FILE_NAME = readInSetting(settingLines,SESSION_FILE_NAME_LINE_NAME).encode('utf-8')
  USER_FILE_NAME = readInSetting(settingLines,USER_FILE_NAME_LINE_NAME).encode('utf-8')
  return PROJECT_FILE_NAME, SESSION_FILE_NAME, USER_FILE_NAME

def getPaths(settingLines):
  DRIVER_PATH = str(readInSetting(settingLines,DRIVER_PATH_LINE_NAME).replace("\\", "/").replace("//", "/")).encode('utf-8')
  if (DRIVER_PATH == ""): DRIVER_PATH = DRIVER_PATH + "chromedriver.exe"
  else:
    if (DRIVER_PATH[-4:] !=".exe"):
      if ("chromedriver" == DRIVER_PATH[-len("chromedriver"):]): 
        DRIVER_PATH = DRIVER_PATH + ".exe"
      elif (DRIVER_PATH[-1] =="/"): 
        DRIVER_PATH = DRIVER_PATH + "chromedriver.exe"
      else: DRIVER_PATH = DRIVER_PATH + "/chromedriver.exe"

  DESTINATION_FOLDER = str(readInSetting(settingLines,DESTINATION_FOLDER_LINE_NAME).replace("\\", "/").replace("//", "/"))
  if (DESTINATION_FOLDER != ""):
    if (DESTINATION_FOLDER[-1] != "/"): DESTINATION_FOLDER = DESTINATION_FOLDER + "/"

  ARCHIVE_FOLDER = str(readInSetting(settingLines,ARCHIVE_FOLDER_LINE_NAME).replace("\\", "/").replace("//", "/"))
  if (ARCHIVE_FOLDER != ""):
    if (ARCHIVE_FOLDER[-1] != "/"): ARCHIVE_FOLDER = ARCHIVE_FOLDER + "/"
  return DRIVER_PATH, DESTINATION_FOLDER, ARCHIVE_FOLDER

def driverOps(DRIVER_PATH, LOGIN_URL, USERNAME, PASSWORD):
  print("\n############### Sarting Browser ###############")
  if not os.path.exists(DRIVER_PATH): 
    print("ERROR: "+DRIVER_PATH+" NOT FOUND!")
    junk = input("\nEnter any key to EXIT program...")
    sys.exit()
  os.environ["webdriver.chrome.driver"] = DRIVER_PATH
  driver = webdriver.Chrome(DRIVER_PATH)
  print("[Complete] Browser Started")

  print("\n################# Logging in ##################")
  driver.get(LOGIN_URL)
  time.sleep( 3 )
  driver.find_element_by_id("login1_txtEmail").send_keys(USERNAME)
  driver.find_element_by_id("login1_txtPassword").send_keys(PASSWORD)
  driver.find_element_by_id("login1_btnLogin").click()
  time.sleep( 3 )
  print("[Complete] Logged in")
  return driver

def fileMover(fileName, DESTINATION_FOLDER, downFoldPath, ARCHIVE_FOLDER):
  if len(fileName) > 1:
    if os.path.exists(os.path.join(DESTINATION_FOLDER, fileName)):
      print("Archiving old " + fileName + " file")
      checkDumpForDoubles(os.path.join(DESTINATION_FOLDER, fileName),downFoldPath,ARCHIVE_FOLDER, fileName,fileName[fileName.find("."):])
    print("Moving New " + fileName + " file to " + DESTINATION_FOLDER + "\n")
    shutil.move(os.path.join(downFoldPath, fileName), os.path.join(DESTINATION_FOLDER, fileName))

'''****************************checkDumpForDoubles()****************************
PURPOSE: Renames the given file with the given name and puts a timestamp at the 
         end of it and then checks if the new filename already exsists in the 
         dump folder. If it does a number gets added at the end to make it 
         unquie and then gets put in the dump folder. If it does not it is 
         simply moved to the dump folder.

INPUT: 'inputFileName' a string containg a filepath, 'inputFilePath' a string 
       containing the path to the folder that that file is in, 'dumpPath' a 
       string containg the path to the dump folder, 'sourceDir' a string the 
       containing the name to be given to the file, 'exstension' a string 
       containing the extension of the file.
 
OUTPUT: None
  
NOTES: If 'sourceDir' is equal 'exstension' the file will not be renamed; only 
       moved.
*****************************************************************************'''
def checkDumpForDoubles(inputFileName,inputFilePath,dumpPath, sourceDir,exstension):
  exLen=len(exstension)
  currentFileName = inputFileName[len(inputFilePath):]
  if ((os.path.join(inputFilePath,currentFileName) != os.path.join(dumpPath,currentFileName)) or (sourceDir == exstension)):
    if sourceDir != exstension:
      currentFileName = time.strftime(sourceDir[:-exLen]+"-%y%m%d-%H%M%S"+exstension)
      os.rename(inputFileName,os.path.join(inputFilePath,currentFileName))
      inputFileName = os.path.join(inputFilePath,currentFileName)
  if (os.path.exists(os.path.join(dumpPath,currentFileName))):
    updatedFileName = findFileNameDouble(dumpPath,currentFileName,0,exLen)
    os.rename(inputFileName,os.path.join(inputFilePath,updatedFileName))
    inputFileName = os.path.join(inputFilePath,updatedFileName) 
  shutil.move(inputFileName, os.path.join(dumpPath,currentFileName))    

'''****************************findFileNameDouble()*****************************
PURPOSE: Find how many other doubles there are of the given file name and add 
         the number plus one to the end of the filename to name the new double 
         with.

INPUT: 'dumpPath' a string containg the path to the dump folder, 'FileName' 
       string containg a filename, 'count' an int containg the number of times 
       this function has been run on the current parameters(should be given 0 to 
       start or 1 if the filename string is already a result of this function), 
       'exLen' an int containing the length of the extension of the file.
 
OUTPUT: 'FileName' a string containing a filename that does not yet exsist in 
  the dump folder.
  
NOTES: None
*****************************************************************************'''
def findFileNameDouble(dumpPath,FileName,count,exLen):
  if os.path.exists(os.path.join(dumpPath,FileName)):
    if(count>0):
      FileName=FileName[:-(len(str(count+1))+7)]+FileName[-exLen:]
      count=count+1
  FileName = findFileNameDouble(dumpPath,FileName[:-exLen]+" ("+str(count+1)+")"+FileName[-exLen:],count,exLen)
    
  return FileName

'''*****************************readInSettingsFile()****************************
PURPOSE: To read in the settings.txt

INPUT: None

OUTPUT: 'settingLines' the list of lines from the settings.txt in the form of 
        an arry of strings.

NOTES: If unable to find settings.txt an error message will be printed saying 
       so. The same goes for if the file is empty.
*****************************************************************************'''
def readInSettingsFile():
  if not os.path.exists(settingsFile):
    print ("ERROR: Cannot find the "+settingsFile+" file.")
    print ("This program cannot run properly without it.")
    # make the program stop so user acknowledges the failure to open
    junk = input("\nEnter any key to EXIT program...")
    sys.exit()     
  INPUT = codecs.open(settingsFile, encoding='utf-8')
  settingLines = INPUT.readlines()
  INPUT.close()
  fileEmpty(settingLines,settingsFile)
    
  return settingLines

def readInSetting(settingLines, string):
  NotFound = True
  for line in settingLines:
    if (line.find(":") != -1):
      lineName = readInLineName(line)
      if lineName == string:
        Line = line
        NotFound = False
  if NotFound: lineMissingError(string)
  setting = readInPromptEntries(Line)
  print("Retrieved " + string + " setting")
  return setting

def readInLineName(nextLine):
  nextLine = nextLine.strip()
  entryStart = nextLine.find(":")
  nextEntry = nextLine[:(entryStart)]
  return nextEntry

  '''****************************readInPromptEntries()****************************
PURPOSE: To read in a single entry from a string after a ":". 

INPUT: 'nextLine' a string

OUTPUT: 'nextEntry' a string
  
NOTES: If there is a space after the ":" it will keep checking the next 
       character untill it finds one that isn't white space or untill it reaches 
       the end of the string. If unable to find a ":" will just return the 
       original string.
*****************************************************************************'''
def readInPromptEntries(nextLine):
  nextLine = nextLine.strip()
  if (nextLine.find(": ") != -1):
    offset = recursiveSpaces(nextLine,nextLine.find(":")+1,1)
  else:
    offset = 0
  entryStart = nextLine.find(":")
  nextEntry = nextLine[(entryStart+1+offset):]
  return nextEntry

'''*********************************recursivePath()*****************************
PURPOSE: To find the first leftmost '/' from a perticular position in a string.

INPUT: 'line' a string and 'pos' a int containg the index of the string to start
       at. 
 
OUTPUT: 'pos' an int containing the index of the first leftmost '/' from the 
  given position.
  
NOTES: If no '/' is found -1 will be returned. 
*****************************************************************************'''
def recursivePath(line,pos):
  if "/" in line:
    if  not ("/" in line[pos-1]):
      pos = recursivePath(line,pos-1)
  else: pos = -1
  return pos

'''******************************recursiveSpaces()******************************
PURPOSE: To find out how many spaces there are in a row after the given position
         in a string. 

INPUT: 'line' a string, 'pos' an int conaining a numeric position in that 
       string, and 'howMany' an int containing number of spaces to start form in 
       the count.

OUTPUT: 'howMany' an int containing the number of spaces found plus the starting 
  number of spaces 
  
NOTES: None
*****************************************************************************'''
def recursiveSpaces(line,pos,howMany):
  if line[pos+1]==' ':
    howMany = recursiveSpaces(line,pos+1,howMany+1)
  return howMany

def requestCSVDownload(driver, SLEEPTIME, DAYS, downSuc, downFoldPath, fileName, filterURL, usersSelect=False):
  if len(fileName) > 1:
    if len(fileName[fileName.find("."):]) < 2: extensionNotFound(fileName)
    if not os.path.exists(downFoldPath + "/" + fileName):
      print("\nRequesting: "+fileName)
      download_csv_from_url(driver,  DAYS, filterURL, users_select=usersSelect)
      time.sleep( SLEEPTIME )
      if not os.path.exists(downFoldPath + "/" + fileName): 
        print("[FAILED] REQUEST FOR: "+fileName)
      else: 
        print("[SATISFIED] REQUEST FOR: "+fileName)
        downSuc = True
    else: 
      print("[ALREADY SATISFIED] REQUEST FOR: "+fileName)
      downSuc = True
  else:
    downSuc = True

  return downSuc

def download_csv_from_url(driver,  DAYS, url,users_select=False):
  if ("-" in DAYS) and ("/" in DAYS):
    DAYS = DAYS.split("-")
    endDate = DAYS[1]
    startDate = DAYS[0]
  elif "/" in DAYS:
    endDate = str(datetime.datetime.strptime(str(datetime.date.today()), "%Y-%m-%d").strftime("%m/%d/%Y"))
    startDate = DAYS
  else: 
    endDate = str(datetime.datetime.strptime(str(datetime.date.today()), "%Y-%m-%d").strftime("%m/%d/%Y"))
    startDate = str(datetime.datetime.strptime(str(datetime.date.today() - datetime.timedelta(days=(int(DAYS)-1))), "%Y-%m-%d").strftime("%m/%d/%Y"))
  driver.get(url)
  time.sleep( 3 )

  if users_select:
    driver.find_element(by=By.CSS_SELECTOR,value="input#userInput").click()
    time.sleep( 2 )
    driver.find_element(by=By.CSS_SELECTOR,value="div[data-reactid='.0.2.1.0.0.1.0.0.0.0.$userDD.0']").click()
    time.sleep( 2 )
    for user in driver.find_elements_by_class_name("item--jss-0-625"):
      user.click()

  caret = driver.find_element(by=By.CSS_SELECTOR,value="div[data-reactid='.0.2.1.0.0.1.0.0.0.2.1.0.3']")
  caret.click()
  time.sleep( 3 )
  end = driver.find_element_by_name("daterangepicker_end")
  for x in xrange(1,11): end.send_keys(Keys.BACKSPACE)
  end.send_keys(endDate)
  start = driver.find_element_by_name("daterangepicker_start")
  for x in xrange(1,11): start.send_keys(Keys.BACKSPACE)
  start.send_keys(startDate)
  time.sleep( 3 )
  apply_btn =driver.find_element(by=By.CSS_SELECTOR,value="button.applyBtn")
  apply_btn.click()
  time.sleep( 3 )
  dropdown = driver.find_element(by=By.CSS_SELECTOR,value="div[data-reactid='.0.2.1.0.0.1.0.0.0.3.0.1']")
  dropdown.click()
  download = driver.find_element(by=By.CSS_SELECTOR,value="div[data-reactid='.0.2.1.0.0.1.0.0.0.3.0.1.1.0']")
  download.click()

if os.name == 'nt':
    import ctypes
    from ctypes import windll, wintypes
    from uuid import UUID

    # ctypes GUID copied from MSDN sample code
    class GUID(ctypes.Structure):
        _fields_ = [
            ("Data1", wintypes.DWORD),
            ("Data2", wintypes.WORD),
            ("Data3", wintypes.WORD),
            ("Data4", wintypes.BYTE * 8)
        ] 

        def __init__(self, uuidstr):
            uuid = UUID(uuidstr)
            ctypes.Structure.__init__(self)
            self.Data1, self.Data2, self.Data3, \
                self.Data4[0], self.Data4[1], rest = uuid.fields
            for i in range(2, 8):
                self.Data4[i] = rest>>(8-i-1)*8 & 0xff

    SHGetKnownFolderPath = windll.shell32.SHGetKnownFolderPath
    SHGetKnownFolderPath.argtypes = [
        ctypes.POINTER(GUID), wintypes.DWORD,
        wintypes.HANDLE, ctypes.POINTER(ctypes.c_wchar_p)
    ]

    def _get_known_folder_path(uuidstr):
        pathptr = ctypes.c_wchar_p()
        guid = GUID(uuidstr)
        if SHGetKnownFolderPath(ctypes.byref(guid), 0, 0, ctypes.byref(pathptr)):
            raise ctypes.WinError()
        return pathptr.value

    FOLDERID_Download = '{374DE290-123F-4565-9164-39C4925E467B}'

    def get_download_folder():
        return _get_known_folder_path(FOLDERID_Download)
else:
    def get_download_folder():
        home = os.path.expanduser("~")
        return os.path.join(home, "Downloads")

def pathError(path, identifier):
    print ("ERROR: Cannot find the following "+identifier+ " " + path)
    print ("This program cannot run properly without it.")
    print ("Please check that the file path is entered correctly in the "+settingsFile+" file.")
    print ("Consult the ReadMe.txt if you are not sure of how to properly modify the file.")
    # make the program stop so user acknowledges the failure to open
    junk = input("\nEnter any key to EXIT program...")
    sys.exit()

def fileEmpty(lines, path):
  if not (len(lines)>0):
    print ("ERROR: "+path+" is empty!!!")
    print ("This program cannot run properly without it.")
    print ("Please check that required information is properly entered in this file.")
    print ("Consult the ReadMe.txt if you are not sure of how to properly modify the file.")
    # make the program stop so user acknowledges the failure to open
    junk = input("\nEnter any key to EXIT program...")
    sys.exit()
  
def lineMissingError(string):
    print ("ERROR: The line "+string+": is missing or not where it's supposed to be in "+settingsFile+"!!!")
    print ("This program cannot run properly without it.")
    print ("Please check that required information is properly entered in this file.")
    print ("Consult the ReadMe.txt if you are not sure of how to properly modify the file.")
    # make the program stop so user acknowledges the failure to open
    junk = input("\nEnter any key to EXIT program...")
    sys.exit()

def ColNotFound(string):
    print ("ERROR: Could not find the "+string+" column in one of the input files!!!")
    print ("This program cannot run properly without it.")
    print ("To fix this manually enter the appropriate column number in the "+settingsFile+" file.")
    print ("Consult the ReadMe.txt if you are not sure of how to properly modify the file.")
    # make the program stop so user acknowledges the failure to open
    junk = input("\nEnter any key to EXIT program...")
    sys.exit()

def extensionNotFound(string):
    print ("ERROR: The filename "+string+" does not seem to have a proper exstenstion!!!")
    print ("This program cannot run properly without it.")
    print ("To fix this manually enter the appropriate extenstion in the "+settingsFile+" file.")
    print ("Consult the ReadMe.txt if you are not sure of how to properly modify the file.")
    # make the program stop so user acknowledges the failure to open
    junk = input("\nEnter any key to EXIT program...")
    sys.exit()

if __name__ == '__main__':
  main()
