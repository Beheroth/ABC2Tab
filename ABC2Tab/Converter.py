import json
import re
from Chord import Chord
from Song import Song

class Converter:

    '''
        The Vehicle object contains lots of vehicles

        path: Path to the json file describing what notes can be played on the guitar.
        filepath: Path to the .abc file you want to convert for the robot.
        song: Song object created from the .abc file.
        left: output list designed for the left hand of the robot.
        right: output list designed for the right hand of the robot.
        mapping: Dictionary containing each playable note on the guitar. The note is the key, the positions are the value.
    '''

    def __init__(self, filepath):
        #self.path = "/home/pi/AGP/ABC2Tab/resources/string_note_pos.json"
        self.path = "resources/string_note_pos.json"
        self.convert_guitar_to_notes()
        self.filepath = filepath
        self.song = None

    def convert_guitar_to_notes(self):
        """
        Creates a map of all the available notes on the guitar and where to play them. The method use 'self.path' to create the map.
        """
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


    def convert_song(self):
        """
        Completes the self.right and self.left attributes.
        """
        self.read_file()
        song = self.song
        counter = 0
        output = []

        #the "strings" dictionnary is the best representation of a tablature.
        strings = {'1':[], '2':[], '3':[], '4':[], '5':[], '6':[]}
        self.left = {'1':[], '2':[], '3':[], '4':[], '5':[], '6':[]}
        self.right = {'1':[], '2':[], '3':[], '4':[], '5':[], '6':[]}
        chords = self.song.chords
        for chord in chords:
            output.append(self.lookup_chord(chord))
        #print("Output: %s" % output)
        for i in range(len(output)):
            #print("counter: %s" % counter)

            smallest = self.time_to_ticks(chords[i].smallest())
            for key in output[i].keys():
                strings[key].append((output[i][key], counter + smallest))
            counter += smallest
        for key, value in strings.items():
            self.left[key] = self.simplify_left(value)
            self.right[key] = self.simplify_right(value)

            #print("%s: %s" % (key, value))
            #print("Left: %s" % self.simplify_left(value))
            #print("Right: %s" % self.simplify_right(value))
        #print("Left: %s" % self.left)
        #print("Right: %s" % self.right)

    def read_file(self):
        """
        Translates the file into a song object and finds its tquantum.
        """
        filepath = self.filepath
        abc = open(filepath, 'r')
        header = {}
        chords = []

        pattern = re.compile(r'(.): (.+)')
        header_context = True
        for line in abc:
            if header_context:
                try:
                    match = pattern.match(line)
                    # macth headers
                    header[match.group(1)] = match.group(2)
                except:
                    header_context = False
                    print("Header endend:" + str(header))
            if not (header_context):
                # split lines
                s_chords = line.split(' ')
                # create chords list
                for s_chord in s_chords:
                    if(s_chord != ''):
                        chords.append(Chord(s_chord))
        abc.close()
        self.song = Song(header, chords)
        self.song.eval_tquantum()

    def time_to_ticks(self, time):
        return int(time//self.song.tquantum)

    def lookup_chord(self, chord):
        """
        Lookup where to play every note in the chord
        :param chord: Chord object containing notes.
        :return: dictionary where keys are the number of the string and values are the position on the string.
        """
        result = {}
        #print("--START: LookUp Chord: chord: %s:" % (chord.notes))
        for note in chord.notes:
            if note != 'z':
                positions = self.lookup_note(note)          #list of tuples
                #print("note %s: %s" % (note, positions))
                i = 0
                while(i < len(positions) and (str(positions[i][0])) in result):
                    i += 1
                try:
                    result[str(positions[i][0])] = positions[i][1] #{'1': 3}
                except:
                    print("Error, there is no position to play %s. i = %s" %(note, i))
        #print("--END: LookUp Chord: result: %s \n" % (result))
        return result

    def lookup_note(self, note):
        """
        :param note: string
        :return: list of tuples: positions where you can play that note on the guitar.
        """
        ans = None
        try:
            ans = self.mapping[note]
        except:
            ans = []
            print("couldn't find %s in the mapping" % (note))
        return ans

    def simplify_left(self, pos):
        ans = pos.copy()    #to avoid shallow copies
        i = 0
        while (i < len(ans) - 1):
            if (ans[i][0] == ans[i+1][0]):
                ans.pop(i)
            else:
                i += 1
        return ans

    def simplify_right(self, pos):
        ans = []
        i = 0
        while(i < len(pos)):
            ans.append(pos[i][1])
            i += 1
        return ans

    def get_quantum(self):
        return self.song.tquantum

    def get_left(self, string):
        return self.left[string]

    def get_right(self, string):
        return self.right[string]
