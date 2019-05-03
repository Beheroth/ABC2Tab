import re
from time import sleep
from Converter import Converter
from Chord import Chord
from Song import Song

abc = open("resources/Test.abc", 'r')
pattern = re.compile(r'(.): (.+)')
header = {}
chords = []
converter = Converter()

header_context = True
for line in abc:
    if header_context:
        try:
            match = pattern.match(line)
            #macth headers
            header[match.group(1)] = match.group(2)
        except:
            header_context = False
            print("Header endend:" + str(header))
    if not(header_context):
        #split lines
        s_chords = line.split(' ')
        #create chords list
        for s_chord in s_chords:
            chords.append(Chord(s_chord))
abc.close()

song = Song(header, chords)
song.eval_tquantum()
#print("Chords: %s" % (song.chords))
converter.convert_song(song)

"""
def parse_header(pattern, line, header):
    answer = False
    match = pattern.match(line)
    if match != None:
        values = match.groups()
        header[values[0]] = values[1]
        answer = True
    return answer

def parse_notes(pattern, line):
    notes = line.split(' ')
    for note in notes:
        match = pattern.match(note)
        if match != None:
            pass

    match = pattern.match(line)
    if match != None:
        values = match.groups()
        header[values[0]] = values[1]
    return header

"""
