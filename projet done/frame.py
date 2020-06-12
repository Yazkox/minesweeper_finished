class Frame:
    def __init__(self):
        self._neighbours = []
        self.covered = True
        self.mined = False
        self.flagged = False
        self._pos_number = 0
        self._pos_number_cached = False

    def _get_pos_number(self):
        if not self._pos_number_cached:
            count = 0
            for neigh in self._neighbours:
                if neigh.mined:
                    count += 1
            self._pos_number_cached = True
            self._pos_number = count
        return self._pos_number

    def _put_mine(self):
        self.mined = True

    def _add_neighbour(self, neighbour):
        self._neighbours.append(neighbour)

    def flag(self):
        if self.covered:
            if self.flagged :
                self.flagged = False
            else :
                self.flagged = True

    def _uncover(self):
        if self.covered and not self.flagged:
            self.covered = False

    def update(self):
        if not self.mined:
            self._uncover()
            if self._get_pos_number() == 0:
                for neigh in self._neighbours:
                    if neigh.covered:
                        neigh.update()