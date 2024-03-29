# carvingOpCodes.py
# carves the op codes from the three malware families:
# - winwebsec
# - zbot
# - zeroaccess
import os
import time
import re


'''UTILITY FUNCTIONS'''
# desc: prints the percent done in the terminal of a task
# input: index number, total length of task, (optional) bar length in terminal, and (optional) task message
# output: N/A
def print_percent_done(index, total, bar_len=20, title='Please wait'):
    '''
    index is expected to be 0 based index. 
    0 <= index < total
    '''
    percent_done = (index+1)/total*100
    percent_done_rounded = round(percent_done, 1)

    done = round(percent_done/(100/bar_len))
    togo = bar_len-done

    done_str = '█'*int(done)
    togo_str = '_'*int(togo)

    if percent_done_rounded == 100 and index >= total-2:
        print(f'{ "---DONE---" + title}: [{done_str}{togo_str}] {percent_done_rounded}% done',end='\r')
    else:
        print(f'{ " " + title}: [{done_str}{togo_str}] {percent_done_rounded}% done', end='\r')

# desc: Gets opCodeList and opCodeValueList to sort them by occurance.
#       The lists are sorted together, i.e. if the values are swapped, 
#       the opcodes are swapped. Output is descending order. 
#       (change inequality on line 40 to acending order)
# input: two lists: opCodeList, opCodeValueList
# output: a sorted dictionary, opcode = occuranceValue
def bubbleSortOpCodes(opCodeList, opCodeValueList):
    sortedDictionary = { }
    for j in range (0, len(opCodeList), 1):
        for i in range (0, len(opCodeList)-1, 1): 
            if opCodeValueList[i] < opCodeValueList[i+1]:
                # swapping values 
                tempValue = opCodeValueList[i]
                opCodeValueList[i] = opCodeValueList[i+1]
                opCodeValueList[i+1] = tempValue

                # swapping opcodes
                tempOpCode = opCodeList[i]
                opCodeList[i] = opCodeList[i+1] 
                opCodeList[i+1] = tempOpCode
        print_percent_done(j,len(opCodeList),title="Sorting opcodes")
    print('\n')
    # once lists are sorted
    for dictionaryEntry in range(0,len(opCodeList),1):
        sortedDictionary[opCodeList[dictionaryEntry]] = opCodeValueList[dictionaryEntry]

    return sortedDictionary

# desc: gets the file opcodes 
# input: the file (asm.txt)
# output: returns a list of opcodes
def getFileData(FILE_NAME):
    opCodeTable = open(FILE_NAME, "r")
    opCodeTableList = opCodeTable.read().splitlines()
    return opCodeTableList

# desc: opens a write file
# input: FILE_NAME
# output: file object
def openWriteFile(FILE_NAME,hasUnderscore):
    if hasUnderscore == True:
        fileStr = FILE_NAME+"_Converted.asm.txt"
    else:
        fileStr = FILE_NAME
    fileToWrite = open(fileStr, "w")
    return fileToWrite

# desc: splits a dictionary with "'"
# input: a dictionary to split
# output: a string of the split dictionary
def splitADictionary(dictionaryToSplit,splitParameter):
    strDictionary = str(dictionaryToSplit)
    splitDictionary = strDictionary.split(splitParameter)
    return splitDictionary

# desc: gets CWD of where this file is located
# input: N/A
# output: string of the CWD
def getCWD():
    originalCWD = os.getcwd()
    return originalCWD

# desc: gets the list of the files in a specific subfolder in the CWD
# input: CWD of where this file is located, a subfolder from CWD
# output: a list of file paths readable for the CWD
def getFileList(currentWorkingDIR,subfolder):
    # create a new path to the directory with the given subfolders
    newCWD = os.path.join(currentWorkingDIR, subfolder)
    fileList = os.listdir(newCWD) # grab the list of all files in the directory
    return fileList

# desc: regex match finder
# input: pattern to search for, text to search in
# output: boolean value whether it found a match
def findMatch(pattern, text):
    match = re.search(pattern, text)
    if match:
        return True
    else:
        return False


