class Board: # Board é a classe que representa o tabuleiro de xadrez e controla as peças e seus movimentos
    def __init__(self, rows=8, columns=8):
        self.rows = rows
        self.columns = columns
        self.board = [[None for _ in range(columns)] for _ in range(rows)]
        self.turn = "white"
    def __str__(self): # mostra o tabuleiro como string para Debug
        str_board = ''
        for row in self.board:
            str_board += '|'.join(row) + '\n'
        return str_board
    def place_piece(self, piece):
        row, col = piece.position
        self.board[row][col] = piece
    def move_piece(self, piece, new_position):
        # Os if's abaixo verificam se o movimento é válido: se a peça pertence ao jogador que tem a vez, e se o movimento é permitido para aquela peça
        if self.turn != piece.color:
            print(f"Não é a vez do jogador {piece.color}.")
            return False
        if new_position not in piece.possible_moves():
            print("Movimento inválido para essa peça.")
            return False
        old_row, old_col = piece.position
        new_row, new_col = new_position
        # remove a peça da old_position
        self.board[old_row][old_col] = None
        # move a peça para a new_position
        self.board[new_row][new_col] = piece
        # atualiza a posição da peça
        piece.position = new_position
        
        self.switch_turn()
        return True
    def switch_turn(self):
        self.turn = "black" if self.turn == "white" else "white"

class Piece: # Piece é a super classe motor de todas as peças. Ela apenas realiza os cálculos de movimento, as subclasses (Pawn, Rook, Knight, Bishop, Queen, King) herdam essa classe e implementam seus próprios movimentos específicos.
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
        return '♙' if self.color == "white" else '♟'
def print_board(board):
    print(" a b c d e f g h")
    print("+---------------+")
    for row in board.board:
        print('|' + '|'.join(' ' if cell is None else cell.symbol() for cell in row) + '|')
    print("+---------------+")
    print(" a b c d e f g h")

"""board = Board()
pawn_white = Pawn("white", board, (6, 0))
pawn_black = Pawn("black", board, (1, 0))

board.place_piece(pawn_white)
board.place_piece(pawn_black)
print_board(board)

board.move_piece(pawn_black, (2, 0))  # ❌ erro (turno branco)
board.move_piece(pawn_white, (5, 0))  # ✅ ok
print_board(board)
board.move_piece(pawn_black, (2, 0))  # ✅ agora pode
print_board(board)""" # código de teste para verificar se o peão está funcionando corretamente.
