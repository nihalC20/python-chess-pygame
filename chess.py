import pygame
import sys
import itertools
pygame.init()

# Image and Font Loading

w_pawn_img = pygame.image.load("assets/wht_pawn.png")
w_rook_img = pygame.image.load("assets/wht_rook.png")
w_knight_img = pygame.image.load("assets/wht_knight.png")
w_bishop_img = pygame.image.load("assets/wht_bishop.png")
w_queen_img = pygame.image.load("assets/wht_queen.png")
w_king_img = pygame.image.load("assets/wht_king.png")

b_pawn_img = pygame.image.load("assets/blk_pawn.png")
b_rook_img = pygame.image.load("assets/blk_rook.png")
b_knight_img = pygame.image.load("assets/blk_knight.png")
b_bishop_img = pygame.image.load("assets/blk_bishop.png")
b_queen_img = pygame.image.load("assets/blk_queen.png")
b_king_img = pygame.image.load("assets/blk_king.png")

# Changeable variables

squaresize = 60

squarecolor_wht = [200, 200, 200]
squarecolor_blk = [100, 100, 100]

selectcolor = [0, 255, 0]

colorkey = [10, 10, 10]

botbar = 150
botbarcolor = squarecolor_blk

notpressedcolor = squarecolor_wht
pressedcolor = squarecolor_blk

# Dependent Variables

game_w = squaresize * 8
game_h = (squaresize * 8)

win_w = game_w
win_h = game_h + botbar

# Static Variables

turn = "black"
selected = 0
lastselected = 0
gameboard = {}
hypo_gameboard = {}
gameover = 0
turncount = 0
w_gamestates = []
b_gamestates = []

# Class Construction


class White:
    def __init__(self):
        self.pawn = []
        self.rook = []
        self.knight = []
        self.bishop = []
        self.queen = []
        self.king = []
        self.pieces = []
        self.attacking = []
        self.hypo_attacking = []
        self.hypo_pieces = []
        self.movesum = 0


class Black:
    def __init__(self):
        self.pawn = []
        self.rook = []
        self.knight = []
        self.bishop = []
        self.queen = []
        self.king = []
        self.pieces = []
        self.attacking = []
        self.hypo_attacking = []
        self.hypo_pieces = []
        self.movesum = 0


class Pawn:
    def __init__(self, file, color):
        if color == "w":
            self.img = w_pawn_img
            self.square = [file, 7]
            self.y = squaresize * 6
        if color == "b":
            self.img = b_pawn_img
            self.square = [file, 2]
            self.y = squaresize * 1

        self.surf = pygame.Surface([squaresize, squaresize])
        self.surf.fill(colorkey)
        self.surf.set_colorkey(colorkey)
        self.surf.blit(self.img, [0, 0])

        self.x = (file - 1) * squaresize

        self.name = color + "P" + str(file)

        self.moves = []
        self.nomoves = []

        self.ep_L = 0
        self.ep_R = 0

    def atk_generate(self, listy, board):
        if self.name[0] == "w":
            if self.square[0] - 1 > 0 and self.square[1] - 1 > 0:
                listy.append([self.square[0] - 1, self.square[1] - 1])
            if self.square[0] + 1 < 9 and self.square[1] - 1 > 0:
                listy.append([self.square[0] + 1, self.square[1] - 1])
        elif self.name[0] == "b":
            if self.square[0] - 1 > 0 and self.square[1] + 1 < 9:
                listy.append([self.square[0] - 1, self.square[1] + 1])
            if self.square[0] + 1 < 9 and self.square[1] + 1 < 9:
                listy.append([self.square[0] + 1, self.square[1] + 1])

    def move_generate(self):
        global hypo_gameboard
        self.moves = []

        if self.name[0] == "w":
            if self.square[0] - 1 > 0 and self.square[1] - 1 > 0:
                if gameboard[str([self.square[0] - 1, self.square[1] - 1])] != " ":
                    if gameboard[str([self.square[0] - 1, self.square[1] - 1])].name[0] == "b":
                        self.moves.append([self.square[0] - 1, self.square[1] - 1])
            if self.square[0] + 1 < 9 and self.square[1] - 1 > 0:
                if gameboard[str([self.square[0] + 1, self.square[1] - 1])] != " ":
                    if gameboard[str([self.square[0] + 1, self.square[1] - 1])].name[0] == "b":
                        self.moves.append([self.square[0] + 1, self.square[1] - 1])
            if self.square[1] - 1 > 0:
                if gameboard[str([self.square[0], self.square[1] - 1])] == " ":
                    self.moves.append([self.square[0], self.square[1] - 1])
            if self.square[1] == 7:
                if gameboard[str([self.square[0], self.square[1] - 2])] == " ":
                    if gameboard[str([self.square[0], self.square[1] - 1])] == " ":
                        self.moves.append([self.square[0], self.square[1] - 2])
            if self.ep_L == 1:
                self.moves.append([self.square[0] - 1, self.square[1] - 1])
            if self.ep_R == 1:
                self.moves.append([self.square[0] + 1, self.square[1] - 1])
        if self.name[0] == "b":
            if self.square[0] - 1 > 0 and self.square[1] + 1 < 9:
                if gameboard[str([self.square[0] - 1, self.square[1] + 1])] != " ":
                    if gameboard[str([self.square[0] - 1, self.square[1] + 1])].name[0] == "w":
                        self.moves.append([self.square[0] - 1, self.square[1] + 1])
            if self.square[0] + 1 < 9 and self.square[1] + 1 < 9:
                if gameboard[str([self.square[0] + 1, self.square[1] + 1])] != " ":
                    if gameboard[str([self.square[0] + 1, self.square[1] + 1])].name[0] == "w":
                        self.moves.append([self.square[0] + 1, self.square[1] + 1])
            if self.square[1] + 1 < 9:
                if gameboard[str([self.square[0], self.square[1] + 1])] == " ":
                    self.moves.append([self.square[0], self.square[1] + 1])
            if self.square[1] == 2:
                if gameboard[str([self.square[0], self.square[1] + 2])] == " ":
                    if gameboard[str([self.square[0], self.square[1] + 1])] == " ":
                        self.moves.append([self.square[0], self.square[1] + 2])
            if self.ep_L == 1:
                self.moves.append([self.square[0] - 1, self.square[1] + 1])
            if self.ep_R == 1:
                self.moves.append([self.square[0] + 1, self.square[1] + 1])

        self.nomoves = []
        for hypo in self.moves:
            white.hypo_attacking = []
            black.hypo_attacking = []
            hypo_gameboard = dict(gameboard)
            white.hypo_pieces = list(white.pieces)
            black.hypo_pieces = list(black.pieces)

            if hypo_gameboard[str(hypo)] != " " and self.name[0] == "w":
                black.hypo_pieces.remove(hypo_gameboard[str(hypo)])
            elif hypo_gameboard[str(hypo)] != " " and self.name[0] == "b":
                white.hypo_pieces.remove(hypo_gameboard[str(hypo)])

            if self.name[0] == "w":
                if hypo == [self.square[0] - 1, self.square[1] - 1] and self.ep_L == 1:
                    if hypo_gameboard[str([self.square[0] - 1, self.square[1]])] != " ":
                        black.hypo_pieces.remove(hypo_gameboard[str([self.square[0] - 1, self.square[1]])])
                if hypo == [self.square[0] + 1, self.square[1] - 1] and self.ep_R == 1:
                    if hypo_gameboard[str([self.square[0] + 1, self.square[1]])] != " ":
                        black.hypo_pieces.remove(hypo_gameboard[str([self.square[0] + 1, self.square[1]])])

            if self.name[0] == "b":
                if hypo == [self.square[0] - 1, self.square[1] + 1] and self.ep_L == 1:
                    if hypo_gameboard[str([self.square[0] - 1, self.square[1]])] != " ":
                        white.hypo_pieces.remove(hypo_gameboard[str([self.square[0] - 1, self.square[1]])])
                if hypo == [self.square[0] + 1, self.square[1] + 1] and self.ep_R == 1:
                    if hypo_gameboard[str([self.square[0] + 1, self.square[1]])] != " ":
                        white.hypo_pieces.remove(hypo_gameboard[str([self.square[0] + 1, self.square[1]])])

            hypo_gameboard[str(hypo)] = gameboard[str(self.square)]
            hypo_gameboard[str(self.square)] = " "
            for piece in white.hypo_pieces:
                piece.atk_generate(white.hypo_attacking, hypo_gameboard)
            for piece in black.hypo_pieces:
                piece.atk_generate(black.hypo_attacking, hypo_gameboard)
            if self.name[0] == "w":
                for k in white.king:
                    if k.square in black.hypo_attacking:
                        self.nomoves.append(hypo)
            elif self.name[0] == "b":
                for k in black.king:
                    if k.square in white.hypo_attacking:
                        self.nomoves.append(hypo)

        self.moves.sort()
        self.moves = list(self.moves for self.moves, _ in itertools.groupby(self.moves))
        self.nomoves.sort()
        self.nomoves = list(self.nomoves for self.nomoves, _ in itertools.groupby(self.nomoves))

        for move in self.nomoves:
            self.moves.remove(move)


