class Song:
    def __init__(self, header, chords):
        self.header = header
        self.chords = chords
        self.tquantum = None

    def eval_tquantum(self):
        quantums = []
        for chord in self.chords:
            if chord.smallest() in quantums:
                pass
                #print("skip")
            else:
                quantums.append(chord.smallest())
        #trouver le PGCD
        cur_gcp = 1
        for elem in quantums:
            cur_gcp = self.gcp(cur_gcp, elem)

        #smallest = min(quantums)
        smallest = cur_gcp
        #print("smallest is %s" % smallest)
        self.tquantum = smallest

    def ordTicks(self, tics):
        strings = {1:[], 2:[], 3:[], 4:[], 5:[], 6:[]}
        for tic in tics:
            Slist = strings[tic[0]]
            Slist.append(tic[1])
        return strings

    def gcp(self, x, y):
        while y != 0:
            (x, y) = (y, x % y)
        return x