'''CORE PROGRAM FUNCTIONS'''
# desc: scans the directory for files and other directories
# input: CWD of where this file is located, subfolders of the CWD
# output: list containing dictionaries of the content contained in
#         each file
def scanDirectoryFiles(currentWorkingDIR,subfolders):
    fileContentDictionaryList = [ ] # a list of dictionaries { push: 1 }

    for pathIndex in range(0,len(subfolders),1):
        fileList = getFileList(currentWorkingDIR,subfolders[pathIndex])
        # appending the processed file data into a dictionary for all files in the directory
        for fileListIndex in range(0,len(fileList),1):
            # if the file dirctory does not have an underscore, meaning it is not a converted file 
            # (it will skip converted files if it is false)
            if findMatch('_',os.path.join(subfolders[pathIndex], fileList[fileListIndex])) == False:
                fileDataObject = processFileData(os.path.join(subfolders[pathIndex], fileList[fileListIndex]))
                # print progress
                print_percent_done(fileListIndex,len(fileList),title='Scanning and processesing files in '+ subfolders[pathIndex])
                # process the file's content and append the content dictionary in the list
                fileContentDictionaryList.append(fileDataObject) # file data
        print("\n")
    
    return fileContentDictionaryList 

# desc: organizes and counts the opcodes of the opCodeList
# input: fileContentDictionaries in a list, the list of opcodes
# output: sorted opCode dictionary, opcodes are keys per a paired occurance value in descending order
def organizeAndCountOpCodes(fileContentDictionaryList,opCodeList):
    sortedOpCodeDictionary = { }
    opCodeValueList = [ ]

    # appending values to the value list checking the occurance of opcodes
    for opCodeInList in range(0,len(opCodeList),1):
        opCodeValueList.append(0) # append the value as zero initially

        for dictionaryIndex in range(0,len(fileContentDictionaryList),1):
            
            # getting content of each dictionary per file
            chosenDictionary = fileContentDictionaryList[dictionaryIndex]
            splitDictionary = splitADictionary(chosenDictionary,"'")

            # compare opcodes to find all duplicate opcodes to count occurance
            # starts at 1 to avoid the '{' at the start of the split dictionary, 
            # and opcodes (keys) are found in every other element in the string (inc by 2)
            for opCodeInDictionary in range(1,len(splitDictionary),2):
                # if the opcode duplicate is found with a match in the content dictionary
                if opCodeList[opCodeInList] == splitDictionary[opCodeInDictionary]:
                    opCodeValueList[opCodeInList] += 1 # increment the value in the value list
        
        # progress
        print_percent_done(opCodeInList,len(opCodeList),title="Counting opcodes from file content")
    print("\n")

    # once all values have been counted, sort the opCodeList and opCodeValueList accordingly
    sortedOpCodeDictionary = bubbleSortOpCodes(opCodeList,opCodeValueList)
    return sortedOpCodeDictionary

# desc: processes the file data of a file and appends it to a dictionary of key value pairs
#       (opcode is our key, occurance value is our value of the key)
#       this will be used later to sum up the occurances in each file (and possbily each family)
# input: FILE_NAME
# output: opCodeCounterDictionary, a dictionary of opCodes
def processFileData(FILE_NAME):
    opCodeCounterDictionary = { }
    fileOpCodes = getFileData(FILE_NAME) # get the file data

    # loading up content dictionary of file data
    for opCodeIndex in range(0,len(fileOpCodes),1):
        # if the list is at the beginning
        if opCodeIndex == 0:
            # append the first opcode with a value
            opCodeCounterDictionary[fileOpCodes[opCodeIndex]] = 1
        # else, the opCodeCounterDictionary does have elements, and check for duplicates to increment
        else:
            # split the dictionary
            splitOpCodeDictionary = splitADictionary(opCodeCounterDictionary,"'")

            # compare opcodes to find all duplicate opcodes to count occurance 
            # within content dictionary
            # starts at 1 to avoid the '{' at the start of the split dictionary, 
            # and opcodes (keys) are found in every other element in the string (inc by 2)
            for opCode in range(1,len(splitOpCodeDictionary),2):
                # if the opcode found in the split dictionary has a match in the file op codes
                if splitOpCodeDictionary[opCode] == fileOpCodes[opCodeIndex]:
                    # increment the value
                    opCodeCounterDictionary[splitOpCodeDictionary[opCode]] = opCodeCounterDictionary[splitOpCodeDictionary[opCode]] + 1
                    break # break to the next item in the split dictionary
                # else, if there was no match found
                elif opCode == len(splitOpCodeDictionary)-2:
                    # create a new key-value pair for the unique opcode
                    opCodeCounterDictionary[fileOpCodes[opCodeIndex]] = 1
    
    return opCodeCounterDictionary

