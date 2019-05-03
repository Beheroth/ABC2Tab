import json

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
            #print("counter: %s" % counter)
            smallest = self.time_to_ticks(chords[i].smallest(), song)
            for key in output[i].keys():
                strings[key].append((output[i][key], counter + smallest))
            counter += smallest

        for key, value in strings.items():
            print("%s: %s" % (key, value))
            pass


    def time_to_ticks(self, time, song):
        return int(time//song.tquantum)

    def lookup_chord(self, chord):
        result = {}
        #print("--START: LookUp Chord: chord: %s:" % (chord.notes))
        self.solve_collision(chord)
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
                    print("Erreur, il n'y a pas de position pour jouer %s. i = %s" %(note, i))
        #print("--END: LookUp Chord: result: %s \n" % (result))
        return result

    def solve_collision(self, chord):
        #print("--START: Solve Collision")
        result = {}
        for note in chord.notes:
            if note != 'z':
                positions = self.lookup_note(note)
                for position in positions:
                    #print("Note: %s Position: %s" % (note,position[0]))
                    if(str(position[0]) not in result):
                        result[str(position[0])] =[]
                    result[str(position[0])].append(note)
        #print("Result: %s" % result)
        #print("unique: string %s, note: %s" % self.find_unique(result))
        #print("Result: %s" % result)

        #print("--END: Solve Collision")

    def find_unique(self, positions_set):
        key = ''
        note = ''
        for key in positions_set.keys():
            if len(positions_set[key]) == 1:
                note = positions_set[key][0]    #recupere la note
                positions_set.pop(key)          #supprime la corde des positions possibles
                for otherkey in positions_set.keys():
                    if note in positions_set[otherkey]:
                        positions_set[otherkey].remove(note)    #supprime la note des autres cordes
                break
        return key, note

    def resolve_sudoku(self, positions_set):
        result = {}

    def lookup_note(self, note):
        #return positions where you can play that note on the neck
        ans = None
        try:
            ans = self.mapping[note]
        except:
            print("couldn't find %s in the mapping" % (note))
        return ans  #list of tuples
