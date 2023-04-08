##############################################
#      Responder-Parser.py                   #
#      Author: Nikos Vourdas (@nickvourd)    #
#      License: MIT                          #
#      Required Dependencies: None           #
##############################################

import argparse
from platform import system
from os import walk, path, remove, rename
from sys import exit, argv

#Global variables
__author__ = "@nickvourd"
__team__ = "@villains_team"
__version__ = "1.0.0"
__license__ = "MIT"
__github__ = "https://github.com/villains-team/Responder-Parser"

__ascii__ = '''


  _____                                 _                  _____                         
 |  __ \                               | |                |  __ \                        
 | |__) |___  ___ _ __   ___  _ __   __| | ___ _ __ ______| |__) |_ _ _ __ ___  ___ _ __ 
 |  _  // _ \/ __| '_ \ / _ \| '_ \ / _` |/ _ \ '__|______|  ___/ _` | '__/ __|/ _ \ '__|
 | | \ \  __/\__ \ |_) | (_) | | | | (_| |  __/ |         | |  | (_| | |  \__ \  __/ |   
 |_|  \_\___||___/ .__/ \___/|_| |_|\__,_|\___|_|         |_|   \__,_|_|  |___/\___|_|   
                 | |                                                                     
                 |_|                                                                     

Responder-Parser v.{} - Responder's parsing tool.
Responder-Parser is an open source tool licensed under {}.
Written with <3 by {}...
Please visit {} for more...
'''.format(__version__, __license__, __team__, __github__)

#Arguments function
def Arguments(argv):
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter, prog="Responder-Parser", usage='%(prog)s [options]')

    parser.add_argument('-v', '--version', action='version', version='%(prog)s 1.0.0')
    parser.add_argument('-c', '--challenge', type=str, dest='NUMBER', required=False, help="set challenge to Repsonder")
    parser.add_argument('--cleardb', action='store_true', required=False, help="clear Responder.db data")
    parser.add_argument('--setdb', type=str, dest='DATABASENAME', required=False, help="set Database file to Responder conf")
    parser.add_argument('--sessionlog', type=str, dest='SESSIONLOG', required=False, help="set Session log file to Responder conf"),
    parser.add_argument('--poisonlog', type=str, dest='POISONERSLOG', required=False, help="set Poisoners log file to Responder conf")
    parser.add_argument('--analyzelog', type=str, dest='ANALYZELOG', required=False, help="set Analyze mode log file to Responder conf")
    parser.add_argument('--configdumplog', type=str, dest='CONFIGDUMPLOG', required=False, help="set Confing Dump log file to Responder conf")

    args = parser.parse_args()

    #check the number of arguments
    if len(argv) == 1:
        parser.print_help()
        exit(1)

    return args

#FindOS function
def FindOS(candidateOS):
    match candidateOS:
            case "windows":
                myOS = "windows"
            case "linux":
                myOS = "linux"
            case _:
                myOS = "not supported"
                print("[!] Not supported operating system...\n")
                exit(1)
    
    return myOS

#SearchPath function
def SearchPath(directory):
    foundPath = path.exists(directory)
    
    return foundPath

#SearchFile function
def SearchFile(myOS, file):
    foundFileFlag = False
    match myOS:
        case "linux":
            #Using default directory
            defaultDir = "/usr/share/responder"

            #Call function named SearchPath
            foundPath = SearchPath(defaultDir)

            #If defaultDir not exists use "/"
            if foundPath != True:
                defaultDir = "/"

            #Search file in directories
            for root, dirs, files in walk(defaultDir):
                if file in files:
                    foundFileFlag = True
                    foundFile = path.join(root, file)
                
        case "windows":
            foundFile = "test"
        case _:
          foundFile = "not supported"
          print("[!] Not supported operating system...\n")
          exit(1)

    if foundFileFlag != True:
        print("[!] " + file + " does not exists in the system...\n")
        exit(1)

    return foundFile

