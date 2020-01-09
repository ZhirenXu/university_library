import sys
import json
import csv
import re
import urllib.request
import requests
from bs4 import BeautifulSoup

# open csv file and read handler link, store in a list
# @param    csvName
#           the file name user typed in
# @return   urlList
#           a list contain item url that need to be scraped
def readCSV(csvName):
    urlList = []
    inFile = open(csvName, 'r')
    csvReader = csv.reader(inFile, delimiter=',')
    for row in csvReader:
        urlList.append(row[0])
    # del the column name read for first line
    urlList.pop(0)
    return urlList

# write category and data into csv file
# @param    categoryList
#           a list contain category name of data
# @param    dataList
#           a list contain useful data
# @param    outputFile
#           output File pointed by user
def writeCSV(list_, outputFile):
    # write all ids into file
    print("Writing identifiers into ", outputFile, "...")
    #open file for output
    try:
        outFile = open(outputFile, 'w', encoding = 'utf8', newline='')
        csvWriter = csv.writer(outFile)
        for element in list_:
            csvWriter.writerow([category])
        for data in dataList:
            csvWriter.writerow([data])
        print("Complete!")
        outFile.close()
    except:
        print("Fail to write csv!")
        
# get the name of this collection
# @param    soup
#           a parsed url
# @return   collectionName
def getCollectionName(soup):
    collectionName = ""
    name = soup.find('input', attrs = {"type" : "hidden", "name" : "f[collection_name_sim][]"})
    if name != None:
        collectionName = name.get("value")
    else:
        collectionName = "can't_retreive"
    return collectionName

# parse url link to readable bs4 content
# @param    url
#           The url needed to be parsed
# @return   soup
#           parsed url
def parseUrl(url):
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, 'html.parser')
    return soup

# get 100-per-page link from input url
# @param    soup
#           parsed url from input file
# @return   maxRecordLink
#           an unparsed 100-per-page url
def getMaxRecords(soup):
    maxRecordLink = "https://library.osu.edu"
    aTagList = soup.find_all('a')
    for aTag in aTagList:
        if '100' in aTag.contents:   
            href = aTag.get('href')
            if href != None:
                maxRecordLink += href
                break
    return maxRecordLink

# parse an url, find JSON link and extract results in a dict
# @param    url
#           an unparsed input url
# @param    idContainer
#           an container to store id
def getJson(url, idContainer):
    soup = parseUrl(url)
    # find tag which contains json link
    linkTag = soup.find('link', attrs={"type": "application/json"})
    # extract 100-record json link from attribute
    jsonLink = "https://library.osu.edu"
    jsonLink += linkTag.get('href')
    # open json link
    jsonPage = requests.get(jsonLink)
    jsonContent = jsonPage.json()
    try:
        for tuple_ in jsonContent["docs"]:
            isInContainer = tuple_["id"] in idContainer
            if not isInContainer:
                idContainer.append(tuple_["id"])
    except(ValueError, KeyError, TypeError):
        print("Fail to extract json data!")

# find url for next page and return it
# @param    url
#           current unparsed page url
# @return   nextUrl
#           next page's url. If it is the last page,return None
def getNextPage(url):
    nextUrl = "https://library.osu.edu"
    soup = parseUrl(url)
    aTag= soup.find('a', attrs={"rel": "next"})
    if aTag != None:
        nextUrl += aTag.get('href')
    else:
        nextUrl == None
    return nextUrl
        
def main():
    pageUrl = []
    csvCategory = []
    ids = []
    i = 0
    remainRecords = 0
    # get inputfile
    print("Please enter csv file name. The file must in the same folder with your main.py program: ")
    fileIn = input()
    # get outputfile
    print("Please enter output file name: ")
    fileOut = input()
    try:
        pageUrl = readCSV(fileIn)
    except:
        print("Fail to open this file. Press enter to exit.")
        key = input()
        sys.exit()
    numOfUrl = len(pageUrl)
    print("There are ", numOfUrl, " records in the input file.")
    # id scraping
    outFile = open(fileOut, 'w', encoding = 'utf8', newline='')
    csvWriter = csv.writer(outFile)
    for url in pageUrl:
        # parse url
        print("Reading url...", end = "")
        parsedUrl = parseUrl(url)
        # find the name of collection
        collectionTitle = getCollectionName(parsedUrl)
        ids.append(collectionTitle)
        # find how many records in this collection
        tag = parsedUrl.find('meta', attrs={'name': "totalResults"})
        numOfRecords = int(tag['content'])
        remainRecords = numOfRecords
        # find 100-per-page link
        maxRecordLink = getMaxRecords(parsedUrl)
        nextLink = maxRecordLink
        print("OK")
        # after get that link, read json data from it
        while remainRecords > 0:
            print("Get JSON data...", end = "")
            getJson(nextLink, ids)
            print("OK")
            print("Find rest of JSON page for this link...", end = "")
            nextPage = getNextPage(nextLink)
            nextLink = nextPage
            print("OK. Remaining records for this link: ", end = "")
            remainRecords = numOfRecords - len(ids)
            print(remainRecords)
            print("number of ids: ", len(ids))
        i += 1
        print(i, "/", len(pageUrl), " has been processed.")
        csvWriter.writerow(ids)
        ids = []
    # write data to csv file
    #writeCSV(csvCategory, ids, fileOut)
    # program exit
    print("The program has finished. The output file is: ", fileOut, " . It is located in the same folder with your main.py program. Press enter to exit.")
    key = input()
    sys.exit()
    
if __name__ == "__main__":
    main()