class Rook:
    def __init__(self, num, color):
        if num == 1:
            self.square = [1]
        elif num == 2:
            self.square = [8]
        else:
            self.square = [0]
        if color == "w":
            self.img = w_rook_img
            self.square.append(8)
        if color == "b":
            self.img = b_rook_img
            self.square.append(1)

        self.surf = pygame.Surface([squaresize, squaresize])
        self.surf.fill(colorkey)
        self.surf.set_colorkey(colorkey)
        self.surf.blit(self.img, [0, 0])

        self.x = (self.square[0] - 1) * squaresize
        self.y = (self.square[1] - 1) * squaresize

        self.name = color + "R" + str(num)

        self.moves = []
        self.nomoves = []

        self.stop = 0
        self.adder = 1

        self.castle = 0

    def atk_generate(self, listy, board):
        self.stop = 0
        self.adder = 1
        while self.stop == 0:
            if self.square[0] + self.adder < 9:
                if board[str([self.square[0] + self.adder, self.square[1]])] != " ":
                    self.stop = 1
                    listy.append([self.square[0] + self.adder, self.square[1]])
                else:
                    listy.append([self.square[0] + self.adder, self.square[1]])
                    self.adder += 1
            else:
                self.stop = 1
        self.stop = 0
        self.adder = 1
        while self.stop == 0:
            if self.square[0] - self.adder > 0:
                if board[str([self.square[0] - self.adder, self.square[1]])] != " ":
                    self.stop = 1
                    listy.append([self.square[0] - self.adder, self.square[1]])
                else:
                    listy.append([self.square[0] - self.adder, self.square[1]])
                    self.adder += 1
            else:
                self.stop = 1
        self.stop = 0
        self.adder = 1
        while self.stop == 0:
            if self.square[1] + self.adder < 9:
                if board[str([self.square[0], self.square[1] + self.adder])] != " ":
                    self.stop = 1
                    listy.append([self.square[0], self.square[1] + self.adder])
                else:
                    listy.append([self.square[0], self.square[1] + self.adder])
                    self.adder += 1
            else:
                self.stop = 1
        self.stop = 0
        self.adder = 1
        while self.stop == 0:
            if self.square[1] - self.adder > 0:
                if board[str([self.square[0], self.square[1] - self.adder])] != " ":
                    self.stop = 1
                    listy.append([self.square[0], self.square[1] - self.adder])
                else:
                    listy.append([self.square[0], self.square[1] - self.adder])
                    self.adder += 1
            else:
                self.stop = 1

    def move_generate(self):
        global hypo_gameboard
        self.moves = []

        self.stop = 0
        self.adder = 1
        while self.stop == 0:
            if self.square[0] + self.adder < 9:
                if gameboard[str([self.square[0] + self.adder, self.square[1]])] != " ":
                    if gameboard[str([self.square[0] + self.adder, self.square[1]])].name[0] != self.name[0]:
                        self.stop = 1
                        self.moves.append([self.square[0] + self.adder, self.square[1]])
                    else:
                        self.stop = 1
                else:
                    self.moves.append([self.square[0] + self.adder, self.square[1]])
                    self.adder += 1
            else:
                self.stop = 1
        self.stop = 0
        self.adder = 1
        while self.stop == 0:
            if self.square[0] - self.adder > 0:
                if gameboard[str([self.square[0] - self.adder, self.square[1]])] != " ":
                    if gameboard[str([self.square[0] - self.adder, self.square[1]])].name[0] != self.name[0]:
                        self.stop = 1
                        self.moves.append([self.square[0] - self.adder, self.square[1]])
                    else:
                        self.stop = 1
                else:
                    self.moves.append([self.square[0] - self.adder, self.square[1]])
                    self.adder += 1
            else:
                self.stop = 1
        self.stop = 0
        self.adder = 1
        while self.stop == 0:
            if self.square[1] + self.adder < 9:
                if gameboard[str([self.square[0], self.square[1] + self.adder])] != " ":
                    if gameboard[str([self.square[0], self.square[1] + self.adder])].name[0] != self.name[0]:
                        self.stop = 1
                        self.moves.append([self.square[0], self.square[1] + self.adder])
                    else:
                        self.stop = 1
                else:
                    self.moves.append([self.square[0], self.square[1] + self.adder])
                    self.adder += 1
            else:
                self.stop = 1
        self.stop = 0
        self.adder = 1
        while self.stop == 0:
            if self.square[1] - self.adder > 0:
                if gameboard[str([self.square[0], self.square[1] - self.adder])] != " ":
                    if gameboard[str([self.square[0], self.square[1] - self.adder])].name[0] != self.name[0]:
                        self.stop = 1
                        self.moves.append([self.square[0], self.square[1] - self.adder])
                    else:
                        self.stop = 1
                else:
                    self.moves.append([self.square[0], self.square[1] - self.adder])
                    self.adder += 1
            else:
                self.stop = 1

        self.nomoves = []
        for hypo in self.moves:
            white.hypo_attacking = []
            black.hypo_attacking = []
            white.hypo_pieces = list(white.pieces)
            black.hypo_pieces = list(black.pieces)
            hypo_gameboard = dict(gameboard)

            if hypo_gameboard[str(hypo)] != " " and self.name[0] == "w":
                black.hypo_pieces.remove(hypo_gameboard[str(hypo)])
            elif hypo_gameboard[str(hypo)] != " " and self.name[0] == "b":
                white.hypo_pieces.remove(hypo_gameboard[str(hypo)])

            hypo_gameboard[str(hypo)] = self
            hypo_gameboard[str(self.square)] = " "
            for piece in white.hypo_pieces:
                piece.atk_generate(white.hypo_attacking, hypo_gameboard)
            for piece in black.hypo_pieces:
                piece.atk_generate(black.hypo_attacking, hypo_gameboard)
            if self.name[0] == "w":
                for k in white.king:
                    if k.square in black.hypo_attacking:
                        self.nomoves.append(hypo)
            elif self.name[0] == "b":
                for k in black.king:
                    if k.square in white.hypo_attacking:
                        self.nomoves.append(hypo)

        self.moves.sort()
        self.moves = list(self.moves for self.moves, _ in itertools.groupby(self.moves))
        self.nomoves.sort()
        self.nomoves = list(self.nomoves for self.nomoves, _ in itertools.groupby(self.nomoves))

        for move in self.nomoves:
            self.moves.remove(move)


class Knight:
    def __init__(self, num, color):
        if num == 1:
            self.square = [2]
        elif num == 2:
            self.square = [7]
        else:
            self.square = [0]
        if color == "w":
            self.img = w_knight_img
            self.square.append(8)
        if color == "b":
            self.img = b_knight_img
            self.square.append(1)

        self.surf = pygame.Surface([squaresize, squaresize])
        self.surf.fill(colorkey)
        self.surf.set_colorkey(colorkey)
        self.surf.blit(self.img, [0, 0])

        self.x = (self.square[0] - 1) * squaresize
        self.y = (self.square[1] - 1) * squaresize

        self.name = color + "N" + str(num)

        self.moves = []
        self.nomoves = []

    def atk_generate(self, listy, board):
        if self.square[0] + 1 < 9 and self.square[1] - 2 > 0:
            listy.append([self.square[0] + 1, self.square[1] - 2])
        if self.square[0] - 1 > 0 and self.square[1] - 2 > 0:
            listy.append([self.square[0] - 1, self.square[1] - 2])
        if self.square[0] + 1 < 9 and self.square[1] + 2 < 9:
            listy.append([self.square[0] + 1, self.square[1] + 2])
        if self.square[0] - 1 > 0 and self.square[1] + 2 < 9:
            listy.append([self.square[0] - 1, self.square[1] + 2])
        if self.square[0] - 2 > 0 and self.square[1] - 1 > 0:
            listy.append([self.square[0] - 2, self.square[1] - 1])
        if self.square[0] - 2 > 0 and self.square[1] + 1 < 9:
            listy.append([self.square[0] - 2, self.square[1] + 1])
        if self.square[0] + 2 < 9 and self.square[1] - 1 > 0:
            listy.append([self.square[0] + 2, self.square[1] - 1])
        if self.square[0] + 2 < 9 and self.square[1] + 1 < 9:
            listy.append([self.square[0] + 2, self.square[1] + 1])

    def move_generate(self):
        global hypo_gameboard
        self.moves = []

        if self.square[0] + 1 < 9 and self.square[1] - 2 > 0:
            if gameboard[str([self.square[0] + 1, self.square[1] - 2])] != " ":
                if gameboard[str([self.square[0] + 1, self.square[1] - 2])].name[0] != self.name[0]:
                    self.moves.append([self.square[0] + 1, self.square[1] - 2])
            else:
                self.moves.append([self.square[0] + 1, self.square[1] - 2])
        if self.square[0] - 1 > 0 and self.square[1] - 2 > 0:
            if gameboard[str([self.square[0] - 1, self.square[1] - 2])] != " ":
                if gameboard[str([self.square[0] - 1, self.square[1] - 2])].name[0] != self.name[0]:
                    self.moves.append([self.square[0] - 1, self.square[1] - 2])
            else:
                self.moves.append([self.square[0] - 1, self.square[1] - 2])
        if self.square[0] + 1 < 9 and self.square[1] + 2 < 9:
            if gameboard[str([self.square[0] + 1, self.square[1] + 2])] != " ":
                if gameboard[str([self.square[0] + 1, self.square[1] + 2])].name[0] != self.name[0]:
                    self.moves.append([self.square[0] + 1, self.square[1] + 2])
            else:
                self.moves.append([self.square[0] + 1, self.square[1] + 2])
        if self.square[0] - 1 > 0 and self.square[1] + 2 < 9:
            if gameboard[str([self.square[0] - 1, self.square[1] + 2])] != " ":
                if gameboard[str([self.square[0] - 1, self.square[1] + 2])].name[0] != self.name[0]:
                    self.moves.append([self.square[0] - 1, self.square[1] + 2])
            else:
                self.moves.append([self.square[0] - 1, self.square[1] + 2])
        if self.square[0] - 2 > 0 and self.square[1] - 1 > 0:
            if gameboard[str([self.square[0] - 2, self.square[1] - 1])] != " ":
                if gameboard[str([self.square[0] - 2, self.square[1] - 1])].name[0] != self.name[0]:
                    self.moves.append([self.square[0] - 2, self.square[1] - 1])
            else:
                self.moves.append([self.square[0] - 2, self.square[1] - 1])
        if self.square[0] - 2 > 0 and self.square[1] + 1 < 9:
            if gameboard[str([self.square[0] - 2, self.square[1] + 1])] != " ":
                if gameboard[str([self.square[0] - 2, self.square[1] + 1])].name[0] != self.name[0]:
                    self.moves.append([self.square[0] - 2, self.square[1] + 1])
            else:
                self.moves.append([self.square[0] - 2, self.square[1] + 1])
        if self.square[0] + 2 < 9 and self.square[1] - 1 > 0:
            if gameboard[str([self.square[0] + 2, self.square[1] - 1])] != " ":
                if gameboard[str([self.square[0] + 2, self.square[1] - 1])].name[0] != self.name[0]:
                    self.moves.append([self.square[0] + 2, self.square[1] - 1])
            else:
                self.moves.append([self.square[0] + 2, self.square[1] - 1])
        if self.square[0] + 2 < 9 and self.square[1] + 1 < 9:
            if gameboard[str([self.square[0] + 2, self.square[1] + 1])] != " ":
                if gameboard[str([self.square[0] + 2, self.square[1] + 1])].name[0] != self.name[0]:
                    self.moves.append([self.square[0] + 2, self.square[1] + 1])
            else:
                self.moves.append([self.square[0] + 2, self.square[1] + 1])

        self.nomoves = []
        for hypo in self.moves:
            white.hypo_attacking = []
            black.hypo_attacking = []
            hypo_gameboard = dict(gameboard)
            white.hypo_pieces = list(white.pieces)
            black.hypo_pieces = list(black.pieces)

            if hypo_gameboard[str(hypo)] != " " and self.name[0] == "w":
                black.hypo_pieces.remove(hypo_gameboard[str(hypo)])
            elif hypo_gameboard[str(hypo)] != " " and self.name[0] == "b":
                white.hypo_pieces.remove(hypo_gameboard[str(hypo)])

            hypo_gameboard[str(hypo)] = self
            hypo_gameboard[str(self.square)] = " "
            for piece in white.hypo_pieces:
                piece.atk_generate(white.hypo_attacking, hypo_gameboard)
            for piece in black.hypo_pieces:
                piece.atk_generate(black.hypo_attacking, hypo_gameboard)
            if self.name[0] == "w":
                for k in white.king:
                    if k.square in black.hypo_attacking:
                        self.nomoves.append(hypo)
            elif self.name[0] == "b":
                for k in black.king:
                    if k.square in white.hypo_attacking:
                        self.nomoves.append(hypo)

        self.moves.sort()
        self.moves = list(self.moves for self.moves, _ in itertools.groupby(self.moves))
        self.nomoves.sort()
        self.nomoves = list(self.nomoves for self.nomoves, _ in itertools.groupby(self.nomoves))

        for move in self.nomoves:
            self.moves.remove(move)


