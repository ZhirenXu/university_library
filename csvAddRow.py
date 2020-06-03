import os
import sys
import csv
import shutil

def welcome():
    print("***************************************")
    print("*     CSV Empty Row Adder v1.0.0      *")
    print("*          Author: Zhiren Xu          *")
    print("*        published data: 6/3/20       *")
    print("***************************************")

def end():
    print("The process is finished.")
    print("Press anykey to exit")
    input()
    sys.exit()

def getCSVInput():
    print("Please enter csv file name with .csv. \nThe file must in the same folder with your main.py program: ")
    fileIn = input()

    return fileIn

## read from input csv, write to out.csv, then change name to original file name
# @param    fileName
#           inputFile Name
# @update
#           input csv file
def writeCSV(fileName):
    i = 1
    blankRowNum = 0
    
    try:
        inFile = open(fileName, 'r')
    except:
        print("Fail to open input CSV. Press enter to exit.")
        key = input()
        sys.exit()
    try:
        outFile = open("Out.csv", 'w', newline = '')
    except:
        print("Fail to create file. Check if out.csv already exist under script directory.")
        print("Press enter to exit.")
        sys.exit()
    csvReader = csv.reader(inFile, delimiter=',')
    csvWriter = csv.writer(outFile, delimiter=',')
    for row in csvReader:
        try:
            print("Change ", i, " line......", end = "")
            blankRowNum = int(row[2])
            csvWriter.writerow(row)
            while blankRowNum > 0:
                csvWriter.writerow([])
                blankRowNum = blankRowNum - 1
            print("childRow found. Done.")
            i = i + 1
        except:
            print("childRow not found. No row get added.")
            csvWriter.writerow(row)
            i = i + 1
    inFile.close()
    outFile.close()
        
def main():
    welcome()
    file = getCSVInput()
    print("Modify CSV...\n")
    writeCSV(file)
    os.remove(file)
    os.rename('Out.csv', file)
    end()
    
if __name__ == "__main__":
    main()
