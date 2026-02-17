class Board:
    def __init__(self, rows=8, columns=8):
        self.rows = rows
        self.columns = columns
        self.board = []
        self.create_board()
    def __str__(self): # Mostra o tabuleiro como string para Debug
        str_board = ''
        for row in self.board:
            str_board += '|'.join(row) + '\n'
        return str_board
    def create_board(self):
        for i in range(self.rows):
            row = []
            for j in range(self.columns):
                if (i + j) % 2 == 0:
                    row.append(' ')
                else:
                    row.append('#')
            self.board.append(row)
    def print_board(self):
        print('-' * (self.columns * 2 + 1))
        for row in self.board:
            print('|' + ('|').join(row) + '|')
        print('-' * (self.columns * 2 + 1))
class Piece:
    def __init__(self, name, color, board, position):
        self.name = name
        self.color = color
        self.board = board
        self.position = position
    def __str__(self): # Mostra a peça como string para Debug. Ex: "P" para peão preto, "p" para peão branco
        return f"{self.name}"
    def move(self, new_position):
        self.position = new_position
    def load_board(self):
        row, col = self.position
        self.board.board[row][col] = str(self)
        self.board.print_board()
class Pawn(Piece):
    def __init__(self, color, board, position):
        super().__init__("P", color, board, position)
    def move(self, new_position):
        super().move(new_position)
    def load_board(self):
        return super().load_board()
board = Board()
pawn = Pawn("Black", board, (1, 0))
pawn.load_board()