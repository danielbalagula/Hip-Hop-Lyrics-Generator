import sys
from songs import *
from lyric_formatter import *
from lyric_extractor import *
import random

debug = "--debug" in sys.argv
no_exceptions = "--no_exceptions" in sys.argv
no_markov = "--no_markov" in sys.argv

if no_exceptions:
	exceptions = []
else:
	exceptions = ["IN","DT"]

artists = []
all_song_tokens = []
all_song_lyrics = ""

#randomness = float((10-int(raw_input("How jumbled would like your lyrics to be? (0-10): "))))/10
randomness = 0

def pre_process():
	global all_song_lyrics
	artists_info = get_artists()
	for artist_info in artists_info:
		artists.append(Artist(artist_info))
	for artist in artists:
		songs = get_songs(artist.name)
		for song in songs:
			current_song = Song(song, artist.name)
			artist.add_song(current_song)
			current_song.lyrics = format_lyrics(get_lyrics(current_song.url, artist.name, current_song.title).replace("\n"," EOL "))
			all_song_lyrics = all_song_lyrics + current_song.lyrics
		all_song_lyrics = all_song_lyrics + " ENDOFARTIST "
			
	all_song_tokens = nltk.pos_tag(nltk.word_tokenize(unicode(all_song_lyrics, 'utf-8')))

	i=1
	for artist in artists:
		s=0
		current_line = []
		for token in all_song_tokens:
			if (token[0] == "EOL"):
				artist.songs[s].add_line(current_line, j)
				j=j+1
				current_line = []
			elif token[0] == "ENDOFSONG":
				j=0
				s=s+1
				current_line = []
			elif token[0] == "ENDOFARTIST":
				break;
			elif token[0] != "STARTOFSONG":
				j=0	
				current_line.append(token)						

def process():
	global debug
	print "\nLyrics:\n"
	for i in range(1,25):
		line = get_random_line(i)
		line_structure = line.contents
		new_line = ["" for x in range(len(line_structure))]
		new_line_string = ""
		for p in range(0,len(line_structure)):
			if new_line[p] == "":
				word = check_exceptions(p, line_structure[p][1], line_structure);
				if word == "":
					word = get_word(new_line[p-1], line_structure[p][1], num_syllables(word));
					repeated_positions = check_repetitions(p, line);
					for position in repeated_positions:
						if new_line[int(position)] == "":
							new_line[int(position)] = word
				else:
					new_line[p] = word
		for word in new_line:
			if word == "I":
				new_line_string += " I"
			elif word != ".":
				new_line_string += " " + word.lower()
			else:
				new_line_string += word
		new_line_string = new_line_string[1:2].upper() + new_line_string[2:]
		print new_line_string
			
def get_random_line(i):
	artist = random.choice(artists)
	song = random.choice(artist.songs)
	while len(song.lines) < i+1:
		#print "stuick here"
		song = random.choice(artist.songs)
	line = song.lines[i]
	return line

def check_exceptions(position, token_type, line):
	global exceptions
	if token_type in exceptions:
		return line[position][0]
	elif position == 0:
		return random.choice(possible_words[line[position][1]])
	else:
		return ""

def get_word(previous_word, token_type, num_syllables):
	global no_markov
	if possible_word_followups[previous_word] and not no_markov:
		word_followups = possible_word_followups[previous_word]
		pos_used = possible_words[token_type]
		same_syllables = syllable_list[str(num_syllables)]
		word_i_pos = list(set(word_followups) & set(pos_used))
		word_i_pos_i_syl = list(set(word_i_pos) & set(same_syllables))
		if word_i_pos_i_syl:
			return random.choice(word_i_pos_i_syl)
		elif word_i_pos:
			return random.choice(word_i_pos)
		else:
			return random.choice(word_followups)
	else:
		return random.choice(possible_words[token_type])

def check_repetitions(position, structure):
	repeated_positions = structure.repetitions[str(position)].split(",")
	return repeated_positions

pre_process()
process()