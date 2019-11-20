import urllib.request
import csv
from bs4 import BeautifulSoup

# Contain all category name a collection probably has in DC.
# Add/Delete keywords in the list to create new .csv w/ more/less category. Don't forget to delete corresponding liTag!
# Follow the format when change this list.
categoryList = ["Title", "Permanent link", "Alternative title", "Resource Type", "Creator", "Contributor", "Genre", "Language",
"Publisher", "Date created", "Date issued", "Date copyrighted", "Summary",
"Description", "Staff notes", "Format", "Extent", "Measurements", "Repository",
"Collection", "Sub collection", "Source", "Provenance", "Related finding aid",
"Related URL", "Identifier", "Call number", "Collection identifier", "Archival context",
"Published in", "Subject", "Keyword", "Place (Topic)", "Time period (Topic)", "Material"
"Rights statement", "Rights note", "Rights holder", "License", "Access rights",
"Preservation level", "Preservation level rationale", "Preservation level date assigned"]
liTagList = ["attribute attribute-handle", "attribute attribute-alternative_title",
"attribute attribute-resource_type", "attribute attribute-creator", "attribute attribute-contributor", "attribute attribute-work_type", "attribute attribute-language", "attribute attribute-publisher", "attribute attribute-date_created", "attribute attribute-date_issued", "attribute attribute-date_copyrighted", "attribute attribute-abstract", "attribute attribute-description", "attribute attribute-staff_notes", "attribute attribute-format", "attribute attribute-extent", "attribute attribute-measurement", "attribute attribute-based_near_label", "attribute attribute-collection_name", "attribute attribute-sub_collection", "attribute attribute-source", "attribute attribute-provenance", "attribute attribute-related_finding_aid", "attribute attribute-related_url", "attribute attribute-identifier", "attribute attribute-call_number", "attribute attribute-collection_identifier", "attribute attribute-archival_context", "attribute attribute-bibliographic_citation", "class='attribute attribute-subject", "attribute attribute-keyword", "attribute attribute-spatial", "attribute attribute-temporal", "attribute attribute-material", "attribute attribute-rights_statement", "attribute attribute-rights_note", "attribute attribute-rights_holder", "attribute attribute-license", "attribute attribute-access_rights", "attribute attribute-preservation_level", "attribute attribute-preservation_level_rationale", "attribute attribute-preservation_level_date_assigned"]
# TODO  implement a file-read function that read <li> tag in, eliminate the need of a fixed list

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
        urlList.append(row[1])
    # del the column name read for first line
    urlList.pop(0)
    return urlList

# find object title and store it into a list
# @param    source
#           html page that has been parsed by beautifulsoup
# @param    valueList
#           a list contain contents in each <li> tag, in here we just need to add item's title
def findObjectTitle(source, valueList):
    value = ""
    # delete front/back whitespace
    for tag in source.findAll('title'):
        value += tag.string.split("|", 3)[1]
        valueList.append(value[1:len(value) - 1])
        value = ""

# find and store all contents of desired <li> tags according to categoryList
# @param    source
#           html page that has been parsed by beautifulsoup
# @param    liTagList
#           a list contain 'class' attribution in <li> tag, use it to find correct <li> tag and its content
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
          content += result[0].text
          content += '|'
          result.pop(0)
      valueList.append(content[:len(content)-1])
      content = ""
    elif len(result) == 1:
      valueList.append(result[0].text)
    else:
      valueList.append("null")
  valueList.pop()
  writer.writerow(valueList)

def main():
    categoryValue = []
    itemURL = []
    # iterator to show program progress
    i = 1
    # get inputfile
    print("Please enter csv file name: ")
    fileIn = input()
    # write csv
    print("Please enter output file name: ")
    fileOut = input()
    outFile = open(fileOut, 'w', encoding="utf-8", newline='')
    csvWriter = csv.writer(outFile)
    csvWriter.writerow(categoryList)
    itemURL = readCSV(fileIn)
    for urlLink in itemURL:
        html = urllib.request.urlopen(urlLink)
        # load target digital collection in html parser
        soup = BeautifulSoup(html, 'html.parser')
        # find collection title
        findObjectTitle(soup, categoryValue)
        # find attributes value
        findCategoryValue(soup, liTagList, categoryValue, csvWriter)
        print("We have successfully web-scraped ", i, " records")
        # reset categoryValue for next collection
        categoryValue = []
        i = i + 1
    # write into csv
    outFile.close()
    
if __name__ == "__main__":
    main()
