##############################################
#      Responder-Parser.py                   #
#      Author: Nikos Vourdas (@nickvourd)    #
#      License: MIT                          #
#      Required Dependencies: None           #
##############################################

import argparse
from platform import system
from os import walk, path, remove
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
    parser.add_argument('-c', '--challenge', type=str, dest='NUMBER', required=False, help="set challenge to Repsonder conf")
    parser.add_argument('--cleardb', action='store_true', required=False, help="clear Responder.db data")
    parser.add_argument('--setsql', type=str, dest='SQLSWITCH', required=False, help="set SQL server ON/OFF to Responder conf")
    parser.add_argument('--setsmb', type=str, dest='SMBSWITCH', required=False, help="set SMB server ON/OFF to Responder conf")
    parser.add_argument('--setrdp', type=str, dest='RDPSWITCH', required=False, help="set RDP server ON/OFF to Responder conf")
    parser.add_argument('--setkerberos', type=str, dest='KERBEROSSWITCH', required=False, help="set Kerberos server ON/OFF to Responder conf")
    parser.add_argument('--setftp', type=str, dest='FTPSWITCH', required=False, help="set FTP server ON/OFF to Responder conf")
    parser.add_argument('--setpop', type=str, dest='POPSWITCH', required=False, help="set POP server ON/OFF to Responder conf")
    parser.add_argument('--setsmtp', type=str, dest='SMTPSWITCH', required=False, help="set SMTP server ON/OFF to Responder conf")
    parser.add_argument('--setimap', type=str, dest='IMAPSWITCH', required=False, help="set IMAP server ON/OFF to Responder conf")
    parser.add_argument('--sethttp', type=str, dest='HTTPSWITCH', required=False, help="set HTTP server ON/OFF to Responder conf")
    parser.add_argument('--sethttps', type=str, dest='HTTPSSWITCH', required=False, help="set HTTPS server ON/OFF to Responder conf")
    parser.add_argument('--setdns', type=str, dest='DNSSWITCH', required=False, help="set DNS server ON/OFF to Responder conf")
    parser.add_argument('--setldap', type=str, dest='LDAPSWITCH', required=False, help="set LDAP server ON/OFF to Responder conf")
    parser.add_argument('--setdcerpc', type=str, dest='DCERPCSWITCH', required=False, help="set DCERPC server ON/OFF to Responder conf")
    parser.add_argument('--setwinrm', type=str, dest='WINRMSWITCH', required=False, help="set WINRM server ON/OFF to Responder conf")
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

#DetermineSwitch function
def DetermineSwitch(statement, candidateValue):
    if candidateValue.lower() != "on" and candidateValue.lower() != "off":
        newValue = "nothing"
        print("[!] " + statement + " parameter accepts only ON/OFF values...")
        exit(1)

    match candidateValue.lower():
        case "on":
            newValue = "On"
        case "off":
            newValue = "Off"
        
    return newValue

#ConfigureOnOff function
def ConfigureOnOff(foundFile, searchingWord, candidateServer, statement):
    #Call function named DetermineSwitch
    foundSwitch = DetermineSwitch(statement, candidateServer)

    #Call function FindString
    FindString(foundFile, searchingWord)

    #Call function named ModifyFile
    ModifyFile(foundFile, searchingWord, foundSwitch, statement)

#ConfigureString function
def ConfigureString(keyword, optionNumber):
    searchingWord = keyword + " = "

    match optionNumber:
        case 1:
            statement =  keyword + " Server"
        case 2:
            statement =  keyword
        case 3:
            statement = "Database"
        case 4:
            statement = "Challenge"
    

    return searchingWord, statement

