class Board:
    def __init__(self, rows=8, columns=8):
        self.rows = rows
        self.columns = columns
        self.board = [[None for _ in range(columns)] for _ in range(rows)]
    def __str__(self): # mostra o tabuleiro como string para Debug
        str_board = ''
        for row in self.board:
            str_board += '|'.join(row) + '\n'
        return str_board
    def place_piece(self, piece):
        row, col = piece.position
        self.board[row][col] = str(piece)
    def move_piece(self, piece, new_position):
        old_row, old_col = piece.position
        new_row, new_col = new_position
        # remove a peça da old_position
        self.board[old_row][old_col] = None
        # move a peça para a new_position
        self.board[new_row][new_col] = str(piece)

class Piece:
    def __init__(self, color, board, position):
        self.color = color
        self.board = board
        self.position = position
    #def __str__(self): # mostra a peça como string para Debug. Ex: "P" para peão preto, "p" para peão branco
        #return f"{self.name}" | retirado para evitar confusão, Piece agora é o motor de todas as peças, então o nome é definido nas subclasses
    def possible_moves(self):
        return []
class Pawn(Piece):
    def possible_moves(self):
        moves = []
        row, col = self.position
        # movimento para frente
        if self.color == 'white':
            direction = -1
        # movimento para trás
        else:
            direction = 1
        next_row = row + direction
        # esse e o próx if verificam se a posição está dentro do tabuleiro e se a casa está vazia
        if 0 <= next_row < self.board.rows:
            if self.board.board[next_row][col] is None:
                moves.append((next_row, col))
        return moves
    def symbol(self):
        return '♙' if self.color == "White" else '♟'

print(Board().board)