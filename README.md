# BlubeamDownloader
CONTENTS OF THIS FILE
---------------------
*BluebeamDownloader.exe
*BluebeamDownloader.py
*Data/BluebeamDownloaderSettings.txt
*Data/BluebeamDownloaderReadMe.txt
*Downloads/Archive/




 TABLE OF CONTENTS
---------------------
*Introduction
*Configuration
*Support




    INTRODUCTION
---------------------
This program is made to download Activity reports off the Bluebeam 
Studio website. There are three different report files that can be
downloaded off this site and they are as follows:

-"ProjectActivity.csv" which contains the project activity report for
 all projects available to the account described in the
 BluebeamDownloaderReadMe.txt file.

-"SessionActivity.csv" which contains the session activity report for
 all sessions available to the account described in the 
 BluebeamDownloaderReadMe.txt file.

-"User Activity Report.csv" which contains the user activity report for
 all users collaborating with the account described in the
 BluebeamDownloaderReadMe.txt file.

After this program attempts to download these files to the computer's 
Downloads it then moves these files to a destination folder described in 
the BluebeamDownloaderReadMe.txt file. Any old report files already in the 
destination folder will be moved to the archive folder described in the 
BluebeamDownloaderReadMe.txt file and stamped with the date and time.

For this program to work properly you must follow the instructions 
provided in the CONFIGURATION section very carefully.




    CONFIGURATION
---------------------
This section of the ReadMe is a detailed description of how this 
program functions. It explains how to give the program an input 
that it expects and why. This section should be able to explain any 
problems you might run into. Since the only input this program needs 
is the BluebeamDownloaderSettings.txt that is what will be covered here.


############# About the settings.txt #############
The settings.txt file must be in the same directory as this program. 
This program is very particular about how this file is set up. Do not
change the name of this file and do not add lines that aren't required. 
If you do, it might give you an error message (or worse, crash without 
any error message). It must have 27 lines (including the 6 blank lines) 
in the given order that read as follows:

[Login Information]
USERNAME: email@website.com
PASSWORD: password

[URLs]
LOGIN_URL: https://studio.bluebeam.com/
PROJECTS_URL: https://prime.bluebeam.com/primeportal/insight?tab=projectsFilter
SESSIONS_URL: https://prime.bluebeam.com/primeportal/insight?tab=sessionsFilter
USERS_URL: https://prime.bluebeam.com/primeportal/insight?tab=usersFilter

[Filenames]
PROJECT_FILE_NAME: ProjectActivity.csv
SESSION_FILE_NAME: SessionActivity.csv
USER_FILE_NAME: User Activity Report.csv

[File System Input/Output]
DRIVER_PATH: data/aDriver.exe
DESTINATION_FOLDER: Downloads/
ARCHIVE_FOLDER: Downloads/Archive/

[Wait Time for Each File]
SLEEPTIME: 10

[Number of days or How far back or date range]
DAYS: 30

For each line with a ":" in it anything after the ":" can be altered to your 
liking so long as you edit it correctly. NEVER CHANGE WHAT IS BEFORE THE ":",
OTHERWISE DOING SO Will BREAK THE PROGRAM!!! Each line in the above example have 
are there as examples of the correct types of inputs to use for those lines. 
There are several different sets of rules you must follow to edit these lines 
correctly depending on what is just before the ":". These rules are as follows:


**************** [Login Information] *****************

 -If the line has "USERNAME:" then you must give it a user name to log in to the
  Bluebeam website with that corresponds with the password provided in the 
  "PASSWORD:" line.

 -If the line has "PASSWORD:" then you must give it a password to log in to the
  Bluebeam website with that corresponds with the user name provided in the 
  "USERNAME:" line.


*********************** [URLs] ***********************

 -If the line has "LOGIN_URL:" then you must give it a URL to the log in page
  of the Bluebeam studio website.

 -If the line has "PROJECTS_URL:" then you must give it a URL to the projects 
  filter on the insights page of the Bluebeam studio website.

 -If the line has "SESSIONS_URL:" then you must give it a URL to the Sessions
  filter on the insights page of the Bluebeam studio website.

 -If the line has "USERS_URL:" then you must give it a URL to the users filter 
  on the insights page of the Bluebeam studio website.


