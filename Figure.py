from color_Manager import color_Manager
import color_Manager


class Figure:
    x = 0
    y = 0

    Figures = [
        [[1, 5, 9, 13], [4, 5, 6, 7]],  # Line
        [[1, 2, 5, 9], [0, 4, 5, 6], [1, 5, 9, 8], [4, 5, 6, 10]],  # rev l
        [[1, 2, 6, 10], [5, 6, 7, 9], [2, 6, 10, 11], [3, 5, 6, 7]],  # l
        [[1, 2, 5, 6]],  # block
        [[6, 7, 9, 10], [1, 5, 6, 10]],  # s
        [[1, 4, 5, 6], [1, 4, 5, 9], [4, 5, 6, 9], [1, 5, 6, 9]],  # t
        [[4, 5, 9, 10], [2, 6, 5, 9]]  # rev s
    ]

    def __init__(self, x_coord, y_coord, pass_Figure):
        self.x = x_coord
        self.y = y_coord
        self.type = pass_Figure
        self.color = color_Manager.colors[self.type + 1]
        self.rotation = 0

    def image(self):
        return self.Figures[self.type][self.rotation]

    def rotate(self):
        self.rotation = (self.rotation + 1) % len(self.Figures[self.type])