#FindString funtion
def FindString(foundFile, searchingWord):
    with open(foundFile, 'r') as file:
        content = file.read()
        if searchingWord not in content:
            print("[!] " + foundFile + " does not support this configuration\n")
            exit(1)

#ModifyFile function
def ModifyFile(foundFile, searchingWord, candidateValue, statement):
    #Read file and find line
        with open(foundFile, 'r') as file:
            for index, line in enumerate(file):
                if searchingWord in line:
                    lineNumber = index + 1

        #Read file and save tha value to specific line
        with open(foundFile, 'r') as file:
            fileContents = file.readlines()
        
        fileContents[lineNumber - 1] = searchingWord + candidateValue + "\n"

        #Modify changes
        with open(foundFile, 'w') as file:
            file.writelines(fileContents)

        print("[+] " + statement + " has been set to " + "'" + candidateValue + "'" + " in " + foundFile + "...\n")

#main function
def main():
    #Call function named Arguments
    arguments = Arguments(argv)

    #Print ascii art
    print(__ascii__)

    candidateOS = system().lower()

    #Call function named FindOS
    foundOS = FindOS(candidateOS)

    #Call function named SearchFile
    foundFile = SearchFile(foundOS, "test.txt")

    #Clear DB section
    if arguments.cleardb:
        candidateOS = system().lower()

        #Call function named SearchFile
        foundFileDB = SearchFile(foundOS, "Responder.db")

        #delete Responder.db
        remove(foundFileDB)

        print("[+] " + foundFileDB + " has been deleted...\n")

    #Challenge section
    if arguments.NUMBER:
        candidateChallenge = arguments.NUMBER
        searchingWord = "Challenge = "
        statement = "Challenge"

        #Call function FindString
        FindString(foundFile, searchingWord)

        #Call function named ModifyFile
        ModifyFile(foundFile, searchingWord, candidateChallenge, statement)

    #DatabaseName Section
    if arguments.DATABASENAME:
        candidateDatabase = arguments.DATABASENAME
        searchingWord = "Database = "
        statement = "Database"

        #Call function FindString
        FindString(foundFile, searchingWord)

        #Call function named ModifyFile
        ModifyFile(foundFile, searchingWord, candidateDatabase, statement)
    
    #Session log section
    if arguments.SESSIONLOG:
        candidateSessionLog = arguments.SESSIONLOG
        searchingWord = "SessionLog = "
        statement = "Session Log"

        #Call function FindString
        FindString(foundFile, searchingWord)

        #Call function named ModifyFile
        ModifyFile(foundFile, searchingWord, candidateSessionLog, statement)

    #Poisoners log section
    if arguments.POISONERSLOG:
        candidatePoisonersLog = arguments.POISONERSLOG
        searchingWord = "PoisonersLog = "
        statement= "Poisoners Log"

        #Call function FindString
        FindString(foundFile, searchingWord)

        #Call function named ModifyFile
        ModifyFile(foundFile, searchingWord, candidatePoisonersLog, statement)

    #Analyze mode log section
    if arguments.ANALYZELOG:
        candidateAnlyzeLog = arguments.ANALYZELOG
        searchingWord = "AnalyzeLog = "
        statement= "Analyze Mode Log"

        #Call function FindString
        FindString(foundFile, searchingWord)

        #Call function named ModifyFile
        ModifyFile(foundFile, searchingWord, candidateAnlyzeLog, statement)

    #Config Dump log section
    if arguments.CONFIGDUMPLOG:
        candidateConfigDumpLog = arguments.CONFIGDUMPLOG
        searchingWord = "ResponderConfigDump = "
        statement= "Responder Config Dump Log"

        #Call function FindString
        FindString(foundFile, searchingWord)

        #Call function named ModifyFile
        ModifyFile(foundFile, searchingWord, candidateConfigDumpLog, statement)

if __name__ == "__main__":
    main()