class Bishop:
    def __init__(self, num, color):
        if num == 1:
            self.square = [3]
        elif num == 2:
            self.square = [6]
        else:
            self.square = [0]
        if color == "w":
            self.img = w_bishop_img
            self.square.append(8)
        if color == "b":
            self.img = b_bishop_img
            self.square.append(1)

        self.surf = pygame.Surface([squaresize, squaresize])
        self.surf.fill(colorkey)
        self.surf.set_colorkey(colorkey)
        self.surf.blit(self.img, [0, 0])

        self.x = (self.square[0] - 1) * squaresize
        self.y = (self.square[1] - 1) * squaresize

        self.name = color + "B" + str(num)

        self.moves = []
        self.nomoves = []

        self.stop = 0
        self.adder = 1

    def atk_generate(self, listy, board):
        self.stop = 0
        self.adder = 1
        while self.stop == 0:
            if self.square[0] + self.adder < 9 and self.square[1] + self.adder < 9:
                if board[str([self.square[0] + self.adder, self.square[1] + self.adder])] != " ":
                    self.stop = 1
                    listy.append([self.square[0] + self.adder, self.square[1] + self.adder])
                else:
                    listy.append([self.square[0] + self.adder, self.square[1] + self.adder])
                    self.adder += 1
            else:
                self.stop = 1
        self.stop = 0
        self.adder = 1
        while self.stop == 0:
            if self.square[0] - self.adder > 0 and self.square[1] + self.adder < 9:
                if board[str([self.square[0] - self.adder, self.square[1] + self.adder])] != " ":
                    self.stop = 1
                    listy.append([self.square[0] - self.adder, self.square[1] + self.adder])
                else:
                    listy.append([self.square[0] - self.adder, self.square[1] + self.adder])
                    self.adder += 1
            else:
                self.stop = 1
        self.stop = 0
        self.adder = 1
        while self.stop == 0:
            if self.square[0] + self.adder < 9 and self.square[1] - self.adder > 0:
                if board[str([self.square[0] + self.adder, self.square[1] - self.adder])] != " ":
                    self.stop = 1
                    listy.append([self.square[0] + self.adder, self.square[1] - self.adder])
                else:
                    listy.append([self.square[0] + self.adder, self.square[1] - self.adder])
                    self.adder += 1
            else:
                self.stop = 1
        self.stop = 0
        self.adder = 1
        while self.stop == 0:
            if self.square[0] - self.adder > 0 and self.square[1] - self.adder > 0:
                if board[str([self.square[0] - self.adder, self.square[1] - self.adder])] != " ":
                    self.stop = 1
                    listy.append([self.square[0] - self.adder, self.square[1] - self.adder])
                else:
                    listy.append([self.square[0] - self.adder, self.square[1] - self.adder])
                    self.adder += 1
            else:
                self.stop = 1

    def move_generate(self):
        global hypo_gameboard
        self.moves = []

        self.stop = 0
        self.adder = 1
        while self.stop == 0:
            if self.square[0] + self.adder < 9 and self.square[1] + self.adder < 9:
                if gameboard[str([self.square[0] + self.adder, self.square[1] + self.adder])] != " ":
                    if gameboard[str([self.square[0] + self.adder,
                                      self.square[1] + self.adder])].name[0] != self.name[0]:
                        self.stop = 1
                        self.moves.append([self.square[0] + self.adder, self.square[1] + self.adder])
                    else:
                        self.stop = 1
                else:
                    self.moves.append([self.square[0] + self.adder, self.square[1] + self.adder])
                    self.adder += 1
            else:
                self.stop = 1
        self.stop = 0
        self.adder = 1
        while self.stop == 0:
            if self.square[0] - self.adder > 0 and self.square[1] + self.adder < 9:
                if gameboard[str([self.square[0] - self.adder, self.square[1] + self.adder])] != " ":
                    if gameboard[str([self.square[0] - self.adder,
                                      self.square[1] + self.adder])].name[0] != self.name[0]:
                        self.stop = 1
                        self.moves.append([self.square[0] - self.adder, self.square[1] + self.adder])
                    else:
                        self.stop = 1
                else:
                    self.moves.append([self.square[0] - self.adder, self.square[1] + self.adder])
                    self.adder += 1
            else:
                self.stop = 1
        self.stop = 0
        self.adder = 1
        while self.stop == 0:
            if self.square[0] + self.adder < 9 and self.square[1] - self.adder > 0:
                if gameboard[str([self.square[0] + self.adder, self.square[1] - self.adder])] != " ":
                    if gameboard[str([self.square[0] + self.adder,
                                      self.square[1] - self.adder])].name[0] != self.name[0]:
                        self.stop = 1
                        self.moves.append([self.square[0] + self.adder, self.square[1] - self.adder])
                    else:
                        self.stop = 1
                else:
                    self.moves.append([self.square[0] + self.adder, self.square[1] - self.adder])
                    self.adder += 1
            else:
                self.stop = 1
        self.stop = 0
        self.adder = 1
        while self.stop == 0:
            if self.square[0] - self.adder > 0 and self.square[1] - self.adder > 0:
                if gameboard[str([self.square[0] - self.adder, self.square[1] - self.adder])] != " ":
                    if gameboard[str([self.square[0] - self.adder,
                                      self.square[1] - self.adder])].name[0] != self.name[0]:
                        self.stop = 1
                        self.moves.append([self.square[0] - self.adder, self.square[1] - self.adder])
                    else:
                        self.stop = 1
                else:
                    self.moves.append([self.square[0] - self.adder, self.square[1] - self.adder])
                    self.adder += 1
            else:
                self.stop = 1

        self.nomoves = []
        for hypo in self.moves:
            white.hypo_attacking = []
            black.hypo_attacking = []
            hypo_gameboard = dict(gameboard)
            white.hypo_pieces = list(white.pieces)
            black.hypo_pieces = list(black.pieces)

            if hypo_gameboard[str(hypo)] != " " and self.name[0] == "w":
                black.hypo_pieces.remove(hypo_gameboard[str(hypo)])
            elif hypo_gameboard[str(hypo)] != " " and self.name[0] == "b":
                white.hypo_pieces.remove(hypo_gameboard[str(hypo)])

            hypo_gameboard[str(hypo)] = self
            hypo_gameboard[str(self.square)] = " "
            for piece in white.hypo_pieces:
                piece.atk_generate(white.hypo_attacking, hypo_gameboard)
            for piece in black.hypo_pieces:
                piece.atk_generate(black.hypo_attacking, hypo_gameboard)
            if self.name[0] == "w":
                for k in white.king:
                    if k.square in black.hypo_attacking:
                        self.nomoves.append(hypo)
            elif self.name[0] == "b":
                for k in black.king:
                    if k.square in white.hypo_attacking:
                        self.nomoves.append(hypo)

        self.moves.sort()
        self.moves = list(self.moves for self.moves, _ in itertools.groupby(self.moves))
        self.nomoves.sort()
        self.nomoves = list(self.nomoves for self.nomoves, _ in itertools.groupby(self.nomoves))

        for move in self.nomoves:
            self.moves.remove(move)


