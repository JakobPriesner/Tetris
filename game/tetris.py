from random import randint

from figure import Figure


class Tetris:
    height = 0
    width = 0
    field = []
    level = 1
    state = "start"
    Figure = None
    figures = []

    def __init__(self, _height, _width):
        self.height = _height
        self.width = _width
        self.field = []
        self.score = 0
        self.state = "start"
        for i in range(_height):
            new_line = []
            for j in range(_width):
                new_line.append(0)
            self.field.append(new_line)
        self.pass_Figures = []
        self.new_figure()

    def new_figure(self):
        if not self.pass_Figures:
            self.pass_Figures = Figure.Figures
        pass_figure = randint(0, len(self.pass_Figures) - 1)
        self.Figure = Figure(3, 0, pass_figure)
        self.figures.append(self.Figure)
        if self.intersects():
            self.state = "gameover"

    def go_down(self, mixer):
        self.Figure.y += 1
        if self.intersects():
            mixer.play("music/block_hit.mp3")
            self.Figure.y -= 1
            self.freeze(mixer)

    def side(self, dx):
        old_x = self.Figure.x
        edge = False
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in self.Figure.image():
                    if j + self.Figure.x + dx > self.width - 1 or \
                            j + self.Figure.x + dx < 0:
                        edge = True
        if not edge:
            self.Figure.x += dx
        if self.intersects():
            self.Figure.x = old_x

    def left(self):
        self.side(-1)

    def right(self):
        self.side(1)

    def down(self, mixer):
        while not self.intersects():
            self.Figure.y += 1
        mixer.play("music/block_hit.mp3")
        self.Figure.y -= 1
        self.freeze(mixer)

    def rotate(self, mixer):
        old_rotation = self.Figure.rotation
        self.Figure.rotate()
        if self.intersects():
            self.Figure.rotation = old_rotation
        else:
            mixer.play("music/rotate.mp3")

    def intersects(self):
        intersection = False
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in self.Figure.image():
                    try:
                        if i + self.Figure.y > self.height - 1 or \
                                i + self.Figure.y < 0 or \
                                self.field[i + self.Figure.y][j + self.Figure.x] > 0 or \
                                j + self.Figure.x < 0:
                            intersection = True
                    except:
                        intersection = True
        return intersection

    def freeze(self, mixer):
        for i in range(4):
            for j in range(4):
                p = i * 4 + j
                if p in self.Figure.image():
                    self.field[i + self.Figure.y][j + self.Figure.x] = self.Figure.type + 1
        self.break_lines(mixer)
        self.new_figure()
        if self.intersects():
            self.state = "gameover"

    def break_lines(self, mixer):
        lines = 0
        is_break = False
        for i in range(1, self.height):
            zeros = 0
            for j in range(self.width):
                if self.field[i][j] == 0:
                    zeros += 1
            if zeros == 0:
                is_break = True
                lines += 1
                for i2 in range(i, 1, -1):
                    for j in range(self.width):
                        self.field[i2][j] = self.field[i2 - 1][j]
            self.score += lines ** 2
        if is_break:
            mixer.play("music/wall_break.mp3")