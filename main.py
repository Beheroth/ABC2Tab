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
        regex = r'([=_^]?\w[,\']?)(\d{0,1}\/?\d{1,2})?'
        match = re.finditer(regex, s_chord)
        for note in match:
            self.notes[note.group(1)] = self.parse_time(note.group(2))

    def parse_time(self, s_time):
        if s_time is None:
            s_time = '1'
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
        #print(s_time + " " + str(time))
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

    """
    def getTicks(self):
        tics = []
        pos = 0
        for chord in self.chords:
            for note in chord.getnotes():
                tics.append((note, int(pos)))
            small_q = chord.smallest() 
            pos += small_q / self.tquantum
        return tics
    """

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
                    #print(coord)
                    if (result.get(note)) is None:
                        result[note] = []
                    result[note].append(coord)
                except:
                    pass
        self.mapping = result
        with open('resources/result.json', "w") as write_file:
            json.dump(result, write_file)

    def convert_song(self, song):
        counter = 0
        output = []
        strings = {'1':[], '2':[], '3':[], '4':[], '5':[], '6':[]}
        chords = song.chords
        for chord in chords:
            output.append(self.lookup_chord(chord))
        print("Output: %s" % output)
        for i in range(len(output)):
            print("counter: %s" % counter)
            smallest = self.time_to_ticks(chords[i].smallest(), song)
            for key in output[i].keys():
                strings[key].append((output[i][key], counter + smallest))
            counter += smallest
        print(strings)
        return strings

    def isolate_tics(self, strings):
        for elem in strings:
            L = strings[elem]
            newL = []
            for note in L:
                newL += [note[1]]
            strings[elem] = newL
        return strings

    def time_to_ticks(self, time, song):
        return int(time//song.tquantum)

    def lookup_chord(self, chord):
        result = {}
        for note in chord.notes:
            if note != 'z':
                positions = self.lookup_note(note)
                #print("note %s: %s" % (note, positions))
                i = 0
                while(result.get(str(positions[i][0])) and i < len(positions)):
                    i += 1
                try:
                    result[str(positions[i][0])] = positions[i][1]
                except:
                    print("erreur, il n'y a pas de position pour jouer %s" %(note))
        return result

    def lookup_note(self, note):
        #return positions where you can play that note on the neck
        ans = None
        try:
            ans = self.mapping[note]
        except:
            print("couldn't find %s in the mapping" % (note))
        return ans



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
print("Chords: %s" % (song.chords))
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
