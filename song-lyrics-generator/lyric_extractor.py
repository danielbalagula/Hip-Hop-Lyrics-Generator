import requests
import bs4
import random
import sys

def find_between(s, first, last):
    try:
        start = s.index(first) + len(first)
        end = s.index(last, start)
        return s[start:end]
    except ValueError:
        return ""

def get_artists():

	artist_list = []
	for i in range(1,len(sys.argv)):
		if "--" not in sys.argv[i]:
			artist_list.append(sys.argv[i])
		else:
			break

	return artist_list

def get_songs(artist_name):

	intro = random.choice(["Adding a dash of ", "Sprinkling some of ", "Glazing some of ", "Sweetening with a touch of "])
	url = 'http://www.metrolyrics.com/' + artist_name + '-lyrics.html'
	print (intro + artist_name + "'s most popular lyrics into the mix...")
	
	artist_page = requests.get(url)
	soup = bs4.BeautifulSoup(artist_page.content, "lxml")
	songs = []
	songs_data = soup.find_all("td")
	for song_data in songs_data:
		song_data_string = str(song_data)
		song = find_between(song_data_string, "http://www.metrolyrics.com/", "-lyrics-" + artist_name + ".html" )
		songs.append(song)

	songs = filter(None, songs)

	return songs

def get_lyrics(song_url, artist_name, song_name):

	song_page = requests.get(song_url)
	soup = bs4.BeautifulSoup(song_page.content, "lxml")
	lyrics = soup.find_all("p", class_='verse')
	str_lyrics = " STARTOFSONG "
	for verse in lyrics:
		verse = str(verse)
		find_artist = find_between(verse, "\"verse\">[", "]" ).lower()
		if artist_name.replace("-", " ") in find_artist or find_artist == "" or ("verse" in find_artist and ":" not in find_artist):
			verse = verse.replace("<p class=\"verse\">", "")
			verse = verse.replace("<br/>", ".")
			verse = verse.replace("?", "")
			verse = verse.replace("!", "")
			verse = verse.replace("</p>", ".")
			extras = find_between(verse, "(", ")" )
			while (extras != ""):
				verse = verse.replace("(" + extras + ")", "")
				extras = find_between(verse, "(", ")" )
			str_lyrics = str_lyrics + verse
	str_lyrics = str_lyrics + " ENDOFSONG  "
	return str_lyrics