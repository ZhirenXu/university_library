import sys
import urllib.request
import csv
from bs4 import BeautifulSoup

## Contain all category name a collection probably has in DC.
## Add/Delete keywords in the list to create new .csv w/ more/less category. Don't forget to delete corresponding liTag!
## Follow the format when change this list.
categoryList = ["Title", "internal id link", "Alternative title", "Resource Type", "Creator", "Contributor", "Genre", "Language",
"Publisher", "Date created", "Date issued", "Date copyrighted", "Summary",
"Description", "Staff notes", "Format", "Extent", "Measurements", "Repository",
"Collection", "Sub collection", "Source", "Provenance", "Related finding aid",
"Related URL", "Identifier", "Call number", "Collection identifier", "Archival context",
"Published in", "Subject", "Keyword", "Place (Topic)", "Time period (Topic)", "Material", 
"Rights statement", "Rights note", "Rights holder", "License", "Access rights", "Permanent link"]
liTagList = ["attribute attribute-alternative_title",
"attribute attribute-resource_type", "attribute attribute-creator", "attribute attribute-contributor", "attribute attribute-work_type",
"attribute attribute-language", "attribute attribute-publisher", "attribute attribute-date_created", "attribute attribute-date_issued",
"attribute attribute-date_copyrighted", "attribute attribute-abstract", "attribute attribute-description", "attribute attribute-staff_notes",
"attribute attribute-format", "attribute attribute-extent", "attribute attribute-measurement", "attribute attribute-based_near_label",
"attribute attribute-collection_name", "attribute attribute-sub_collection", "attribute attribute-source", "attribute attribute-provenance",
"attribute attribute-related_finding_aid", "attribute attribute-related_url", "attribute attribute-identifier", "attribute attribute-call_number",
"attribute attribute-collection_identifier", "attribute attribute-archival_context", "attribute attribute-bibliographic_citation",
"class='attribute attribute-subject", "attribute attribute-keyword", "attribute attribute-spatial", "attribute attribute-temporal",
"attribute attribute-material", "attribute attribute-rights_statement", "attribute attribute-rights_note", "attribute attribute-rights_holder",
"attribute attribute-license", "attribute attribute-access_rights", "attribute attribute-handle"]

## open csv file and read handler link, store in a list
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

## find object title and handler, then store it into a list
# @param    source
#           html page that has been parsed by beautifulsoup
# @param    valueList
#           a list contain contents in each <li> tag, in here we just need to add item's title
def findObjectTitle(source, valueList):
    value = ""
    # delete front/back whitespace and add to valueList
    tag = source.find('title')
    value += tag.string.split("|", 3)[1]
    valueList.append(value[1:len(value) - 1])
    value = ""

## find and store all contents of desired <li> tags according to categoryList
# @param    source
#           html page that has been parsed by beautifulsoup
# @param    liTagList
#           a list contain 'class' attribution in <li> tag, use it to find correct <li> tag and its content
# @param    valueList
#           a list to store scraped attrs' value
# @param    writer
#           csv file writer for output
def findCategoryValue(source, liTagList, valueList, writer):
    content = ""
    for liTag in liTagList:
        result = source.findAll('li', attrs={'class': liTag})
        # use ; to isolate multiple li tag contents
        if len(result) > 1:
            while len(result) > 0:
                if result[0] is not None:
                    rawContent = result[0].text
                    index = rawContent.find('\r\n')
                    if index != -1:
                        content += rawContent[:index]
                    else:
                        content += rawContent    
                    content += '|'
                    result.pop(0)
            valueList.append(content[:len(content)-1])        
            content = ""
        elif len(result) == 1:
            valueList.append(result[0].text)
        else:
            valueList.append("null")
    writer.writerow(valueList)

def main():
    categoryValue = []
    itemURL = []
    # iterator to show program progress
    i = 1
    # get inputfile
    print("Please enter csv file name. The file must in the same folder with your main.py program: ")
    fileIn = input()
    # write csv
    print("Please enter output file name: ")
    fileOut = input()
    try:
        itemURL = readCSV(fileIn)
    except:
        print("Fail to open this file. Press enter to exit.")
        key = input()
        sys.exit()
    numOfURL = len(itemURL)
    print("There are ", numOfURL, " records in the input file.")
    # open file for output
    outFile = open(fileOut, 'w', encoding = 'utf8', newline='')
    csvWriter = csv.writer(outFile)
    csvWriter.writerow(categoryList)
    for urlLink in itemURL:
        html = urllib.request.urlopen(urlLink)
        # load target digital collection in html parser
        soup = BeautifulSoup(html, 'html.parser', from_encoding = 'utf-8')
        # find collection title
        findObjectTitle(soup, categoryValue)
        # find original hdl link
        categoryValue.append(urlLink)
        # find attributes value
        findCategoryValue(soup, liTagList, categoryValue, csvWriter)
        print("We have successfully web-scraped ", i, " / ", numOfURL, " records")
        # reset categoryValue for next collection
        categoryValue = []
        i = i + 1
    # write into csv
    outFile.close()
    print("The program is finished. The output file is: ", fileOut, " . It is located in the same folder with your main.py program. Press enter to exit.")
    key = input()
    sys.exit()
    
if __name__ == "__main__":
    main()