class Queen:
    def __init__(self, num, color):
        if color == "w":
            self.img = w_queen_img
            self.square = [4, 8]
        if color == "b":
            self.img = b_queen_img
            self.square = [4, 1]

        self.surf = pygame.Surface([squaresize, squaresize])
        self.surf.fill(colorkey)
        self.surf.set_colorkey(colorkey)
        self.surf.blit(self.img, [0, 0])

        self.x = (self.square[0] - 1) * squaresize
        self.y = (self.square[1] - 1) * squaresize

        self.name = color + "Q" + str(num)

        self.moves = []
        self.nomoves = []

        self.stop = 0
        self.adder = 1

    def atk_generate(self, listy, board):
        self.stop = 0
        self.adder = 1
        while self.stop == 0:
            if self.square[0] + self.adder < 9:
                if board[str([self.square[0] + self.adder, self.square[1]])] != " ":
                    self.stop = 1
                    listy.append([self.square[0] + self.adder, self.square[1]])
                else:
                    listy.append([self.square[0] + self.adder, self.square[1]])
                    self.adder += 1
            else:
                self.stop = 1
        self.stop = 0
        self.adder = 1
        while self.stop == 0:
            if self.square[0] - self.adder > 0:
                if board[str([self.square[0] - self.adder, self.square[1]])] != " ":
                    self.stop = 1
                    listy.append([self.square[0] - self.adder, self.square[1]])
                else:
                    listy.append([self.square[0] - self.adder, self.square[1]])
                    self.adder += 1
            else:
                self.stop = 1
        self.stop = 0
        self.adder = 1
        while self.stop == 0:
            if self.square[1] + self.adder < 9:
                if board[str([self.square[0], self.square[1] + self.adder])] != " ":
                    self.stop = 1
                    listy.append([self.square[0], self.square[1] + self.adder])
                else:
                    listy.append([self.square[0], self.square[1] + self.adder])
                    self.adder += 1
            else:
                self.stop = 1
        self.stop = 0
        self.adder = 1
        while self.stop == 0:
            if self.square[1] - self.adder > 0:
                if board[str([self.square[0], self.square[1] - self.adder])] != " ":
                    self.stop = 1
                    listy.append([self.square[0], self.square[1] - self.adder])
                else:
                    listy.append([self.square[0], self.square[1] - self.adder])
                    self.adder += 1
            else:
                self.stop = 1
        self.stop = 0
        self.adder = 1
        while self.stop == 0:
            if self.square[0] + self.adder < 9 and self.square[1] + self.adder < 9:
                if board[str([self.square[0] + self.adder, self.square[1] + self.adder])] != " ":
                    self.stop = 1
                    listy.append([self.square[0] + self.adder, self.square[1] + self.adder])
                else:
                    listy.append([self.square[0] + self.adder, self.square[1] + self.adder])
                    self.adder += 1
            else:
                self.stop = 1
        self.stop = 0
        self.adder = 1
        while self.stop == 0:
            if self.square[0] - self.adder > 0 and self.square[1] + self.adder < 9:
                if board[str([self.square[0] - self.adder, self.square[1] + self.adder])] != " ":
                    self.stop = 1
                    listy.append([self.square[0] - self.adder, self.square[1] + self.adder])
                else:
                    listy.append([self.square[0] - self.adder, self.square[1] + self.adder])
                    self.adder += 1
            else:
                self.stop = 1
        self.stop = 0
        self.adder = 1
        while self.stop == 0:
            if self.square[0] + self.adder < 9 and self.square[1] - self.adder > 0:
                if board[str([self.square[0] + self.adder, self.square[1] - self.adder])] != " ":
                    self.stop = 1
                    listy.append([self.square[0] + self.adder, self.square[1] - self.adder])
                else:
                    listy.append([self.square[0] + self.adder, self.square[1] - self.adder])
                    self.adder += 1
            else:
                self.stop = 1
        self.stop = 0
        self.adder = 1
        while self.stop == 0:
            if self.square[0] - self.adder > 0 and self.square[1] - self.adder > 0:
                if board[str([self.square[0] - self.adder, self.square[1] - self.adder])] != " ":
                    self.stop = 1
                    listy.append([self.square[0] - self.adder, self.square[1] - self.adder])
                else:
                    listy.append([self.square[0] - self.adder, self.square[1] - self.adder])
                    self.adder += 1
            else:
                self.stop = 1

    def move_generate(self):
        global hypo_gameboard
        self.moves = []

        self.stop = 0
        self.adder = 1
        while self.stop == 0:
            if self.square[0] + self.adder < 9:
                if gameboard[str([self.square[0] + self.adder, self.square[1]])] != " ":
                    if gameboard[str([self.square[0] + self.adder, self.square[1]])].name[0] != self.name[0]:
                        self.stop = 1
                        self.moves.append([self.square[0] + self.adder, self.square[1]])
                    else:
                        self.stop = 1
                else:
                    self.moves.append([self.square[0] + self.adder, self.square[1]])
                    self.adder += 1
            else:
                self.stop = 1
        self.stop = 0
        self.adder = 1
        while self.stop == 0:
            if self.square[0] - self.adder > 0:
                if gameboard[str([self.square[0] - self.adder, self.square[1]])] != " ":
                    if gameboard[str([self.square[0] - self.adder, self.square[1]])].name[0] != self.name[0]:
                        self.stop = 1
                        self.moves.append([self.square[0] - self.adder, self.square[1]])
                    else:
                        self.stop = 1
                else:
                    self.moves.append([self.square[0] - self.adder, self.square[1]])
                    self.adder += 1
            else:
                self.stop = 1
        self.stop = 0
        self.adder = 1
        while self.stop == 0:
            if self.square[1] + self.adder < 9:
                if gameboard[str([self.square[0], self.square[1] + self.adder])] != " ":
                    if gameboard[str([self.square[0], self.square[1] + self.adder])].name[0] != self.name[0]:
                        self.stop = 1
                        self.moves.append([self.square[0], self.square[1] + self.adder])
                    else:
                        self.stop = 1
                else:
                    self.moves.append([self.square[0], self.square[1] + self.adder])
                    self.adder += 1
            else:
                self.stop = 1
        self.stop = 0
        self.adder = 1
        while self.stop == 0:
            if self.square[1] - self.adder > 0:
                if gameboard[str([self.square[0], self.square[1] - self.adder])] != " ":
                    if gameboard[str([self.square[0], self.square[1] - self.adder])].name[0] != self.name[0]:
                        self.stop = 1
                        self.moves.append([self.square[0], self.square[1] - self.adder])
                    else:
                        self.stop = 1
                else:
                    self.moves.append([self.square[0], self.square[1] - self.adder])
                    self.adder += 1
            else:
                self.stop = 1
        self.stop = 0
        self.adder = 1
        while self.stop == 0:
            if self.square[0] + self.adder < 9 and self.square[1] + self.adder < 9:
                if gameboard[str([self.square[0] + self.adder, self.square[1] + self.adder])] != " ":
                    if gameboard[str([self.square[0] + self.adder,
                                      self.square[1] + self.adder])].name[0] != self.name[0]:
                        self.stop = 1
                        self.moves.append([self.square[0] + self.adder, self.square[1] + self.adder])
                    else:
                        self.stop = 1
                else:
                    self.moves.append([self.square[0] + self.adder, self.square[1] + self.adder])
                    self.adder += 1
            else:
                self.stop = 1
        self.stop = 0
        self.adder = 1
        while self.stop == 0:
            if self.square[0] - self.adder > 0 and self.square[1] + self.adder < 9:
                if gameboard[str([self.square[0] - self.adder, self.square[1] + self.adder])] != " ":
                    if gameboard[str([self.square[0] - self.adder,
                                      self.square[1] + self.adder])].name[0] != self.name[0]:
                        self.stop = 1
                        self.moves.append([self.square[0] - self.adder, self.square[1] + self.adder])
                    else:
                        self.stop = 1
                else:
                    self.moves.append([self.square[0] - self.adder, self.square[1] + self.adder])
                    self.adder += 1
            else:
                self.stop = 1
        self.stop = 0
        self.adder = 1
        while self.stop == 0:
            if self.square[0] + self.adder < 9 and self.square[1] - self.adder > 0:
                if gameboard[str([self.square[0] + self.adder, self.square[1] - self.adder])] != " ":
                    if gameboard[str([self.square[0] + self.adder,
                                      self.square[1] - self.adder])].name[0] != self.name[0]:
                        self.stop = 1
                        self.moves.append([self.square[0] + self.adder, self.square[1] - self.adder])
                    else:
                        self.stop = 1
                else:
                    self.moves.append([self.square[0] + self.adder, self.square[1] - self.adder])
                    self.adder += 1
            else:
                self.stop = 1
        self.stop = 0
        self.adder = 1
        while self.stop == 0:
            if self.square[0] - self.adder > 0 and self.square[1] - self.adder > 0:
                if gameboard[str([self.square[0] - self.adder, self.square[1] - self.adder])] != " ":
                    if gameboard[str([self.square[0] - self.adder,
                                      self.square[1] - self.adder])].name[0] != self.name[0]:
                        self.stop = 1
                        self.moves.append([self.square[0] - self.adder, self.square[1] - self.adder])
                    else:
                        self.stop = 1
                else:
                    self.moves.append([self.square[0] - self.adder, self.square[1] - self.adder])
                    self.adder += 1
            else:
                self.stop = 1

        self.nomoves = []
        for hypo in self.moves:
            white.hypo_attacking = []
            black.hypo_attacking = []
            white.hypo_pieces = list(white.pieces)
            black.hypo_pieces = list(black.pieces)
            hypo_gameboard = dict(gameboard)

            if hypo_gameboard[str(hypo)] != " " and self.name[0] == "w":
                black.hypo_pieces.remove(hypo_gameboard[str(hypo)])
            elif hypo_gameboard[str(hypo)] != " " and self.name[0] == "b":
                white.hypo_pieces.remove(hypo_gameboard[str(hypo)])
            hypo_gameboard[str(hypo)] = self
            hypo_gameboard[str(self.square)] = " "
            for piece in white.hypo_pieces:
                piece.atk_generate(white.hypo_attacking, hypo_gameboard)
            for piece in black.hypo_pieces:
                piece.atk_generate(black.hypo_attacking, hypo_gameboard)
            if self.name[0] == "w":
                for k in white.king:
                    if k.square in black.hypo_attacking:
                        self.nomoves.append(hypo)
            elif self.name[0] == "b":
                for k in black.king:
                    if k.square in white.hypo_attacking:
                        self.nomoves.append(hypo)

        self.moves.sort()
        self.moves = list(self.moves for self.moves, _ in itertools.groupby(self.moves))
        self.nomoves.sort()
        self.nomoves = list(self.nomoves for self.nomoves, _ in itertools.groupby(self.nomoves))

        for move in self.nomoves:
            self.moves.remove(move)


