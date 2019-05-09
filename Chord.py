import re

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
        try:
            smallest = min(list(self.notes.values()))
        except:
            smallest = 99
            print(self.notes.values())
            print(self.notes)
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