******************** [Filenames] *********************

 -If you leave the space after any line that ends with "_FILE_NAME:" the program will skip
  trying to download that file.

 -If the line has "PROJECT_FILE_NAME:" then you must give it the filename that 
  corresponds to the filename that is supposed to be downloaded from webpage provided 
  in the "PROJECTS_URL:" line. This program requires that you include the file extension
  as part of the filename you enter.

 -If the line has "SESSION_FILE_NAME:" then you must give it the filename that 
  corresponds to the filename that is supposed to be downloaded from webpage provided 
  in the "SESSIONS_URL:" line. This program requires that you include the file extension
  as part of the filename you enter.

 -If the line has "USER_FILE_NAME:" then you must give it the filename that 
  corresponds to the filename that is supposed to be downloaded from webpage provided 
  in the "USERS_URL:" line. This program requires that you include the file extension
  as part of the filename you enter.


************* [File System Input/Output] *************

 -First it is essential that you understand how to enter a file path. There are two
  kinds of file paths this program understands are relative and absolute. If you are 
  confident that understand how different kinds of file paths (relative and absolute) 
  work you may skip to the next "-" bullet. These two way of entering a file path
  are as follows:

   >You can enter a relative (to the directory the program is in) file path 
    such as "relative/file/path/". This tells the program to look for a file
    or folder with in a sub directory of the folder that the program lives in. 
    If you give it no path after "_FOLDER:" the program will use the exact same 
    directory as where the program lives. For example:

    *If you were to type "Downloads/" after the line "DESTINATION_FOLDER:" in 
     the form "DESTINATION_FOLDER: Downloads/" the program will look for a folder 
     called "Downloads" in the same directory that the program is stored in and 
     store the .csv files that the program downloads from Bluebeam in that folder. 

    *If you were to type nothing after the line "DESTINATION_FOLDER:" the program 
     will use the same folder that the program is stored in for that parameter.

   >You can enter an absolute file path such as "N:/whatever/path/you/want/".
    If you are an experienced Windows or Linux user, this should be the
    type of directory scheme you are used to seeing (In Windows they use 
    '\' instead of '/' but this program doesn't care which you use). For example
    if you typed "C:/Desktop/" after "DESTINATION_FOLDER:" in the form 
    "DESTINATION_FOLDER: C:/Desktop/" the program will use the Desktop folder on 
    the C drive for that parameter.

 -If the line has "DRIVER_PATH:" then you must give it a path to a file. 
  Specifically, this file must be the chrome drive needed to lunch chrome. In the
  example of the settings file format above the name of this file is 
  "aDriver.exe". If you leave out the name of the driver it will assume
  that the name of the file is "chromedriver.exe".

 -If the line has "DESTINATION_FOLDER:" then you must enter a path to a folder for 
  the program to send the .csv files after they are downloaded from the Bluebeam site. 
  If there are old copies of these .csv files they will be moved to the Archive folder 
  which is specified by the line that starts with "ARCHIVE_FOLDER:".

 -If the line has "ARCHIVE_FOLDER:" then you must enter a path to a folder for the 
  program to send any old copies of the .csv files from an older run of this program. 
  When these files are moved, a time stamp is appended to the names of these files. 
  The time stamp appended is the date and military time in the format 
  "NameOfActivityReport-YearMonthDay-HourMinuteSecound".


************* [Wait Time for Each File] **************
 -If the line has "SLEEPTIME:" then you must enter a number to indicate how many seconds
  the program should wait for each file to download from the Bluebeam website. 5 to 30
  seconds are recommended.


*** [Number of days or How far back or date range] ***
 -If the line has "DAYS:" then you have 3 options:

   >You can enter a number representing how many days back the activity reports
    should go. In other words, from today how many days should the data include.

   >You can enter a date representing how far back the activity reports should go. 
    In other words, from what date forward should the data include. The date should
    be in the format mm/dd/yyyy.

   >You can enter a date range representing from when to when reports should include 
    data for. The date range must be in the format mm/dd/yyyy-mm/dd/yyyy. The program
    will try to get the data from the first date to the date at the end.
    



      SUPPORT
---------------------
If you are having issues and this document has not helped, you may contact the creator 
of this program at horwitz_alec@wheatoncollege.edu.
