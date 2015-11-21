#! /usr/local/bin/python3

# CPE 466 Fall 2015
# Lab 4: Supervised Learning
# Jeff McGovern - jmcgover@calpoly.edu
# Nicole Martin - nlmartin@calpoly.edu

import errno
import os
import sys

import xml.etree.ElementTree as ElementTree
from xml.etree.ElementTree import Element

from xml.dom import minidom

def main():
   attributes = Element('domain')
   # Party
   party = ElementTree.SubElement(attributes, 'node')
   democratic = ElementTree.SubElement(party, 'edge')
   republican = ElementTree.SubElement(party, 'edge')
   independent = ElementTree.SubElement(party, 'edge')

   party.set('var', 'Party')
   democratic.set('var', 'Democratic')
   democratic.set('num', '1')
   republican.set('var', 'Republican')
   republican.set('num', '2')
   independent.set('var', 'Independent')
   independent.set('num', '3')

   # Ideology
   ideology = ElementTree.SubElement(attributes, 'node')
   liberal = ElementTree.SubElement(ideology, 'edge')
   conservative = ElementTree.SubElement(ideology, 'edge')
   moderate = ElementTree.SubElement(ideology, 'edge')

   ideology.set('var','Ideology')
   liberal.set('var', 'Liberal')
   liberal.set('num', '1')
   conservative.set('var', 'Conservative')
   conservative.set('num', '2')
   moderate.set('var', 'Moderate')
   moderate.set('num', '3')

   # Race
   race = ElementTree.SubElement(attributes, 'node')
   race.set('var','Race')
   black = ElementTree.SubElement(race, 'edge')
   black.set('var','Black')
   black.set('num','1')
   white = ElementTree.SubElement(race, 'edge')
   white.set('var','White')
   white.set('num','2')
   other = ElementTree.SubElement(race, 'edge')
   other.set('var','Other')
   other.set('num','3')

   # Gender
   gender = ElementTree.SubElement(attributes, 'node')
   gender.set('var','Gender')
   male = ElementTree.SubElement(gender, 'edge')
   male.set('var','Male')
   male.set('num','1')
   female = ElementTree.SubElement(gender, 'edge')
   female.set('var','Female')
   female.set('num','2')

   # Religion
   religion = ElementTree.SubElement(attributes, 'node')
   religion.set('var','Religion')
   protestant = ElementTree.SubElement(religion, 'edge')
   protestant.set('var','Protestant')
   protestant.set('num','1')
   catholic = ElementTree.SubElement(religion, 'edge')
   catholic.set('var','Catholic')
   catholic.set('num','2')
   other = ElementTree.SubElement(religion, 'edge')
   other.set('var','Other')
   other.set('num','3')

   # Income
   income = ElementTree.SubElement(attributes, 'node')
   income.set('var','Income')
   less30000 = ElementTree.SubElement(income, 'edge')
   less30000.set('var','Less than 30000')
   less30000.set('num','1')
   from30000_49999 = ElementTree.SubElement(income, 'edge')
   from30000_49999.set('var','30000-49999')
   from30000_49999.set('num','2')
   from50000_74999 = ElementTree.SubElement(income, 'edge')
   from50000_74999.set('var','50000-74999')
   from50000_74999.set('num','3')
   from75000_99999 = ElementTree.SubElement(income, 'edge')
   from75000_99999.set('var','75000-99999')
   from75000_99999.set('num','4')
   from100000_149999 = ElementTree.SubElement(income, 'edge')
   from100000_149999.set('var','100000-149999')
   from100000_149999.set('num','5')
   over150000 = ElementTree.SubElement(income, 'edge')
   over150000.set('var','150000+')
   over150000.set('num','6')

   # Education
   education = ElementTree.SubElement(attributes, 'node')
   education.set('var','Education')
   hs = ElementTree.SubElement(education, 'edge')
   hs.set('var','H.S. diploma or less')
   hs.set('num','1')
   college = ElementTree.SubElement(education, 'edge')
   college.set('var','College')
   college.set('num','2')
   post_grad = ElementTree.SubElement(education, 'edge')
   post_grad.set('var','Post-Grad')
   post_grad.set('num','3')

   # Age
   age = ElementTree.SubElement(attributes, 'node')
   age.set('var','Age')
   from18_29 = ElementTree.SubElement(age, 'edge')
   from18_29.set('var','18-29')
   from18_29.set('num','1')
   from30_44 = ElementTree.SubElement(age, 'edge')
   from30_44.set('var','30-44')
   from30_44.set('num','2')
   from45_64 = ElementTree.SubElement(age, 'edge')
   from45_64.set('var','45-64')
   from45_64.set('num','3')
   over65 = ElementTree.SubElement(age, 'edge')
   over65.set('var','65+')
   over65.set('num','4')

   # Region
   region = ElementTree.SubElement(attributes, 'node')
   region.set('var','Region')
   northeast = ElementTree.SubElement(region, 'edge')
   northeast.set('var','Northeast')
   northeast.set('num','1')
   south = ElementTree.SubElement(region, 'edge')
   south.set('var','South')
   south.set('num','2')
   midwest = ElementTree.SubElement(region, 'edge')
   midwest.set('var','Midwest')
   midwest.set('num','3')
   west = ElementTree.SubElement(region, 'edge')
   west.set('var','West')
   west.set('num','4')

   # Bush Approval
   bush_approval = ElementTree.SubElement(attributes, 'node')
   bush_approval.set('var','BushApproval')
   approve = ElementTree.SubElement(bush_approval, 'edge')
   approve.set('var','Approve')
   approve.set('num','1')
   disapprove = ElementTree.SubElement(bush_approval, 'edge')
   disapprove.set('var','Disapprove')
   disapprove.set('num','2')

   vote = ElementTree.SubElement(attributes, 'node')
   vote.set('var','Vote')
   obama = ElementTree.SubElement(vote, 'edge')
   obama.set('var','Obama')
   obama.set('num','1')
   mccain = ElementTree.SubElement(vote, 'edge')
   mccain.set('var','McCain')
   mccain.set('num','2')

   #ElementTree.dump(attributes)
   xmlstr = minidom.parseString(ElementTree.tostring(attributes)).toprettyxml(indent='   ')
   print(xmlstr)
   return 0

if __name__ == '__main__':
   rtn = main()
   sys.exit(rtn)
