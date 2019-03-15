import re
from time import sleep
import json

class Chord:
    def __init__(self, s_chord):
        self.notes = {}
        self.parse_chord(s_chord)

    def __repr__(self):
        return str(self.notes)

    def parse_chord(self, s_chord):
        regex = r'([=_^]?)(([a-zA-Z])([,\'])?)(\d{0,1}\/?\d{1,2})'
        match = re.finditer(regex, s_chord)
        for note in match:
            self.notes[note.group(3)] = self.parse_time(note.group(5))

    def parse_time(self, s_time):
        regex = r'((\d{0,1})\/(\d{1,2}))|(\d{0,1})'
        match = re.match(regex, s_time)
        numerator = match.group(2)
        denominator = match.group(3)

        if numerator == "":
            numerator = 1

        if denominator == None:
            denominator = 1
            numerator = match.group(4)
        numerator = float(numerator)
        denominator = float(denominator)

        time = numerator / denominator
        print(s_time + " " + str(time))
        return time

    def getnotes(self):
        return self.notes.keys()

    def smallest(self):
        #find smallest unit of time in the chord
        smallest = min(list(self.notes.values()))
        return smallest


    """
    def getNotes(self):
        #import pdb; pdb.set_trace()
        regex = r'([=_^]?[a-zA-Z][,\']?\d?)\/(\d)'
        notes = []
        if self.notes[0] == '[':
            matches = re.finditer(regex, self.note, re.MULTILINE)
            for matchnum, match in enumerate(matches):
                notes += [match.group()]
        else:
            pattern = re.compile(regex)
            note = pattern.match(self.note)
            try:
                notes = [note.group(0)]
            except:
                pass
        return notes
    """

class Song:
    def __init__(self, header, chords):
        self.header = header
        self.chords = chords
        self.tquantum = None

    def eval_tquantum(self):
        quantums = []
        for chord in self.chords:
            if chord.smallest() in quantums:
                o = 0
            else:
                quantums.append(chord.smallest())
        #trouver le PGCD
        cur_gcp = 1
        for elem in quantums:
            cur_gcp = Song.gcp(cur_gcp, elem)

        #smallest = min(quantums)
        smallest = cur_gcp
        print("smallest is %s" % smallest)
        self.tquantum = smallest

    def getTicks(self):
        tics = []
        pos = 0
        for chord in self.chords:
            for note in chord.getnotes():
                tics.append((note, int(pos)))
            small_q = chord.smallest() 
            pos += small_q / self.tquantum
        return tics

    def ordTicks(self, tics):
        strings = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[]}
        for tic in tics:
            Slist = strings[tic[0]]
            Slist.append(tic[1])
        return strings

    def gcp(x, y):
        while y != 0:
            (x, y) = (y, x % y)
        return x

class Converter:

    def __init__(self):
        self.path = "resources/string_note_pos.json"
        self.convert_guitar_to_notes()


    def convert_guitar_to_notes(self):
        with open(self.path, "r") as read_file:
            self.guitar = json.load(read_file)
            data = self.guitar
        #print(data)
        notes = data["notes"]
        #print(notes)
        result = {}
        for note in notes:
            for guitar_string in range(1, 7):
                submap = data["guitar"][str(guitar_string)]
                try:
                    coord = (int(guitar_string), submap[note])
                    print(coord)
                    if (result.get(note)) is None:
                        result[note] = []
                    result[note].append(coord)
                except:
                    pass
        self.mapping = result
        with open('resources/result.json', "w") as write_file:
            json.dump(result, write_file)

    def convert_song(self, song):
        counter = float(0)
        output = []
        for chord in song.chords:
            output.append(self.lookup_chord(chord))

    def lookup_note(self, note):
        return self.mapping[note][0]

    def lookup_chord(selfself, chord):
        result = []
        for note in chord.notes:
            #result.append(lookup_note(self, note))
            pass



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
        #prune lines
        s_chords = line.split(' ')
        #create chords list
        for s_chord in s_chords:
            chords.append(Chord(s_chord))
abc.close()

song = Song(header, chords)
song.eval_tquantum()
("hello" + str(song.chords))


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