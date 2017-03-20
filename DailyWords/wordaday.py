import json
import os
import urllib2
from flask import Flask
from bs4 import BeautifulSoup
from django.utils.encoding import smart_str, smart_unicode
import unicodedata
import sys

path_file = os.path.abspath("")

def CollectWord():
	#save file strings
	dayString = ['TodaysWord','YesterdaysWord']
	#Getting the urls of the previous days words. /word-of-the-day/#word#-2015-12-29 format
	urls = get_URLs()
	#Extracting the date from the urls
	getStringDates = getDates(urls)
	# Looping through and writting todays and Yesterdays word
	for x in range (0,len(dayString)+len(getStringDates)):
		if x < 2:
			#get the attributes to the words
			word,syllables,Definitions,Examples = run(urls[x])
			archive = False
			print word
			jsonize_word(word,syllables,Definitions,Examples,dayString[x],archive)
			#This is for the archive , where the file is appended not overwritten
			if x==0:
				archive = True
				word,syllables,Definitions,Examples = run(urls[x])
				jsonize_word(word,syllables,Definitions,Examples,dayString[x],archive)
		else:
			
			# Looping through and writing the words for specific dates
			word,syllables,Definitions,Examples = run(urls[x])
			jsonize_previousWords(word,syllables,Definitions,Examples,getStringDates[x-2])
	deleteExtraFile(getStringDates)
	print 'Program-end'
	

def getDates(urls):
	#extracting the dates from the url list
	dateList = []
	for x in range(1,len(urls)-1):
		newString = ''
		for y in range(len(urls[x])-10,len(urls[x])):
			newString = newString + urls[x][y]
		dateList.append(newString)
	#removing yesterdays date
	dateList.pop(0)
	return dateList	
	

def get_URLs():
	urls = []
	soup = getPage('http://www.merriam-webster.com/word-of-the-day')
	for url in soup.find_all('a'):
		if url.get('href').find('/word-of-the-day/') != -1:
			urls.append(url.get('href'))
		else:
			pass
	for x in range(0,len(urls)):
		urls[x] = 'http://www.merriam-webster.com' + urls[x]
	
	del urls[0] 
	
	FirstLink = 'http://www.merriam-webster.com/word-of-the-day'
	urls = [FirstLink]+ urls
	return urls

def run(url):
	soup = getPage(url)
	word = getWord(soup)
	syllables = getSyllables(soup)
	Definitions = getDefinition(soup)
	Examples = getExample(soup)
	return (word,syllables,Definitions,Examples)

def getPage(URL):
	content = urllib2.urlopen(URL).read()
	soup = BeautifulSoup(content)
	return soup


def getWord(soup):
	word = soup.find('h1')
	word = word.getText()
	return word


def getSyllables(soup):
	Syllables = soup.find("span", class_="word-syllables").getText()
	return Syllables


def get_contents(soup):
	tag_content = soup.h2.find_all_next("p")
	counter = 0
#All <p> turned from object to unicode
	for x in range(0,len(tag_content)):
		tag_content[x] = tag_content[x].get_text()
		try:
			tag_content[x] = str(tag_content[x])
		except UnicodeEncodeError:
			tag_content[x] = unicodedata.normalize('NFKD',tag_content[x]).encode('ascii','ignore')
#This is the part that cuts the list down to what we need
	for x in range(0,len(tag_content)-20):
		if tag_content[x].find('Learn a new word every day') != -1:
			counter = x
		else:
			pass
	return (tag_content,counter)


def removeLetters(list,itemToRemove,itemToAdd):
	for i in range(0,len(list)):
		list[i] = list[i].replace(itemToRemove,itemToAdd) 
	return list

#Definition Method
def getDefinition(soup):
	tag_content,counter= get_contents(soup) 
	Definitions = []
	for i in range(0,counter-2):
		Definitions.append(tag_content[i])
	Definitions = removeLetters(Definitions,':','-')
	return Definitions


def getExample(soup):
	tag_content,counter= get_contents(soup) 
	Examples = []
	for i in range(counter-2,counter):
		Examples.append(tag_content[i])
	Examples = removeLetters(Examples,':','-')
	Examples = removeLetters(Examples,'"','')
	return Examples


def jsonize_word(word,syllables,Definitions,Examples,fileName,archive):
	remove = '"'
	add = ''
	#Absolute path to file
	filename = path_file+'/'+fileName+'.json'
	written = 'w'
	#change the way that the file is written in
	if archive == True:
		written = 'ab+'
		filename = path_file+'/archive.json'
	target = open(filename, written)
	definition = ''
	for x in range(0,len(Definitions)):
		if x==len(Definitions)-1:
			definition = definition + '\n \t"Definition' + str(x+1) + '": "' + Definitions[x] + '",'
		else:
			definition = definition + '\n \t"Definition' + str(x+1) + '": "' + Definitions[x] + '",' 
	example = ''
	for x in range(0,len(Examples)):
		if x==len(Examples)-1:
			example = example + '\n \t"example' + str(x+1) + '": "' + Examples[x] + '"'
		else:
			example = example + '\n \t"example' + str(x+1) + '": "' + Examples[x] + '", ' 
	jsoned = '{\n' + '\t"word": "' + word + '",' + '\n \t"syllables":"' +syllables + '",' + definition + ''+ example +'\n}'
	target.seek(0, 0)
	target.write('\n')
	target.write(jsoned)	
	target.close()


def jsonize_previousWords(word,syllables,Definitions,Examples,fileName):
	filename = path_file+'/Dates/'+fileName+'.json'
	target = open(filename, 'w')
	definition = ''
	for x in range(0,len(Definitions)):
		if x==len(Definitions)-1:
			definition = definition + '\n \t"Definition' + str(x+1) + '": "' + Definitions[x] + '",'
		else:
			definition = definition + '\n \t"Definition' + str(x+1) + '": "' + Definitions[x] + '",' 
	example = ''
	for x in range(0,len(Examples)):
		if x==len(Examples)-1:
			example = example + '\n \t"example' + str(x+1) + '": "' + Examples[x] + '"'
		else:
			example = example + '\n \t"example' + str(x+1) + '": "' + Examples[x] + '", ' 
	jsoned = '{\n' + '\t"word": "' + word + '",' + '\n \t"syllables":"' +syllables + '",' + definition + ''+ example +'\n}'
	target.write(jsoned)	
	target.close()


def deleteExtraFile(getStringDates):
	#files that exits . Only one file will be deleted
	FilesInDirectory = []
	delete = []
	p_file = path_file + "/Dates/"
	# go through the dates and add on json, so we can compare them
	for x in range(0,len(getStringDates)):
		getStringDates[x] = getStringDates[x]+ '.json'
	# go through the folder and add to the list the names of the file
	
	for file in os.listdir(p_file):
	    if file.endswith(".json"):
	        FilesInDirectory.append(file)
	#differece between the file add to a new file. Should only be one
	delete = list(set(FilesInDirectory) - set(getStringDates))
	try:
		#add the extension file to the file 
		for a in range(0,len(delete)):
			delete[a] = p_file + delete[a]
			#delete the file
			os.remove(delete[a])	 
	except NameError:
		print 'No Change in file'

		
CollectWord()