class King:
    def __init__(self, color):
        if color == "w":
            self.img = w_king_img
            self.square = [5, 8]
        if color == "b":
            self.img = b_king_img
            self.square = [5, 1]

        self.surf = pygame.Surface([squaresize, squaresize])
        self.surf.fill(colorkey)
        self.surf.set_colorkey(colorkey)
        self.surf.blit(self.img, [0, 0])

        self.x = (self.square[0] - 1) * squaresize
        self.y = (self.square[1] - 1) * squaresize

        self.name = color + "K"

        self.check = 0
        self.checkmate = 0
        self.castle = 1

        self.moves = []
        self.nomoves = []

    def atk_generate(self, listy, board):
        if self.square[0] + 1 < 9:
            listy.append([self.square[0] + 1, self.square[1]])
        if self.square[0] - 1 > 0:
            listy.append([self.square[0] - 1, self.square[1]])
        if self.square[1] - 1 > 0:
            listy.append([self.square[0], self.square[1] - 1])
        if self.square[1] + 1 < 9:
            listy.append([self.square[0], self.square[1] + 1])
        if self.square[0] - 1 > 0 and self.square[1] - 1 > 0:
            listy.append([self.square[0] - 1, self.square[1] - 1])
        if self.square[0] + 1 < 9 and self.square[1] - 1 > 0:
            listy.append([self.square[0] + 1, self.square[1] - 1])
        if self.square[0] - 1 > 0 and self.square[1] + 1 < 9:
            listy.append([self.square[0] - 1, self.square[1] + 1])
        if self.square[0] + 1 < 9 and self.square[1] + 1 < 9:
            listy.append([self.square[0] + 1, self.square[1] + 1])

    def move_generate(self):
        global hypo_gameboard
        global gameboard
        self.moves = []

        if self.square[0] + 1 < 9:
            if gameboard[str([self.square[0] + 1, self.square[1]])] != " ":
                if gameboard[str([self.square[0] + 1, self.square[1]])].name[0] != self.name[0]:
                    self.moves.append([self.square[0] + 1, self.square[1]])
            else:
                self.moves.append([self.square[0] + 1, self.square[1]])
        if self.square[0] - 1 > 0:
            if gameboard[str([self.square[0] - 1, self.square[1]])] != " ":
                if gameboard[str([self.square[0] - 1, self.square[1]])].name[0] != self.name[0]:
                    self.moves.append([self.square[0] - 1, self.square[1]])
            else:
                self.moves.append([self.square[0] - 1, self.square[1]])
        if self.square[1] - 1 > 0:
            if gameboard[str([self.square[0], self.square[1] - 1])] != " ":
                if gameboard[str([self.square[0], self.square[1] - 1])].name[0] != self.name[0]:
                    self.moves.append([self.square[0], self.square[1] - 1])
            else:
                self.moves.append([self.square[0], self.square[1] - 1])
        if self.square[1] + 1 < 9:
            if gameboard[str([self.square[0], self.square[1] + 1])] != " ":
                if gameboard[str([self.square[0], self.square[1] + 1])].name[0] != self.name[0]:
                    self.moves.append([self.square[0], self.square[1] + 1])
            else:
                self.moves.append([self.square[0], self.square[1] + 1])
        if self.square[0] - 1 > 0 and self.square[1] - 1 > 0:
            if gameboard[str([self.square[0] - 1, self.square[1] - 1])] != " ":
                if gameboard[str([self.square[0] - 1, self.square[1] - 1])].name[0] != self.name[0]:
                    self.moves.append([self.square[0] - 1, self.square[1] - 1])
            else:
                self.moves.append([self.square[0] - 1, self.square[1] - 1])
        if self.square[0] + 1 < 9 and self.square[1] - 1 > 0:
            if gameboard[str([self.square[0] + 1, self.square[1] - 1])] != " ":
                if gameboard[str([self.square[0] + 1, self.square[1] - 1])].name[0] != self.name[0]:
                    self.moves.append([self.square[0] + 1, self.square[1] - 1])
            else:
                self.moves.append([self.square[0] + 1, self.square[1] - 1])
        if self.square[0] - 1 > 0 and self.square[1] + 1 < 9:
            if gameboard[str([self.square[0] - 1, self.square[1] + 1])] != " ":
                if gameboard[str([self.square[0] - 1, self.square[1] + 1])].name[0] != self.name[0]:
                    self.moves.append([self.square[0] - 1, self.square[1] + 1])
            else:
                self.moves.append([self.square[0] - 1, self.square[1] + 1])
        if self.square[0] + 1 < 9 and self.square[1] + 1 < 9:
            if gameboard[str([self.square[0] + 1, self.square[1] + 1])] != " ":
                if gameboard[str([self.square[0] + 1, self.square[1] + 1])].name[0] != self.name[0]:
                    self.moves.append([self.square[0] + 1, self.square[1] + 1])
            else:
                self.moves.append([self.square[0] + 1, self.square[1] + 1])

        if self.name[0] == "w":
            if gameboard["[1, 8]"] != " ":
                if gameboard["[1, 8]"].name[0] == "w" and gameboard["[1, 8]"].name[1] == "R":
                    if gameboard["[1, 8]"].castle == 1 and self.castle == 1:
                        if gameboard["[2, 8]"] == " " and gameboard["[3, 8]"] == " ":
                            if gameboard["[4, 8]"] == " " and self.check == 0:
                                self.moves.append([3, 8])
            if gameboard["[8, 8]"] != " ":
                if gameboard["[8, 8]"].name[0] == "w" and gameboard["[8, 8]"].name[1] == "R":
                    if gameboard["[8, 8]"].castle == 1 and self.castle == 1:
                        if gameboard["[6, 8]"] == " " and gameboard["[7, 8]"] == " ":
                            if self.check == 0:
                                self.moves.append([7, 8])

        if self.name[0] == "b":
            if gameboard["[1, 1]"] != " ":
                if gameboard["[1, 1]"].name[0] == "b" and gameboard["[1, 1]"].name[1] == "R":
                    if gameboard["[1, 1]"].castle == 1 and self.castle == 1:
                        if gameboard["[2, 1]"] == " " and gameboard["[3, 1]"] == " ":
                            if gameboard["[4, 1]"] == " " and self.check == 0:
                                self.moves.append([3, 1])
            if gameboard["[8, 1]"] != " ":
                if gameboard["[8, 1]"].name[0] == "b" and gameboard["[8, 1]"].name[1] == "R":
                    if gameboard["[8, 1]"].castle == 1 and self.castle == 1:
                        if gameboard["[6, 1]"] == " " and gameboard["[7, 1]"] == " ":
                            if self.check == 0:
                                self.moves.append([7, 1])

        self.nomoves = []
        for hypo in self.moves:
            white.hypo_attacking = []
            black.hypo_attacking = []
            hypo_gameboard = dict(gameboard)
            white.hypo_pieces = list(white.pieces)
            black.hypo_pieces = list(black.pieces)

            if self.name[0] == "w":
                if self.square == [5, 8] and hypo == [3, 8]:
                    hypo_gameboard[str(hypo)] = self
                    hypo_gameboard[str(self.square)] = " "
                    for piece in white.rook:
                        if piece.name[2] == "1":
                            hypo_gameboard["[4, 8]"] = piece
                    hypo_gameboard["[1, 8]"] = " "
                elif self.square == [5, 8] and hypo == [7, 8]:
                    hypo_gameboard[str(hypo)] = self
                    hypo_gameboard[str(self.square)] = " "
                    for piece in white.rook:
                        if piece.name[2] == "2":
                            hypo_gameboard["[6, 8]"] = piece
                    hypo_gameboard["[8, 8]"] = " "
                else:
                    if hypo_gameboard[str(hypo)] != " ":
                        black.hypo_pieces.remove(hypo_gameboard[str(hypo)])
                    hypo_gameboard[str(hypo)] = self
                    hypo_gameboard[str(self.square)] = " "
            elif self.name[0] == "b":
                if self.square == [5, 1] and hypo == [3, 1]:
                    hypo_gameboard[str(hypo)] = self
                    hypo_gameboard[str(self.square)] = " "
                    for piece in black.rook:
                        if piece.name[2] == "1":
                            hypo_gameboard["[4, 1]"] = piece
                    hypo_gameboard["[1, 1]"] = " "
                elif self.square == [5, 1] and hypo == [7, 1]:
                    hypo_gameboard[str(hypo)] = self
                    hypo_gameboard[str(self.square)] = " "
                    for piece in black.rook:
                        if piece.name[2] == "2":
                            hypo_gameboard["[6, 1]"] = piece
                    hypo_gameboard["[8, 1]"] = " "
                else:
                    if hypo_gameboard[str(hypo)] != " ":
                        white.hypo_pieces.remove(hypo_gameboard[str(hypo)])
                    hypo_gameboard[str(hypo)] = self
                    hypo_gameboard[str(self.square)] = " "
            for piece in white.hypo_pieces:
                piece.atk_generate(white.hypo_attacking, hypo_gameboard)
            for piece in black.hypo_pieces:
                piece.atk_generate(black.hypo_attacking, hypo_gameboard)
            if self.name[0] == "w":
                if hypo in black.hypo_attacking:
                    self.nomoves.append(hypo)
                if self.square == [5, 8] and hypo == [3, 8]:
                    if [4, 8] in black.hypo_attacking:
                        self.nomoves.append(hypo)
                if self.square == [5, 8] and hypo == [7, 8]:
                    if [6, 8] in black.hypo_attacking:
                        self.nomoves.append(hypo)
            elif self.name[0] == "b":
                if hypo in white.hypo_attacking:
                    self.nomoves.append(hypo)
                if self.square == [5, 1] and hypo == [3, 1]:
                    if [4, 1] in white.hypo_attacking:
                        self.nomoves.append(hypo)
                if self.square == [5, 1] and hypo == [7, 1]:
                    if [6, 1] in white.hypo_attacking:
                        self.nomoves.append(hypo)

        self.moves.sort()
        self.moves = list(self.moves for self.moves, _ in itertools.groupby(self.moves))
        self.nomoves.sort()
        self.nomoves = list(self.nomoves for self.nomoves, _ in itertools.groupby(self.nomoves))

        for move in self.nomoves:
            self.moves.remove(move)


# Initilization

clock = pygame.time.Clock()
win = pygame.display.set_mode([win_w, win_h])
pygame.display.set_caption("Chess")

white = White()
black = Black()


