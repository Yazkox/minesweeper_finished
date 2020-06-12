import random
import frame

around_frame = [(1, 1), (0, 1), (1, 0), (0, -1), (-1, -1), (-1, 0), (-1, 1), (1, -1)]


class Grid:
    def __init__(self, height, width, mine_amount):
        self.height = height
        self.width = width
        self.mine_amount = mine_amount
        self.lost = False
        self.won = False
        self.display = []
        for y in range(height):
            L = []
            for x in range(width):
                L.append(frame.Frame())
            self.display.append(L)
        for y in range(height):
            for x in range(width):
                for adjacent in around_frame:
                    if y + adjacent[0] >= 0 and x + adjacent[1] >= 0:
                        try:
                            self.display[y][x]._neighbours.append(self.display[y + adjacent[0]][x + adjacent[1]])
                        except IndexError:
                            pass

    def generate(self, start_x, start_y):
        mine_placed = 0
        while mine_placed < self.mine_amount:
            y = random.randint(0, self.height - 1)
            x = random.randint(0, self.width - 1)
            if not self.display[y][x].mined and not (
                    start_x - 1 <= x <= start_x + 1 and start_y - 1 <= y <= start_y + 1):
                self.display[y][x]._put_mine()
                mine_placed += 1
        self.display[start_y][start_x].update()

    def check(self, x, y):
        if not self.display[y][x].flagged:
            self.display[y][x].update()
            if self.display[y][x].mined:
                self.lost = True

    def check_won(self):
        discovered_frame = 0
        for line in self.display:
            for frame in line:
                if not frame.covered:
                    discovered_frame += 1
        if discovered_frame + self.mine_amount >= self.height * self.width:
            self.won = True
    def mine_left(self):
        flagged_frame = 0
        for line in self.display:
            for frame in line:
                if frame.flagged:
                    flagged_frame += 1
        return self.mine_amount- flagged_frame