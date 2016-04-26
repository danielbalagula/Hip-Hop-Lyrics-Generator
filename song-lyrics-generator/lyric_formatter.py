import re

def format_lyrics(lyrics):
	lyrics = re.sub(r"\.(?=[a-zA-Z])", ". ", lyrics)
	lyrics = re.sub(r"n'\s", "ng ", lyrics)
	lyrics = re.sub(r"tryna", "trying to", lyrics)
	lyrics = re.sub(r"I'?mma", "I'm going to", lyrics)
	lyrics = re.sub(r"I wanna", "I want to", lyrics)
	lyrics = re.sub(r"s?he wanna", "she wants to", lyrics)
	lyrics = re.sub(r"needa", "I need to", lyrics)
	lyrics = re.sub(r'\ba\b(?=\s+[aeiouAEIOU])', 'an', lyrics)
	lyrics = re.sub(r'\ban\b(?=\s+[bcdfghjklmnpqrstvwxyzBCDFGHJKLMNPQRSTVWXYZ])', 'a', lyrics)
	lyrics = re.sub(r",", "", lyrics)
	lyrics = re.sub(r";", "", lyrics)
	return lyrics