def game():
    global turn
    global selected
    global lastselected
    global gameboard
    global hypo_gameboard
    global gameover
    global turncount
    global w_gamestates
    global b_gamestates
    newgame()

    turnchange = 1

    while 1:
        clock.tick(30)
        mouse = pygame.mouse.get_pos()
        drawgame()

        gameboard = {}

        for x in range(1, 9):
            for y in range(1, 9):
                gameboard["[" + str(x) + ", " + str(y) + "]"] = " "

        for piece in white.pieces:
            gameboard[str(piece.square)] = piece
        for piece in black.pieces:
            gameboard[str(piece.square)] = piece

        hypo_gameboard = gameboard

        for piece in white.pieces:
            piece.x = (piece.square[0] - 1) * squaresize
            piece.y = (piece.square[1] - 1) * squaresize
        for piece in black.pieces:
            piece.x = (piece.square[0] - 1) * squaresize
            piece.y = (piece.square[1] - 1) * squaresize

        if turnchange == 1:

            white.attacking = []
            black.attacking = []
            for piece in white.pieces:
                piece.atk_generate(white.attacking, gameboard)
            white.attacking.sort()
            white.attacking = list(white.attacking for white.attacking, _ in itertools.groupby(white.attacking))
            for piece in black.pieces:
                piece.atk_generate(black.attacking, gameboard)
            black.attacking.sort()
            black.attacking = list(black.attacking for black.attacking, _ in itertools.groupby(black.attacking))

            for k in white.king:
                if k.square in black.attacking:
                    k.check = 1
                else:
                    k.check = 0
            for k in black.king:
                if k.square in white.attacking:
                    k.check = 1
                else:
                    k.check = 0

            turnchange = 0

            if turn == "white":
                for piece in white.pawn:
                    piece.ep_L = 0
                    piece.ep_R = 0
                b_gamestates.append(dict(gameboard))
                turn = "black"
            elif turn == "black":
                for piece in black.pawn:
                    piece.ep_L = 0
                    piece.ep_R = 0
                w_gamestates.append(dict(gameboard))
                turn = "white"
                turncount += 1

            white.movesum = 0
            black.movesum = 0

            for piece in white.pieces:
                piece.move_generate()
                white.movesum += len(piece.moves)
                piece.moves = []

            for piece in black.pieces:
                piece.move_generate()
                black.movesum += len(piece.moves)
                piece.moves = []

            for k in white.king:
                if k.check == 1 and white.movesum == 0:
                    gameover = "black"
            for k in black.king:
                if k.check == 1 and black.movesum == 0:
                    gameover = "white"

            if gameover == 0:
                if turn == "white" and white.movesum == 0:
                    gameover = "draw"
                elif turn == "black" and black.movesum == 0:
                    gameover = "draw"
                elif len(black.pieces) == 1 and len(white.pieces) == 1:
                    gameover = "draw"
                elif len(black.pieces) == 1 and len(white.pieces) == 2:
                    for piece in white.pieces:
                        if piece.name[1] == "B":
                            gameover = "draw"
                        if piece.name[1] == "N":
                            gameover = "draw"
                elif len(white.pieces) == 1 and len(black.pieces) == 2:
                    for piece in black.pieces:
                        if piece.name[1] == "B":
                            gameover = "draw"
                        if piece.name[1] == "N":
                            gameover = "draw"
                elif turncount >= 50:
                    gameover = "draw"
                else:
                    num = 0
                    if turn == "white":
                        for state in w_gamestates:
                            if dict(state) == dict(gameboard):
                                num += 1
                        if num >= 3:
                            gameover = "draw"
                    num = 0
                    if turn == "black":
                        for state in b_gamestates:
                            if dict(state) == dict(gameboard):
                                num += 1
                        if num >= 3:
                            gameover = "draw"

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if (30 <= mouse[0] <= 155 and
                            (game_h + 10 + (botbar - 10) / 2 - 30) <= mouse[1] <= (
                                    game_h + 10 + (botbar - 10) / 2 - 30 + 60)):
                        menu()
                    if (game_w - 30 - 125 <= mouse[0] <= game_w - 30 and
                            (game_h + 10 + (botbar - 10) / 2 - 30) <= mouse[1] <= (
                                    game_h + 10 + (botbar - 10) / 2 - 30 + 60)):
                        game()
                    if gameover == 0:
                        if mouse[1] < game_h:
                            clicked = [(mouse[0] // squaresize) + 1, (mouse[1] // squaresize) + 1]
                            selected = 0
                            old_list_w = list(white.pieces)
                            old_list_wp = list(white.pawn)
                            old_list_wr = list(white.rook)
                            old_list_wn = list(white.knight)
                            old_list_wb = list(white.bishop)
                            old_list_wq = list(white.queen)
                            old_list_wk = list(white.king)
                            old_list_b = list(black.pieces)
                            old_list_bp = list(black.pawn)
                            old_list_br = list(black.rook)
                            old_list_bn = list(black.knight)
                            old_list_bb = list(black.bishop)
                            old_list_bq = list(black.queen)
                            old_list_bk = list(black.king)
                            if turn == "white":
                                for piece in white.pieces:
                                    if piece.square == clicked:
                                        for pce in white.pieces:
                                            pce.moves = []
                                        selected = piece
                                        piece.move_generate()
                            elif turn == "black":
                                for piece in black.pieces:
                                    if piece.square == clicked:
                                        for pce in black.pieces:
                                            pce.moves = []
                                        selected = piece
                                        piece.move_generate()
                            if lastselected == selected:
                                if selected != 0:
                                    selected.moves = []
                                    selected = 0
                            elif selected == 0:
                                if clicked in lastselected.moves:
                                    lastsquare = lastselected.square
                                    lastselected.square = clicked
                                    if turn == "white":
                                        if lastselected.name[1] == "P":
                                            turncount = 0
                                            if lastselected.ep_L == 1:
                                                if lastsquare[0] - 1 == lastselected.square[0]:
                                                    if lastsquare[1] - 1 == lastselected.square[1]:
                                                        for piece in black.pawn:
                                                            if piece.square == [lastsquare[0] - 1, lastsquare[1]]:
                                                                black.pieces.pop(black.pieces.index(piece))
                                                                black.pawn.pop(black.pawn.index(piece))
                                                                turncount = 0
                                            if lastselected.ep_R == 1:
                                                if lastsquare[0] + 1 == lastselected.square[0]:
                                                    if lastsquare[1] - 1 == lastselected.square[1]:
                                                        for piece in black.pawn:
                                                            if piece.square == [lastsquare[0] + 1, lastsquare[1]]:
                                                                black.pieces.pop(black.pieces.index(piece))
                                                                black.pawn.pop(black.pawn.index(piece))
                                                                turncount = 0
                                        for piece in black.pieces:
                                            if piece.square == lastselected.square:
                                                turncount = 0
                                                black.pieces.pop(black.pieces.index(piece))
                                                if piece.name[1] == "P":
                                                    black.pawn.pop(black.pawn.index(piece))
                                                if piece.name[1] == "R":
                                                    black.rook.pop(black.rook.index(piece))
                                                if piece.name[1] == "N":
                                                    black.knight.pop(black.knight.index(piece))
                                                if piece.name[1] == "B":
                                                    black.bishop.pop(black.bishop.index(piece))
                                                if piece.name[1] == "Q":
                                                    black.queen.pop(black.queen.index(piece))
                                                if piece.name[1] == "K":
                                                    black.king.pop(black.king.index(piece))

                                        # En Passant

                                        if lastselected.name[1] == "P":
                                            turncount = 0
                                            if lastselected.square[1] == 5:
                                                if lastsquare[1] == 7:
                                                    for piece in black.pawn:
                                                        if piece.square[1] == 5:
                                                            if piece.square[0] + 1 == lastselected.square[0]:
                                                                piece.ep_R = 1
                                                            elif piece.square[0] - 1 == lastselected.square[0]:
                                                                piece.ep_L = 1

                                        # Castling

                                        if lastselected.name[1] == "K":
                                            lastselected.castle = 0
                                            if lastselected.square[0] == 3 and lastsquare[0] == 5:
                                                for piece in white.rook:
                                                    if piece.name[2] == "1":
                                                        piece.square = [4, 8]
                                                        piece.castle = 0
                                            if lastselected.square[0] == 7 and lastsquare[0] == 5:
                                                for piece in white.rook:
                                                    if piece.name[2] == "2":
                                                        piece.square = [6, 8]
                                                        piece.castle = 0

                                    if turn == "black":
                                        if lastselected.name[1] == "P":
                                            turncount = 0
                                            if lastselected.ep_L == 1:
                                                if lastsquare[0] - 1 == lastselected.square[0]:
                                                    if lastsquare[1] + 1 == lastselected.square[1]:
                                                        for piece in white.pawn:
                                                            if piece.square == [lastsquare[0] - 1, lastsquare[1]]:
                                                                white.pieces.pop(white.pieces.index(piece))
                                                                white.pawn.pop(white.pawn.index(piece))
                                                                turncount = 0
                                            if lastselected.ep_R == 1:
                                                if lastsquare[0] + 1 == lastselected.square[0]:
                                                    if lastsquare[1] + 1 == lastselected.square[1]:
                                                        for piece in white.pawn:
                                                            if piece.square == [lastsquare[0] + 1, lastsquare[1]]:
                                                                white.pieces.pop(white.pieces.index(piece))
                                                                white.pawn.pop(white.pawn.index(piece))
                                                                turncount = 0
                                        for piece in white.pieces:
                                            if piece.square == lastselected.square:
                                                turncount = 0
                                                white.pieces.pop(white.pieces.index(piece))
                                                if piece.name[1] == "P":
                                                    white.pawn.pop(white.pawn.index(piece))
                                                if piece.name[1] == "R":
                                                    white.rook.pop(white.rook.index(piece))
                                                if piece.name[1] == "N":
                                                    white.knight.pop(white.knight.index(piece))
                                                if piece.name[1] == "B":
                                                    white.bishop.pop(white.bishop.index(piece))
                                                if piece.name[1] == "Q":
                                                    white.queen.pop(white.queen.index(piece))
                                                if piece.name[1] == "K":
                                                    white.king.pop(white.king.index(piece))

                                        # En Passant

                                        if lastselected.name[1] == "P":
                                            turncount = 0
                                            if lastselected.square[1] == 4:
                                                if lastsquare[1] == 2:
                                                    for piece in white.pawn:
                                                        if piece.square[1] == 4:
                                                            if piece.square[0] + 1 == lastselected.square[0]:
                                                                piece.ep_R = 1
                                                            elif piece.square[0] - 1 == lastselected.square[0]:
                                                                piece.ep_L = 1

                                        # Castling

                                        if lastselected.name[1] == "K":
                                            lastselected.castle = 0
                                            if lastselected.square[0] == 3 and lastsquare[0] == 5:
                                                for piece in black.rook:
                                                    if piece.name[2] == "1":
                                                        piece.square = [4, 1]
                                                        piece.castle = 0
                                            if lastselected.square[0] == 7 and lastsquare[0] == 5:
                                                for piece in black.rook:
                                                    if piece.name[2] == "2":
                                                        piece.square = [6, 1]
                                                        piece.castle = 0

                                    if lastselected.name[1] == "R":
                                        lastselected.castle = 0

                                    turnchange = 1

                                    if lastselected.name[1] == "P":
                                        turncount = 0
                                        if lastselected.name[0] == "w" and lastselected.square[1] == 1:
                                            ret = promote(lastselected.square)
                                            if ret == "cancel":
                                                lastselected.square = lastsquare
                                                white.pieces = list(old_list_w)
                                                white.pawn = list(old_list_wp)
                                                white.rook = list(old_list_wr)
                                                white.knight = list(old_list_wn)
                                                white.bishop = list(old_list_wb)
                                                white.queen = list(old_list_wq)
                                                white.king = list(old_list_wk)
                                                black.pieces = list(old_list_b)
                                                black.pawn = list(old_list_bp)
                                                black.rook = list(old_list_br)
                                                black.knight = list(old_list_bn)
                                                black.bishop = list(old_list_bb)
                                                black.queen = list(old_list_bq)
                                                black.king = list(old_list_bk)
                                                turnchange = 0
                                            if ret == "rook":
                                                white.pieces.remove(lastselected)
                                                white.pawn.remove(lastselected)
                                                newpiece = Rook(len(white.rook) + 1, "w")
                                                newpiece.square = lastselected.square
                                                white.pieces.append(newpiece)
                                                white.rook.append(newpiece)
                                            if ret == "knight":
                                                white.pieces.remove(lastselected)
                                                white.pawn.remove(lastselected)
                                                newpiece = Knight(len(white.knight) + 1, "w")
                                                newpiece.square = lastselected.square
                                                white.pieces.append(newpiece)
                                                white.knight.append(newpiece)
                                            if ret == "bishop":
                                                white.pieces.remove(lastselected)
                                                white.pawn.remove(lastselected)
                                                newpiece = Bishop(len(white.bishop) + 1, "w")
                                                newpiece.square = lastselected.square
                                                white.pieces.append(newpiece)
                                                white.bishop.append(newpiece)
                                            if ret == "queen":
                                                white.pieces.remove(lastselected)
                                                white.pawn.remove(lastselected)
                                                newpiece = Queen(len(white.queen) + 1, "w")
                                                newpiece.square = lastselected.square
                                                white.pieces.append(newpiece)
                                                white.queen.append(newpiece)
                                        elif lastselected.name[0] == "b" and lastselected.square[1] == 8:
                                            ret = promote(lastselected.square)
                                            if ret == "cancel":
                                                lastselected.square = lastsquare
                                                white.pieces = list(old_list_w)
                                                white.pawn = list(old_list_wp)
                                                white.rook = list(old_list_wr)
                                                white.knight = list(old_list_wn)
                                                white.bishop = list(old_list_wb)
                                                white.queen = list(old_list_wq)
                                                white.king = list(old_list_wk)
                                                black.pieces = list(old_list_b)
                                                black.pawn = list(old_list_bp)
                                                black.rook = list(old_list_br)
                                                black.knight = list(old_list_bn)
                                                black.bishop = list(old_list_bb)
                                                black.queen = list(old_list_bq)
                                                black.king = list(old_list_bk)
                                                turnchange = 0
                                            if ret == "rook":
                                                black.pieces.remove(lastselected)
                                                black.pawn.remove(lastselected)
                                                newpiece = Rook(len(black.rook) + 1, "b")
                                                newpiece.square = lastselected.square
                                                black.pieces.append(newpiece)
                                                black.rook.append(newpiece)
                                            if ret == "knight":
                                                black.pieces.remove(lastselected)
                                                black.pawn.remove(lastselected)
                                                newpiece = Knight(len(black.knight) + 1, "b")
                                                newpiece.square = lastselected.square
                                                black.pieces.append(newpiece)
                                                black.knight.append(newpiece)
                                            if ret == "bishop":
                                                black.pieces.remove(lastselected)
                                                black.pawn.remove(lastselected)
                                                newpiece = Bishop(len(black.bishop) + 1, "b")
                                                newpiece.square = lastselected.square
                                                black.pieces.append(newpiece)
                                                black.bishop.append(newpiece)
                                            if ret == "queen":
                                                black.pieces.remove(lastselected)
                                                black.pawn.remove(lastselected)
                                                newpiece = Queen(len(black.queen) + 1, "b")
                                                newpiece.square = lastselected.square
                                                black.pieces.append(newpiece)
                                                black.queen.append(newpiece)

                                lastselected.moves = []

                            lastselected = selected

                elif event.button == 3:
                    for blah in gameboard:
                        if gameboard[blah] == " ":
                            print(blah + gameboard[blah])
                        else:
                            print(blah + gameboard[blah].name)


def drawgame():
    global selected
    global gameover
    global turn

    mouse = pygame.mouse.get_pos()

    win.fill(botbarcolor)

    for x in range(1, 9):
        for y in range(1, 9):
            if x % 2 != 0:
                if y % 2 != 0:
                    pygame.draw.rect(win, squarecolor_wht, [squaresize * (x - 1), squaresize * (y - 1),
                                                            squaresize, squaresize])
                else:
                    pygame.draw.rect(win, squarecolor_blk, [squaresize * (x - 1), squaresize * (y - 1),
                                                            squaresize, squaresize])
            else:
                if y % 2 != 0:
                    pygame.draw.rect(win, squarecolor_blk, [squaresize * (x - 1), squaresize * (y - 1),
                                                            squaresize, squaresize])
                else:
                    pygame.draw.rect(win, squarecolor_wht, [squaresize * (x - 1), squaresize * (y - 1),
                                                            squaresize, squaresize])

    for piece in white.pieces:
        win.blit(piece.surf, [piece.x, piece.y])
    for piece in black.pieces:
        win.blit(piece.surf, [piece.x, piece.y])

    if selected != 0:
        pygame.draw.rect(win, selectcolor, [selected.x, selected.y, squaresize, squaresize], 5)

    """

    for atk in white.attacking:
        pygame.draw.circle(win, [255, 0, 0], [int((atk[0] - 1) * squaresize + squaresize / 2),
                                              int((atk[1] - 1) * squaresize + squaresize / 2)], 5)

    for atk in black.attacking:
        pygame.draw.circle(win, [0, 255, 0], [int((atk[0] - 1) * squaresize + squaresize / 2),
                                              int((atk[1] - 1) * squaresize + squaresize / 2)], 5)
                                              
    """

    for piece in white.pieces:
        for move in piece.moves:
            pygame.draw.circle(win, [0, 0, 255], [int((move[0] - 1) * squaresize + squaresize / 2),
                                                  int((move[1] - 1) * squaresize + squaresize / 2)], 5)

    for piece in black.pieces:
        for move in piece.moves:
            pygame.draw.circle(win, [0, 0, 255], [int((move[0] - 1) * squaresize + squaresize / 2),
                                                  int((move[1] - 1) * squaresize + squaresize / 2)], 5)

    pygame.draw.rect(win, [0, 0, 0], [0, game_h, game_w, 10])

    pygame.draw.rect(win, [0, 0, 0], [30, game_h + 10 + (botbar - 10) / 2 - 30, 125, 60])

    if (30 <= mouse[0] <= 155 and
            (game_h + 10 + (botbar - 10) / 2 - 30) <= mouse[1] <= (game_h + 10 + (botbar - 10) / 2 - 30 + 60)):
        pygame.draw.rect(win, [200, 200, 50], [35, game_h + 10 + (botbar - 10) / 2 - 30 + 5, 115, 50])
    else:
        pygame.draw.rect(win, [245, 245, 0], [35, game_h + 10 + (botbar - 10) / 2 - 30 + 5, 115, 50])

    pygame.draw.rect(win, [0, 0, 0], [game_w - 30 - 125, game_h + 10 + (botbar - 10) / 2 - 30, 125, 60])

    if (game_w - 30 - 125 <= mouse[0] <= game_w - 30 and
            (game_h + 10 + (botbar - 10) / 2 - 30) <= mouse[1] <= (game_h + 10 + (botbar - 10) / 2 - 30 + 60)):
        pygame.draw.rect(win, [200, 200, 50], [game_w - 30 - 125 + 5,
                                               game_h + 10 + (botbar - 10) / 2 - 30 + 5, 115, 50])
    else:
        pygame.draw.rect(win, [245, 245, 0], [game_w - 30 - 125 + 5,
                                              game_h + 10 + (botbar - 10) / 2 - 30 + 5, 115, 50])

    for k in white.king:
        if k.check == 1:
            pygame.draw.rect(win, [255, 0, 0], [k.x, k.y, squaresize, squaresize], 5)
    for k in black.king:
        if k.check == 1:
            pygame.draw.rect(win, [255, 0, 0], [k.x, k.y, squaresize, squaresize], 5)

    menufont = pygame.font.Font("Chunkfive.otf", 35)
    menutext = menufont.render("Menu", 1, [0, 0, 0])
    win.blit(menutext, [43, game_h + 10 + (botbar - 10) / 2 - 30 + 15])

    restartfont = pygame.font.Font("Chunkfive.otf", 30)
    restarttext = restartfont.render("Restart", 1, [0, 0, 0])
    win.blit(restarttext, [game_w - 30 - 125 + 10, game_h + 10 + (botbar - 10) / 2 - 30 + 17])

    if gameover == 0:
        pygame.draw.rect(win, [255, 255, 255], [game_w / 2 - 60, game_h + 10 + (botbar - 10) / 2 - 30 / 2, 60, 30])
        pygame.draw.rect(win, [0, 0, 0], [game_w / 2, game_h + 10 + (botbar - 10) / 2 - 30 / 2, 60, 30])
        if turn == "white":
            pygame.draw.rect(win, [0, 255, 0],
                             [game_w / 2 - 60, game_h + 10 + (botbar - 10) / 2 - 30 / 2, 60, 30], 5)
        if turn == "black":
            pygame.draw.rect(win, [0, 255, 0], [game_w / 2, game_h + 10 + (botbar - 10) / 2 - 30 / 2, 60, 30], 5)

    elif gameover == "white":
        whitefont = pygame.font.Font("Chunkfive.otf", 25)
        whitetext = whitefont.render("White wins!", 1, [0, 0, 0])
        win.blit(whitetext, [game_w / 2 - whitetext.get_rect()[2] / 2,
                             game_h + 10 + (botbar - 10) / 2 - whitetext.get_rect()[3] / 2])

    elif gameover == "black":
        blackfont = pygame.font.Font("Chunkfive.otf", 25)
        blacktext = blackfont.render("Black wins!", 1, [0, 0, 0])
        win.blit(blacktext, [game_w / 2 - blacktext.get_rect()[2] / 2,
                             game_h + 10 + (botbar - 10) / 2 - blacktext.get_rect()[3] / 2])

    elif gameover == "draw":
        drawfont = pygame.font.Font("Chunkfive.otf", 25)
        drawtext = drawfont.render("Stalemate", 1, [0, 0, 0])
        win.blit(drawtext, [game_w / 2 - drawtext.get_rect()[2] / 2,
                            game_h + 10 + (botbar - 10) / 2 - drawtext.get_rect()[3] / 2])

    pygame.display.update()


def newgame():
    global turn
    global selected
    global lastselected
    global gameboard
    global white
    global black
    global gameover
    global w_gamestates
    global b_gamestates
    global turncount

    gameover = 0
    turncount = 0
    w_gamestates = []
    b_gamestates = []

    turn = "black"
    selected = 0
    lastselected = 0

    white = White()
    black = Black()

    for i in range(1, 9):
        white.pawn.append(Pawn(i, "w"))
        white.pieces.append(white.pawn[-1])
    for i in range(1, 9):
        black.pawn.append(Pawn(i, "b"))
        black.pieces.append(black.pawn[-1])

    white.rook.append(Rook(1, "w"))
    white.rook[-1].castle = 1
    white.pieces.append(white.rook[-1])

    white.rook.append(Rook(2, "w"))
    white.rook[-1].castle = 1
    white.pieces.append(white.rook[-1])

    black.rook.append(Rook(1, "b"))
    black.rook[-1].castle = 1
    black.pieces.append(black.rook[-1])

    black.rook.append(Rook(2, "b"))
    black.rook[-1].castle = 1
    black.pieces.append(black.rook[-1])

    white.knight.append(Knight(1, "w"))
    white.pieces.append(white.knight[-1])

    white.knight.append(Knight(2, "w"))
    white.pieces.append(white.knight[-1])

    black.knight.append(Knight(1, "b"))
    black.pieces.append(black.knight[-1])

    black.knight.append(Knight(2, "b"))
    black.pieces.append(black.knight[-1])

    white.bishop.append(Bishop(1, "w"))
    white.pieces.append(white.bishop[-1])

    white.bishop.append(Bishop(2, "w"))
    white.pieces.append(white.bishop[-1])

    black.bishop.append(Bishop(1, "b"))
    black.pieces.append(black.bishop[-1])

    black.bishop.append(Bishop(2, "b"))
    black.pieces.append(black.bishop[-1])

    white.queen.append(Queen(1, "w"))
    white.pieces.append(white.queen[-1])

    black.queen.append(Queen(1, "b"))
    black.pieces.append(black.queen[-1])

    white.king.append(King("w"))
    white.pieces.append(white.king[-1])

    black.king.append(King("b"))
    black.pieces.append(black.king[-1])


def menu():
    print("main menu")
    game()


def promote(sqr):
    while 1:
        clock.tick(30)
        mouse = pygame.mouse.get_pos()
        drawpromote(sqr)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if (game_w / 16 - 5 <= mouse[0] <= game_w / 16 + squaresize + 10 and
                            game_h + 10 + (botbar - 10) / 2 - squaresize / 2 - 5 <= mouse[1]
                            <= game_h + 10 + (botbar - 10) / 2 - squaresize / 2 + squaresize + 10):
                        return "queen"

                    if ((game_w / 16) * 4 - 5 <= mouse[0] <= (game_w / 16) * 4 + squaresize + 10 and
                            game_h + 10 + (botbar - 10) / 2 - squaresize / 2 - 5 <= mouse[1]
                            <= game_h + 10 + (botbar - 10) / 2 - squaresize / 2 + squaresize + 10):
                        return "bishop"

                    if ((game_w / 16) * 7 - 5 <= mouse[0] <= (game_w / 16) * 7 + squaresize + 10 and
                            game_h + 10 + (botbar - 10) / 2 - squaresize / 2 - 5 <= mouse[1]
                            <= game_h + 10 + (botbar - 10) / 2 - squaresize / 2 + squaresize + 10):
                        return "knight"

                    if ((game_w / 16) * 10 - 5 <= mouse[0] <= (game_w / 16) * 10 + squaresize + 10 and
                            game_h + 10 + (botbar - 10) / 2 - squaresize / 2 - 5 <= mouse[1]
                            <= game_h + 10 + (botbar - 10) / 2 - squaresize / 2 + squaresize + 10):
                        return "rook"

                    if ((game_w / 16) * 13 - 5 <= mouse[0] <= (game_w / 16) * 13 + squaresize + 10 and
                            game_h + 10 + (botbar - 10) / 2 - squaresize / 2 - 5 <= mouse[1]
                            <= game_h + 10 + (botbar - 10) / 2 - squaresize / 2 + squaresize + 10):
                        return "cancel"


def drawpromote(sqr):

    mouse = pygame.mouse.get_pos()

    global selected

    win.fill(botbarcolor)

    for x in range(1, 9):
        for y in range(1, 9):
            if x % 2 != 0:
                if y % 2 != 0:
                    pygame.draw.rect(win, squarecolor_wht, [squaresize * (x - 1), squaresize * (y - 1),
                                                            squaresize, squaresize])
                else:
                    pygame.draw.rect(win, squarecolor_blk, [squaresize * (x - 1), squaresize * (y - 1),
                                                            squaresize, squaresize])
            else:
                if y % 2 != 0:
                    pygame.draw.rect(win, squarecolor_blk, [squaresize * (x - 1), squaresize * (y - 1),
                                                            squaresize, squaresize])
                else:
                    pygame.draw.rect(win, squarecolor_wht, [squaresize * (x - 1), squaresize * (y - 1),
                                                            squaresize, squaresize])

    for piece in white.pieces:
        win.blit(piece.surf, [piece.x, piece.y])
    for piece in black.pieces:
        win.blit(piece.surf, [piece.x, piece.y])

    if selected != 0:
        pygame.draw.rect(win, selectcolor, [selected.x, selected.y, squaresize, squaresize], 5)

    if lastselected != 0:
        pygame.draw.rect(win, selectcolor, [lastselected.x, lastselected.y, squaresize, squaresize], 5)
        pygame.draw.rect(win, [0, 0, 255], [(sqr[0] - 1) * squaresize, (sqr[1] - 1) * squaresize,
                                            squaresize, squaresize], 5)

    pygame.draw.rect(win, [0, 0, 0], [0, game_h, game_w, 10])

    pygame.draw.rect(win, botbarcolor, [0, game_h + 10, game_w, botbar - 10])

    pygame.draw.rect(win, [0, 0, 0], [game_w / 16 - 5, game_h + 10 + (botbar - 10) / 2 - squaresize / 2 - 5,
                                      squaresize + 10, squaresize + 10])

    pygame.draw.rect(win, [0, 0, 0], [(game_w / 16) * 4 - 5, game_h + 10 + (botbar - 10) / 2 - squaresize / 2 - 5,
                                      squaresize + 10, squaresize + 10])

    pygame.draw.rect(win, [0, 0, 0], [(game_w / 16) * 7 - 5, game_h + 10 + (botbar - 10) / 2 - squaresize / 2 - 5,
                                      squaresize + 10, squaresize + 10])

    pygame.draw.rect(win, [0, 0, 0], [(game_w / 16) * 10 - 5, game_h + 10 + (botbar - 10) / 2 - squaresize / 2 - 5,
                                      squaresize + 10, squaresize + 10])

    pygame.draw.rect(win, [0, 0, 0], [(game_w / 16) * 13 - 5, game_h + 10 + (botbar - 10) / 2 - squaresize / 2 - 5,
                                      squaresize + 10, squaresize + 10])

    pygame.draw.rect(win, botbarcolor, [game_w / 16, game_h + 10 + (botbar - 10) / 2 - squaresize / 2,
                                        squaresize, squaresize])

    pygame.draw.rect(win, botbarcolor, [(game_w / 16) * 4, game_h + 10 + (botbar - 10) / 2 - squaresize / 2,
                                        squaresize, squaresize])

    pygame.draw.rect(win, botbarcolor, [(game_w / 16) * 7, game_h + 10 + (botbar - 10) / 2 - squaresize / 2,
                                        squaresize, squaresize])

    pygame.draw.rect(win, botbarcolor, [(game_w / 16) * 10, game_h + 10 + (botbar - 10) / 2 - squaresize / 2,
                                        squaresize, squaresize])

    pygame.draw.rect(win, botbarcolor, [(game_w / 16) * 13, game_h + 10 + (botbar - 10) / 2 - squaresize / 2,
                                        squaresize, squaresize])

    if (game_w / 16 - 5 <= mouse[0] <= game_w / 16 + squaresize + 10 and
            game_h + 10 + (botbar - 10) / 2 - squaresize / 2 - 5 <= mouse[1]
            <= game_h + 10 + (botbar - 10) / 2 - squaresize / 2 + squaresize + 10):
        win.blit(b_queen_img, [game_w / 16, game_h + 10 + (botbar - 10) / 2 - squaresize / 2])
    else:
        win.blit(w_queen_img, [game_w / 16, game_h + 10 + (botbar - 10) / 2 - squaresize / 2])

    if ((game_w / 16) * 4 - 5 <= mouse[0] <= (game_w / 16) * 4 + squaresize + 10 and
            game_h + 10 + (botbar - 10) / 2 - squaresize / 2 - 5 <= mouse[1]
            <= game_h + 10 + (botbar - 10) / 2 - squaresize / 2 + squaresize + 10):
        win.blit(b_bishop_img, [(game_w / 16) * 4, game_h + 10 + (botbar - 10) / 2 - squaresize / 2])
    else:
        win.blit(w_bishop_img, [(game_w / 16) * 4, game_h + 10 + (botbar - 10) / 2 - squaresize / 2])

    if ((game_w / 16) * 7 - 5 <= mouse[0] <= (game_w / 16) * 7 + squaresize + 10 and
            game_h + 10 + (botbar - 10) / 2 - squaresize / 2 - 5 <= mouse[1]
            <= game_h + 10 + (botbar - 10) / 2 - squaresize / 2 + squaresize + 10):
        win.blit(b_knight_img, [(game_w / 16) * 7, game_h + 10 + (botbar - 10) / 2 - squaresize / 2])
    else:
        win.blit(w_knight_img, [(game_w / 16) * 7, game_h + 10 + (botbar - 10) / 2 - squaresize / 2])

    if ((game_w / 16) * 10 - 5 <= mouse[0] <= (game_w / 16) * 10 + squaresize + 10 and
            game_h + 10 + (botbar - 10) / 2 - squaresize / 2 - 5 <= mouse[1]
            <= game_h + 10 + (botbar - 10) / 2 - squaresize / 2 + squaresize + 10):
        win.blit(b_rook_img, [(game_w / 16) * 10, game_h + 10 + (botbar - 10) / 2 - squaresize / 2])
    else:
        win.blit(w_rook_img, [(game_w / 16) * 10, game_h + 10 + (botbar - 10) / 2 - squaresize / 2])

    cancelfont = pygame.font.Font("opensans.ttf", 50)

    if ((game_w / 16) * 13 - 5 <= mouse[0] <= (game_w / 16) * 13 + squaresize + 10 and
            game_h + 10 + (botbar - 10) / 2 - squaresize / 2 - 5 <= mouse[1]
            <= game_h + 10 + (botbar - 10) / 2 - squaresize / 2 + squaresize + 10):
        canceltext = cancelfont.render("X", 1, [0, 0, 0])
    else:
        canceltext = cancelfont.render("X", 1, [255, 255, 255])

    win.blit(canceltext, [((game_w / 16) * 13) + squaresize / 2 - canceltext.get_rect()[2] / 2,
                          game_h + 10 + (botbar - 10) / 2 - canceltext.get_rect()[3] / 2])

    pygame.display.update()


if __name__ == '__main__':
    menu()
