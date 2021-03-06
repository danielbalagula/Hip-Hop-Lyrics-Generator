﻿import nltk
from nltk.corpus import cmudict
from collections import defaultdict

d = cmudict.dict()

possible_words = defaultdict(list)
possible_word_followups = defaultdict(list)
syllable_list = defaultdict(list)
followup_frequency = {}

def num_syllables(word):
	if (word in d):
		length = [len(list(y for y in x if y[-1].isdigit())) for x in d[word.lower()]]
		return length

class Artist:
	def __init__(self, n):
		self.name = n
		self.songs = []

	def add_song(self, s):
		self.songs.append(s)

class Song:
	def __init__(self, n, a):
		self.lyrics = ""
		self.length = 0
		self.lines = []
		self.artist = a
		self.title = n
		self.url = 'http://www.metrolyrics.com/' + self.title + '-lyrics-' + a + '.html'

	def add_line(self, l, n):
		self.lines.append(Line(l,n))
		self.length += 1

class Line:
	def __init__(self, l, n):
		self.line_number = n
		self.contents = l
		self.repetitions = {}
		i=0
		for index, token in enumerate(self.contents):
			if int(index) < len(self.contents)-1:
				next_token_pos = self.contents[index+1][0]
			else:
				next_token_pos = " "
			token_syl = str(num_syllables(token[0]))
			
			if (token[0] not in syllable_list[token_syl]):
				syllable_list[token_syl].append(token[0])
			if (token[0] not in possible_words[token[1]]):
				possible_words[token[1]].append(token[0])
			if next_token_pos not in possible_word_followups[token[0]]:
				possible_word_followups[token[0]].append(next_token_pos)
				followup_frequency[token[0]+"->"+next_token_pos] = 1
			elif not next_token_pos == " ":
				followup_frequency[token[0]+"->"+next_token_pos] += 1
			
			found = False
			if bool(self.repetitions):
				for key in self.repetitions:
					occurences = self.repetitions[key].split(',')
					if self.contents[int(occurences[0])][0] == token[0]:
						found = True
						self.repetitions[key] = self.repetitions[key] + "," + str(i)
						self.repetitions[str(i)] = str(i) + "," + key
						break
			if not found:
				self.repetitions[str(i)] = str(i)
			i=i+1