# desc: writes converted data and calculates avg opcode occurance percentage from user specified opcodes
# input: opcodes that are included (will have values from 1,2,3,...,N opcodes), subfolders
# output: opCodeAvgLit, a list of lists (each inner list contains percentages for opcodes contained in 
#         each file to be calcuated as a group average)
def writeData(includedOpCodes,subfolders):
    opCodeIncrementList = [ ] # used to keep track of the
                              # opcode increments in each file
    opCodePercentList = [ ] # opcode percentages, will be overwritten every file
                            # when overwriting, it will send the percentages 
                            # somewhere to the neural network for training
    csvFileFormatStringList = [ ] # csv file string to format all elements for each row of the csv file
    opCodeTotalSum = 0 # total opcoes in each file, gets recycled
    excludedOpCodeIncrement = 0
    # lists corresponds to the placement of the opcode
    includedOpCodeSumList = [ ] # sum elements of each opcode per family 
    
    print("Starting file write...")
    currentWorkingDIR = getCWD() 

    # open the write file for the csv file
    maliciaCSV = openWriteFile("maliciaCSV.csv",False)

    # used per each subfolder in the CWD
    # inslide CWD
    for pathIndex in range(0,len(subfolders),1):
        fileList = getFileList(currentWorkingDIR,subfolders[pathIndex])
        
        # using each file to write a converted file 
        # inside file list
        for fileListIndex in range(0,len(fileList),1):
            # initialize the percentages list to change the percentages
            # if the file dirctory does not have an underscore, meaning it is not a converted file 
            # (it will skip converted files if it is false)
            if findMatch('_',os.path.join(subfolders[pathIndex], fileList[fileListIndex])) == False:
                
                # initialize lists
                for includedOpCode in range(0,len(includedOpCodes),1):
                    if pathIndex == 0 and fileListIndex == 0:
                        opCodeIncrementList.append(0)
                        includedOpCodeSumList.append(0)
                        opCodePercentList.append(0)
                    else:
                        opCodeIncrementList[includedOpCode] = 0
                        includedOpCodeSumList[includedOpCode] = 0
                        opCodePercentList[includedOpCode] = 0
                        csvFileFormatStringList.clear()
                
                # open the write file and get the data of the specific file
                fileToWrite = openWriteFile(os.path.join(subfolders[pathIndex], fileList[fileListIndex]),True)
                fileContent = getFileData(os.path.join(subfolders[pathIndex], fileList[fileListIndex]))
                # using each content to compare the included opcodes to write a number 
                # (as user specified, each will be 1,2,3,...N)
                # inside file
                for contentAtID in range(0,len(fileContent),1):
                    opCodeTotalSum = opCodeTotalSum + 1
                    # within this section, we have a specific opcode in a said file
                    for includedOpCode in range(0,len(includedOpCodes),1):
                        # here, we check all opcodes that are labeled as included to determine the value it is
                        ## EX: the loop index+1 will be given to an opcode found that is in the list
                        ## pop = 1, so index+1 needs to be = 1, therefore the included list has pop at the top 
                        ## of the list and is then compared in the file to write a 1 in it's place in the converted file
                        
                        # if the file content opcode is an opcode that is labeled to be included
                        if fileContent[contentAtID] == includedOpCodes[includedOpCode]:
                            fileToWrite.write(str(includedOpCode+1)+'\n') # write it's corresponding number based on the 
                                                                          # occurance placement from the included opcode list
                            opCodeIncrementList[includedOpCode] += 1
                            break # break to the next content opcode
                        # else, if we are at the end of the list of included opcodes, the content opcode is not labeled as an 
                        # included opcode and is then written a '0' in it's place in the converted file
                        elif includedOpCode == len(includedOpCodes)-1:
                            fileToWrite.write(str(0)+'\n')
                            excludedOpCodeIncrement = excludedOpCodeIncrement + 1

                # appends all the opcode percentages of the included opcodes, as well as the csv string list for the csv file
                for includedOpCode in range(0,len(includedOpCodes),1):
                    opCodePercentList[includedOpCode] = round((opCodeIncrementList[includedOpCode]/opCodeTotalSum)*100,2)
                    csvFileFormatStringList.append(opCodePercentList[includedOpCode])

                # append the remaining percent (excluded opcode percentage) and the path index label
                # winwebsec is 0, zbot is 1
                csvFileFormatStringList.append(round((excludedOpCodeIncrement/opCodeTotalSum)*100,2))
                csvFileFormatStringList.append(str(pathIndex))

                # csv file writing with the csv format string list
                for formatStringListIndex in range(0,len(csvFileFormatStringList),1):
                    # if the loop is at the end of the list, append the contents at that index in the list followed by a break line
                    if formatStringListIndex == len(csvFileFormatStringList)-1:
                        maliciaCSV.write(str(csvFileFormatStringList[formatStringListIndex])+"\n")
                    # else, follow the contents with a comma
                    else:
                        maliciaCSV.write(str(csvFileFormatStringList[formatStringListIndex])+",")

                opCodeTotalSum = 0 # reset the total sum and excluded opcode increment for the next file
                excludedOpCodeIncrement = 0
                # progress           
                print_percent_done(fileListIndex,len(fileList),title="Writing coverted opcode names for files in " + subfolders[pathIndex])
                fileToWrite.close()
        print("\n")
    maliciaCSV.close() # close the write file
    print("Opcode conversion  complete! Check files ending in '_Converted.asm.txt' for converted data!")

