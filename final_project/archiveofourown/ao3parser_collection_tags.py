#!/usr/bin/python

# CPE 466 Fall 2015
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

from bs4 import BeautifulSoup

import os
import sys

path = '.'
relationships = {}
characters = {}
freeforms = {}
workCount = 0
workIDs = []

print("Parsing tags from all htm files in current directory.... ")
print("This may take a few minutes")

for file in os.listdir(path):
   current = os.path.join(path, file)
   if current[-3:] == "htm":
      with open(current) as openFile:
         soup = BeautifulSoup(openFile, 'html.parser')
         for link in soup.find_all('li', class_="work blurb group"):
            if str(link.get('id')[5:]) not in workIDs:
               workIDs.append(str(link.get('id')[5:]))
               workCount = workCount + 1
               for link_r in link.find_all('li', class_="relationships"):
                  if link_r.string.replace("\"", '').replace("\'",'') not in relationships:
                     relationships[link_r.string.replace("\"", '').replace("\'",'')] = 1
                  else:
                     count = relationships[link_r.string.replace("\"", '').replace("\'",'')]
                     relationships[link_r.string.replace("\"", '').replace("\'",'')] = count + 1

               for link_c in link.find_all('li', class_="characters"):
                  if link_c.string.replace("\"", '').replace("\'",'') not in characters:
                     characters[link_c.string.replace("\"", '').replace("\'",'')] = 1
                  else:
                     count = characters[link_c.string.replace("\"", '').replace("\'",'')]
                     characters[link_c.string.replace("\"", '').replace("\'",'')] = count + 1

               for link_f in link.find_all('li', class_="freeforms"):
                  if link_f.string.replace("\"", '').replace("\'",'') not in freeforms:
                     freeforms[link_f.string.replace("\"", '').replace("\'",'')] = 1
                  else:
                     count = freeforms[link_f.string.replace("\"", '').replace("\'",'')]
                     freeforms[link_f.string.replace("\"", '').replace("\'",'')] = count + 1

         print("%s - %d works processed so far" % (current, workCount))
         openFile.close()

print("All files processed")
print("Overall there were %d works." % (workCount))
print("---------------------")
threshold = workCount * 0.0005
if threshold < 1:
   threshold = 1
print("Removing tags that occurred in <= 0.5 percent of works, aka with count less than %d" % (threshold))

for key in list(relationships):
   if relationships[key] <= threshold:
      del relationships[key]
for key in list(characters):
   if characters[key] <= threshold:
      del characters[key]
for key in list(freeforms):
   if freeforms[key] <= threshold:
      del freeforms[key]

print("---------------------")
print("Relationships:")
print(relationships)
print("---------------------")
print("Character tags:")
print(characters)
print("---------------------")
print("Freeform tags:")
print(freeforms)
print("---------------------")
print("Number relationship tags: %d" % (len(relationships)))
print("Number character tags: %d" % (len(characters)))
print("Number freeform tags: %d" % (len(freeforms)))
print("---------------------")
print("Generating alltags.csv")

tagfile = open("alltags.csv", 'w')
tagfile.write("id,name,type,count\n")
tagid = 0
ids = []
for tag in relationships:
   tagfile.write(str(tagid) + ',\"' + tag.replace("\"", '').replace("\'",'') + '\",\"Relationship\",' + str(relationships[tag]) + '\n')
   tagid +=1
   ids.append(tag.replace("\"", '').replace("\'",''))
for tag in characters:
   tagfile.write(str(tagid) + ',\"' + tag.replace("\"", '').replace("\'",'') + '\",\"Character\",' + str(characters[tag]) + '\n')
   tagid +=1
   ids.append(tag.replace("\"", '').replace("\'",''))
for tag in freeforms:
   tagfile.write(str(tagid) + ',\"' + tag.replace("\"", '').replace("\'",'') + '\",\"Freeform\",' + str(freeforms[tag]) + '\n')
   tagid +=1
   ids.append(tag.replace("\"", '').replace("\'",''))
tagfile.close()


#print(ids)

print("Generating \"market baskets\" for fanwork tags as alldatai.csv ..... this may take a few minutes")

datafile = open("alldata-out1.csv", 'w')
processedIDs = []
for file in os.listdir(path):
   current = os.path.join(path, file)
   if current[-3:] == "htm":
      with open(current) as openFile:
         soup = BeautifulSoup(openFile, 'html.parser')
         for link in soup.find_all('li', class_="work blurb group"):
            toWrite = ''
            toWrite += str(link.get('id')[5:])
            if str(link.get('id')[5:]) not in processedIDs:
               processedIDs.append(str(link.get('id')[5:]))
               for link_r in link.find_all('li', class_="relationships"):
                  text = link_r.string.replace("\"", '').replace("\'",'')
                  if text in ids:
                     toWrite += ',' + str(ids.index(text))

               for link_c in link.find_all('li', class_="characters"):
                  text = link_c.string.replace("\"", '').replace("\'",'')
                  if text in ids:
                     toWrite += ',' + str(ids.index(text))

               for link_f in link.find_all('li', class_="freeforms"):
                  text = link_f.string.replace("\"", '').replace("\'",'')
                  if text in ids:
                     toWrite += ',' + str(ids.index(text))

            #print(toWrite)
            # this ensures that only works with applicable tags get processed
               if len(toWrite) > len(str(link.get('id'[5:]))):
                  toWrite += "\n"
                  datafile.write(toWrite)

print("Done!")
print("---------------------")

datafile.close()