#ConfigureValues function
def ConfigureValues(foundFile, searchingWord, candidateValue, statement):
    #Call function FindString
    FindString(foundFile, searchingWord)

    #Call function named ModifyFile
    ModifyFile(foundFile, searchingWord, candidateValue, statement)

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
        candidateValue = arguments.NUMBER

        #Call function named ConfigureString
        configuredStrings = ConfigureString("Challenge", 4)

        #Call function ConfigureValues
        ConfigureValues(foundFile, configuredStrings[0], candidateValue, configuredStrings[1])

    #DatabaseName Section
    if arguments.DATABASENAME:
        candidateValue = arguments.DATABASENAME

        #Call function named ConfigureString
        configuredStrings = ConfigureString("Database", 3)

        #Call function ConfigureValues
        ConfigureValues(foundFile, configuredStrings[0], candidateValue, configuredStrings[1])
    
    #Session log section
    if arguments.SESSIONLOG:
        candidateValue = arguments.SESSIONLOG

        #Call function named ConfigureString
        configuredStrings = ConfigureString("SessionLog", 2)

        #Call function ConfigureValues
        ConfigureValues(foundFile, configuredStrings[0], candidateValue, configuredStrings[1])

    #Poisoners log section
    if arguments.POISONERSLOG:
        candidateValue = arguments.POISONERSLOG

        #Call function named ConfigureString
        configuredStrings = ConfigureString("PoisonersLog", 2)

        #Call function ConfigureValues
        ConfigureValues(foundFile, configuredStrings[0], candidateValue, configuredStrings[1])

    #Analyze mode log section
    if arguments.ANALYZELOG:
        candidateValue = arguments.ANALYZELOG

        #Call function named ConfigureString
        configuredStrings = ConfigureString("AnalyzeLog", 2)

        #Call function ConfigureValues
        ConfigureValues(foundFile, configuredStrings[0], candidateValue, configuredStrings[1])

    #Config Dump log section
    if arguments.CONFIGDUMPLOG:
        candidateValue = arguments.CONFIGDUMPLOG

        #Call function named ConfigureString
        configuredStrings = ConfigureString("ResponderConfigDump", 2)

        #Call function ConfigureValues
        ConfigureValues(foundFile, configuredStrings[0], candidateValue, configuredStrings[1])

    #SQL Server section
    if arguments.SQLSWITCH:
        candidateServer = arguments.SQLSWITCH

        #Call function named ConfigureString
        configuredStrings = ConfigureString("SQL", 1)

        #Call function named ConfigureOnOff
        ConfigureOnOff(foundFile, configuredStrings[0], candidateServer, configuredStrings[1])

    #SMB Server section
    if arguments.SMBSWITCH:
        candidateServer = arguments.SMBSWITCH

        #Call function named ConfigureString
        configuredStrings = ConfigureString("SMB", 1)

        #Call function named ConfigureOnOff
        ConfigureOnOff(foundFile, configuredStrings[0], candidateServer, configuredStrings[1])

    #RDP Server section
    if arguments.RDPSWITCH:
        candidateServer = arguments.RDPSWITCH

        #Call function named ConfigureString
        configuredStrings = ConfigureString("RDP", 1)

        #Call function named ConfigureOnOff
        ConfigureOnOff(foundFile, configuredStrings[0], candidateServer, configuredStrings[1])

    #Kerberos Server section
    if arguments.KERBEROSSWITCH:
        candidateServer = arguments.KERBEROSSWITCH

        #Call function named ConfigureString
        configuredStrings = ConfigureString("Kerberos", 1)

        #Call function named ConfigureOnOff
        ConfigureOnOff(foundFile, configuredStrings[0], candidateServer, configuredStrings[1])
    
    #FTP Server section
    if arguments.FTPSWITCH:
        candidateServer = arguments.FTPSWITCH

        #Call function named ConfigureString
        configuredStrings = ConfigureString("FTP", 1)

        #Call function named ConfigureOnOff
        ConfigureOnOff(foundFile, configuredStrings[0], candidateServer, configuredStrings[1])
    
    #POP Server section
    if arguments.POPSWITCH:
        candidateServer = arguments.POPSWITCH

        #Call function named ConfigureString
        configuredStrings = ConfigureString("POP", 1)

        #Call function named ConfigureOnOff
        ConfigureOnOff(foundFile, configuredStrings[0], candidateServer, configuredStrings[1])

    #SMTP Server section
    if arguments.SMTPSWITCH:
        candidateServer = arguments.SMTPSWITCH

        #Call function named ConfigureString
        configuredStrings = ConfigureString("SMTP", 1)

        #Call function named ConfigureOnOff
        ConfigureOnOff(foundFile, configuredStrings[0], candidateServer, configuredStrings[1])
    
    #IMAP Server section
    if arguments.IMAPSWITCH:
        candidateServer = arguments.IMAPSWITCH

        #Call function named ConfigureString
        configuredStrings = ConfigureString("IMAP", 1)

        #Call function named ConfigureOnOff
        ConfigureOnOff(foundFile, configuredStrings[0], candidateServer, configuredStrings[1])
    
    #HTTP Server section
    if arguments.HTTPSWITCH:
        candidateServer = arguments.HTTPSWITCH

        #Call function named ConfigureString
        configuredStrings = ConfigureString("HTTP", 1)

        #Call function named ConfigureOnOff
        ConfigureOnOff(foundFile, configuredStrings[0], candidateServer, configuredStrings[1])
    
    #HTTPS Server section
    if arguments.HTTPSSWITCH:
        candidateServer = arguments.HTTPSSWITCH

        #Call function named ConfigureString
        configuredStrings = ConfigureString("HTTPS", 1)

        #Call function named ConfigureOnOff
        ConfigureOnOff(foundFile, configuredStrings[0], candidateServer, configuredStrings[1])   
    
    #DNS Server section
    if arguments.DNSSWITCH:
        candidateServer = arguments.DNSSWITCH

        #Call function named ConfigureString
        configuredStrings = ConfigureString("DNS", 1)

        #Call function named ConfigureOnOff
        ConfigureOnOff(foundFile, configuredStrings[0], candidateServer, configuredStrings[1])

    #LDAP Server section
    if arguments.LDAPSWITCH:
        candidateServer = arguments.LDAPSWITCH

        #Call function named ConfigureString
        configuredStrings = ConfigureString("LDAP", 1)

        #Call function named ConfigureOnOff
        ConfigureOnOff(foundFile, configuredStrings[0], candidateServer, configuredStrings[1])

    #DCERPC Server section
    if arguments.DCERPCSWITCH:
        candidateServer = arguments.DCERPCSWITCH

        #Call function named ConfigureString
        configuredStrings = ConfigureString("DCERPC", 1)

        #Call function named ConfigureOnOff
        ConfigureOnOff(foundFile, configuredStrings[0], candidateServer, configuredStrings[1])    
    
    #WINRM Server section
    if arguments.WINRMSWITCH:
        candidateServer = arguments.WINRMSWITCH

        #Call function named ConfigureString
        configuredStrings = ConfigureString("WINRM", 1)

        #Call function named ConfigureOnOff
        ConfigureOnOff(foundFile, configuredStrings[0], candidateServer, configuredStrings[1])

if __name__ == "__main__":
    main()
