import urllib.request
import csv
from bs4 import BeautifulSoup

categoryValue = []
tagList = []
itemURL = []
# Contain all category name a collection probably has in DC.
# Add/Delete keywords in the list to create new csv w/ more/less category. Don't forget to delete corresponding liTag!
# Follow the format when changthis list.
categoryList = ["Title", "Permanent link", "Alternative title", "Resource Type", "Creator","Contributor", "Genre", "Language",
"Publisher", "Date created", "Date issued", "Date copyrighted", "Summary", 
"Description", "Staff notes", "Format", "Extent", "Measurements", "Repository",
"Collection", "Sub collection", "Source", "Provenance", "Related finding aid",
"Related URL", "Identifier", "Call number", "Collection identifier", "Archival context",
"Published in", "Subject", "Keyword", "Place (Topic)", "Time period (Topic)", "Material"
"Rights statement", "Rights note", "Rights holder", "License", "Access rights",
"Preservation level", "Preservation level rationale", "Preservation level date assigned"]
liTagList = ["attribute attribute-handle", "attribute attribute-alternative_title",
"attribute attribute-resource_type", "attribute attribute-creator", "attribute attribute-contributor", "attribute attribute-work_type", "attribute attribute-language", "attribute attribute-publisher", "attribute attribute-date_created", "attribute attribute-date_issued", "attribute attribute-date_copyrighted", "attribute attribute-abstract", "attribute attribute-description", "attribute attribute-staff_notes", "attribute attribute-format", "attribute attribute-extent", "attribute attribute-measurement", "attribute attribute-based_near_label", "attribute attribute-collection_name", "attribute attribute-sub_collection", "attribute attribute-source", "attribute attribute-provenance", "attribute attribute-related_finding_aid", "attribute attribute-related_url", "attribute attribute-identifier", "attribute attribute-call_number", "attribute attribute-collection_identifier", "attribute attribute-archival_context", "attribute attribute-bibliographic_citation", "class='attribute attribute-subject", "attribute attribute-keyword", "attribute attribute-spatial", "attribute attribute-temporal", "attribute attribute-material", "attribute attribute-rights_statement", "attribute attribute-rights_note", "attribute attribute-rights_holder", "attribute attribute-license", "attribute attribute-access_rights", "attribute attribute-preservation_level", "attribute attribute-preservation_level_rationale", "attribute attribute-preservation_level_date_assigned"]
#get inputfile
print("Please enter csv file name: ")
fileIn = input()
# write csv
print("Please enter output file name: ")
fileOut = input()
outFile = open(fileOut, 'w')
csvWriter = csv.writer(outFile)
csvWriter.writerow(categoryList)
# open csv file and read handler link, store in a list
def readCSV(csvName):
  inFile = open(csvName, 'r')
  csvReader = csv.reader(inFile, delimiter=',')
  for row in csvReader:
    itemURL.append(row[1])
  # del the column name read for first line
  itemURL.pop(0)
# find object title
def findObjectTitle():
  value = ""
  # delete front/back whitespace
  for tag in soup.findAll('title'):
    value += tag.string.split("|", 3)[1]
    categoryValue.append(value[1:len(value)-1])
    value = ""
# find all category value according to categoryList
def findCategoryValue(LiTagList, csvWriter):
  content = ""
  for liTag in liTagList:
    result = soup.findAll('li', attrs={'class': liTag})
    # use ; to isolate multiple li tag contents
    if len(result) > 1:
      while len(result) > 0:
        if result[0] is not None:
          content += result[0].string
          content += '; '
          result.pop(0)
      categoryValue.append(content[:len(content)-2])
      content = ""
    elif len(result) == 1:
      categoryValue.append(result[0].string)
    else:
      categoryValue.append("None")
  csvWriter.writerow(categoryValue)

# iterator to show progress
i = 1
readCSV(fileIn)
for urlLink in itemURL:
  html = urllib.request.urlopen(urlLink)
  # load target digital collection in html parser
  soup = BeautifulSoup(html, 'html.parser')
  # find collection title
  findObjectTitle()
  # find attributes value
  findCategoryValue(liTagList, csvWriter)
  # reset categoryValue for next collection
  categoryValue = []
  print("We have successfully web-scraped ", i, " records")
  i = i + 1
# write into csv
outFile.close()