# desc: scans the files and processes the data contents with other function calls
# input: the dynamic CWD being scanned; the dictionary of files in CWD
# output: N/A 
def processDirectoryContents(currentWorkingDIR,subfolders):
    fileContentDictionaryList = [ ] # a list of dictionaries
    opCodes = { } # opCode dictionary for amount of occurances
    opCodeList = [ ] # all the opcodes in the files
    includedOpCodes = [ ] # and included opCodes
    includedOpCodesOutput = [ ] # for the user output to show what opcodes are being kept


    start = time.time() # start timer for reading data
    # get file content dictionaries from the scan
    fileContentDictionaryList = scanDirectoryFiles(currentWorkingDIR,subfolders)
    splitDictionary = [] # local splitDictionary for access later 
    # grabs a dictionary from the list to find the opcodes
    for dictionaryIndex in range(0,len(fileContentDictionaryList),1):
        chosenDictionary = fileContentDictionaryList[dictionaryIndex]
        splitDictionary = splitADictionary(chosenDictionary,"'")

        # compare opcodes to find all unique opcodes
        # starts at 1 to avoid the '{' at the start of the split dictionary, 
        # and opcodes (keys) are found in every other element in the string (inc by 2)
        for opCodeInDictionary in range(1,len(splitDictionary),2):
            # if the list of opcodes is empty, append the first opcode found in the split dictionary
            if len(opCodeList) == 0:
                opCodeList.append(splitDictionary[opCodeInDictionary])
            else:
                # checking each opcode in the list to the split dictionary for any duplicates
                for opCodeInList in range(0,len(opCodeList),1):
                    # if the opcode list has an opcode that matches an opcode in the split dictionary
                    if opCodeList[opCodeInList] == splitDictionary[opCodeInDictionary]:
                        break # break out of loop to the next one
                    # else, if we are at the end of the list of opCodes, 
                    # there is a new opcode to add to the list
                    elif opCodeInList == len(opCodeList)-1:
                        opCodeList.append(splitDictionary[opCodeInDictionary])
        # progress bar
        print_percent_done(dictionaryIndex,len(fileContentDictionaryList),title="Finding opcodes in files")
    print("\n")
    # get the opCode dictionary that is filled with opcode keys with occurance values for each opcode
    # this dictionary will be unorganized and needs to be sorted later
    opCodes = organizeAndCountOpCodes(fileContentDictionaryList,opCodeList)
    splitOpCodeDictionary = splitADictionary(opCodes,"'")
    
    # end the timer for processing data
    end = time.time()
    time.sleep(1)
    print("Time processing data:",round(end - start,1),"seconds")

    # user input section
    while True:
        # get user's chosen amount of opcodes
        amountOfOpCodes = int(input("Select how many of the most common opcodes: "))

        # show the user what opcodes are being kept and others being excluded
        opCodeCounter = 0
        for opCodeInDictionary in range(1,len(splitOpCodeDictionary),2):
            # if the opcode counter is less than the amount the user specified (-1 because the list starts at 0)
            if opCodeCounter <= amountOfOpCodes - 1:
                # let the user know what opcode we are keeping
                includedOpCodesOutput.append(" '"+str(splitOpCodeDictionary[opCodeInDictionary]) + "' with " + str(opCodes[splitOpCodeDictionary[opCodeInDictionary]]) + " occurances"
                                        " is named "+str(opCodeCounter+1)) # +1 since the '0' is reserved for excluded opcodes
                includedOpCodes.append(splitOpCodeDictionary[opCodeInDictionary])
            opCodeCounter = opCodeCounter + 1
        
        print("\nKeeping: ")
        for outputIndex in range(0,len(includedOpCodesOutput),1):
            print(includedOpCodesOutput[outputIndex])
        print("Excluding all other opcodes and replacing them with '0'\n")

        start = time.time() # start write sequence timer
        writeData(includedOpCodes,subfolders) # write the converted data to _Converted.asm.txt files
        end = time.time() # end timer
        print("\nTime writing data:",round(end - start,1),"seconds\n")

        # if the user wants to leave, they'll input 0
        endLoop = int(input("\nTry another amount? (1 for yes, 0 for no): "))
        if endLoop == 0:
            break
        # else, reset what is being included
        else:
            includedOpCodes = []
            includedOpCodesOutput = []


