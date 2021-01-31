from nltk.chunk import ne_chunk
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize
from dataclasses import dataclass

import itertools
import wikipedia
import csv
import random
import re
import time

NA_LOCATION_FILE = './na_locations.csv'

with open(NA_LOCATION_FILE, newline='') as f:
	reader = csv.reader(f)
	NA_CITIES = list(reader)

@dataclass
class locQObject:
	line1: str
	line2: str
	options: list[str]
	solution: str

@dataclass
class perQObject:
	line1: str
	line2: str
	options: list[str] 
	solution: str

@dataclass
class dateQObject:
	line1: str
	line2: str
	options: list[int] 
	solution: int


def extract_ner(text: str):
	chunks = []
	tree = ne_chunk(pos_tag(word_tokenize(text)))
	for leaf in tree:
		if hasattr(leaf, 'label'):
			chunks.append([leaf.label(),' '.join(c[0] for c in leaf)])
	return chunks

def location_question(text: str):
	entity_list = extract_ner(text)

	for entity in entity_list:
		#Question Number 1. Location Generation
		if entity[0] == "GPE":
			options = [entity[1]]
			available_cities = NA_CITIES
			if [entity[1]] in NA_CITIES:
				available_cities.remove([entity[1]])

			total_cities = len(available_cities)

			city_numbers = random.sample(range(0, total_cities),3)

			for i in range(0,3):
				options.append(available_cities[city_numbers[i]][0])
			#Randomize the order of the options
			qaobject = locQObject("Fill in the blank!", text.replace(entity[1], "_______"), random.sample(options, len(options)), entity[1])
			return qaobject
	return False

def person_question(text: str):
	entity_list = extract_ner(text)
	for entity in entity_list:
		if (entity[0] == "PERSON" and (" " in entity[1])):
			options = []
			if options:
				options = [entity[1]]

			try:
				possible_names = extract_ner(wikipedia.page(entity[1]).content)
			except:
				return False

			for names in possible_names:
				if names[0] == "PERSON" and (names[1] not in entity_list) and (len(options) < 4) and " " in names[1]:
					options.append(names[1])
	if (len(options)==4):
		perquestion = perQObject("Fill in the blank!", text.replace(options[1], "_______"), options, options[1])
		perquestion.options = random.sample(options, len(options))
		return perquestion
	else:
		return False

def date_question(text: str):
	try:
		x = int(re.search('\d{4}', text).group())
		#if the time difference is less than 5 years, we need to apply a shift so the answers are not obviously wrong
		#future dates are not affected (in case there is sci-fi etc)
		if(time.localtime(time.time())[0] - x < 5 and time.localtime(time.time())[0] - x > 0):
			shift = time.localtime(time.time())[0] - x
			options = random.sample(list(range(x-10+shift-1, x - 1)),3)
		else:
			options = random.sample(list(range(x-5,x-1))+list(range(x+1,x+5)),3)
		options.append(x)
		datequestion = dateQObject("Fill in the blank!", text.replace(str(x), "_______"), options, x)
		return datequestion
	except:
		return False

def query(text: str):
	try:
		print(text)
		wiki_query = wikipedia.page(text)
		print(wiki_query.content)
	except Exception as e:
		print(e)


query("Scarlett Johansson")

'''
obama2 = "After graduating from Columbia University in 1983, he worked as a community organizer in Chicago"
question_1 = location_question(obama2)
print(question_1.line1)
print(question_1.line2)
print(question_1.options)
print(question_1.solution)

author = "Invented in 1891 by Canadian-American gym teacher James Naismith in Springfield, Massachusetts, United States, basketball has evolved to become one of the world's most popular and widely viewed sports"
question_2 = person_question(author)
print(question_2.line1)
print(question_2.line2)
print(question_2.options)
print(question_2.solution)

question_3 = date_question("The Mueller report, officially titled Report On The Investigation Into Russian Interference In The - Presidential Election, is the official report documenting the findings and conclusions of former Special Counsel Robert Mueller's investigation into Russian efforts to interfere in the - United States presidential election, allegations of conspiracy or coordination between Donald Trump's presidential campaign and Russia, and allegations of obstruction of justice.")
print(question_3.line1)
print(question_3.line2)
print(question_3.options)
print(question_3.solution)
'''