''' PROGRAM '''
def main():
    subfolders = [ ]
    originalCWD = getCWD()
    # used to append only the directories to the subfolders list
    for entry in os.scandir(originalCWD): # scan the CWD
        if entry.is_dir(): # if the entry in the CWD is a directory
            subfolders.append(entry.name) # append to the subfolders list
    processDirectoryContents(originalCWD, subfolders)
        
main()
''' 
TEST RUN:
$ python carvingOpCodes.py 
---DONE---Scanning and processesing files in winwebsec: [████████████████████] 100.0% done

---DONE---Scanning and processesing files in zbot: [████████████████████] 100.0% done

---DONE---Scanning and processesing files in zeroaccess: [████████████████████] 100.0% done

---DONE---Finding opcodes in files: [████████████████████] 100.0% done

---DONE---Counting opcodes from file content: [████████████████████] 100.0% done

---DONE---Sorting opcodes: [████████████████████] 100.0% done

Time processing data: 577.7 seconds
Select how many of the most common opcodes: 5

Keeping:
 'push' with 7801 occurances is named 1
 'mov' with 7801 occurances is named 2
 'pop' with 7801 occurances is named 3
 'call' with 7799 occurances is named 4
 'add' with 7798 occurances is named 5
Excluding all other opcodes and replacing them with '0'

Starting file write...
---DONE---Writing coverted opcode names for files in winwebsec: [████████████████████] 100.0% done

---DONE---Writing coverted opcode names for files in zbot: [████████████████████] 100.0% done

---DONE---Writing coverted opcode names for files in zeroaccess: [████████████████████] 100.0% done

Opcode conversion complete! Check files ending in '_Converted.asm.txt' for converted data!

Time writing data: 110.2 seconds

Try another amount? (1 for yes, 0 for no): 1
Select how many of the most common opcodes: 15

Keeping:
 'push' with 7801 occurances is named 1
 'mov' with 7801 occurances is named 2
 'pop' with 7801 occurances is named 3
 'call' with 7799 occurances is named 4
 'add' with 7798 occurances is named 5
 'retn' with 7796 occurances is named 6
 'sub' with 7791 occurances is named 7
 'xor' with 7788 occurances is named 8
 'lea' with 7784 occurances is named 9
 'cmp' with 7772 occurances is named 10
 'jnz' with 7761 occurances is named 11
 'jz' with 7719 occurances is named 12
 'test' with 7708 occurances is named 13
 'and' with 7630 occurances is named 14
 'jmp' with 7591 occurances is named 15
Excluding all other opcodes and replacing them with '0'

Starting file write...
---DONE---Writing coverted opcode names for files in winwebsec: [████████████████████] 100.0% done

---DONE---Writing coverted opcode names for files in zbot: [████████████████████] 100.0% done

---DONE---Writing coverted opcode names for files in zeroaccess: [████████████████████] 100.0% done

Opcode conversion complete! Check files ending in '_Converted.asm.txt' for converted data!

Time writing data: 118.3 seconds

Try another amount? (1 for yes, 0 for no): 0

'''