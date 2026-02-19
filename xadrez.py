class Board: # Board é a classe que representa o tabuleiro de xadrez e controla as peças e seus movimentos
    def __init__(self, rows=8, columns=8):
        self.rows = rows
        self.columns = columns
        self.board = [[None for _ in range(columns)] for _ in range(rows)]
        self.turn = "white"
        self.pieces = []
        self.lastest_move = None
        self.moved = False
        self.start = True
    def __str__(self): # mostra o tabuleiro como string para Debug
        str_board = ''
        for row in self.board:
            str_board += '|'.join(row) + '\n'
        return str_board
    def place_piece(self, piece):
        self.pieces.append(piece)
        row, col = piece.position
        self.board[row][col] = piece
    def remove_piece(self, position):
        for piece in self.pieces:
            if piece.position == position:
                self.pieces.remove(piece)
                return piece
        return None
    def move_piece(self, piece, new_position):
        # Os if's abaixo verificam se o movimento é válido: se a peça pertence ao jogador que tem a vez, e se o movimento é permitido para aquela peça
        if self.turn != piece.color:
            print(f"Não é a vez do jogador {piece.color}.")
            return False
        if new_position not in piece.possible_moves():
            print("Movimento inválido para essa peça.")
            return False
        
        captured = self.remove_piece(new_position)  # remove a peça adversária, se houver
        if captured:
            print(f"{piece.color} capturou {captured.color} em {new_position}")
        
        old_row, old_col = piece.position
        new_row, new_col = new_position
        # remove a peça da old_position
        self.board[old_row][old_col] = None
        # move a peça para a new_position
        self.board[new_row][new_col] = piece
        # atualiza a posição da peça
        piece.position = new_position
        
        # promoção do peão(preguiça de criar uma função específica para isso, então coloquei aqui mesmo)
        if isinstance(piece, Pawn):
            if piece.color == "white" and piece.position[0] == 0:
                row, col = piece.position
                self.board[row][col] = None
                self.remove_piece(piece.position)
                self.place_piece(Queen("white", self, piece.position))
            elif piece.color == "black" and piece.position[0] == 7:
                row, col = piece.position
                self.board[row][col] = None
                self.remove_piece(piece.position)
                self.place_piece(Queen("black", self, piece.position))
                
        # en passant do peão(também preguiça de criar uma função específica para isso, então coloquei aqui mesmo)
        if isinstance(piece, Pawn):
            if old_col != new_col and captured is None: # movimento diagonal sem captura normal
                self.board[old_row][new_col] = None # remove a peça adversária que está na coluna do movimento diagonal
                
        self.lastest_move = {
            "piece": piece,
            "from": (old_row, old_col),
            "to": (new_row, new_col)
        }
        self.moved = True

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
    def ray_moves(self, directions):
        moves = []
        row, col = self.position
        for delta_row, delta_col in directions:
            new_row, new_col = row + delta_row, col + delta_col
            while 0 <= new_row < self.board.rows and 0 <= new_col < self.board.columns:
                target_piece = self.board.board[new_row][new_col]
                if target_piece is None:
                    moves.append((new_row, new_col))
                elif target_piece.color != self.color:
                    moves.append((new_row, new_col))
                    break
                else:
                    break
                new_row += delta_row
                new_col += delta_col
        return moves
        
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
                
        # movimento diagonal para captura(mais anotações para os próximos if's)
        for delta_col in [-1, 1]:
            new_col = col + delta_col
            """Esse if's verificam se a posição diagonal está dentro do tabuleiro e se há uma peã adversária para capturar."""
            if 0 <= next_row < self.board.rows and 0 <= new_col < self.board.columns:
                target_piece = self.board.board[next_row][new_col]
                if target_piece is not None and target_piece.color != self.color:
                    moves.append((next_row, new_col))
        
        # duplo movimento incial do peão
        if self.color == 'white' and row == 6:
            if self.board.board[row - 1][col] is None and self.board.board[row - 2][col] is None:
                moves.append((row - 2, col))
        elif self.color == 'black' and row == 1:
            if self.board.board[row + 1][col] is None and self.board.board[row + 2][col] is None:
                moves.append((row + 2, col))
        
        """ CAPTURA EN PASSANT:    
        lastest_move é um dicionário que armazena informações sobre o último movimento(visitar a função move_piece para entender melhor), 
        e aqui verificamos se o último movimento foi um duplo movimento de um peão adversário, e se o peão está na posição correta para realizar a captura en passant. 
        Após verificar isso, adicionamos a posição de captura en passant aos movimentos possíveis do peão."""
        if self.board.moved:
            if abs(self.board.lastest_move["from"][0] - self.board.lastest_move["to"][0]) == 2 and self.board.lastest_move["piece"].color != self.color:
                if self.color == 'white' and row == 3:
                    for delta_col in [-1, 1]:
                        new_col = col + delta_col
                        if 0 <= new_col < self.board.columns:
                            target_piece = self.board.board[row][new_col]
                            if target_piece == self.board.lastest_move["piece"] and isinstance(target_piece, Pawn) and target_piece.color != self.color:
                                moves.append((row - 1, new_col))
                elif self.color == 'black' and row == 4:
                    for delta_col in [-1, 1]: 
                        new_col = col + delta_col
                        if 0 <= new_col < self.board.columns:
                            target_piece = self.board.board[row][new_col]
                            if target_piece == self.board.lastest_move["piece"] and isinstance(target_piece, Pawn) and target_piece.color != self.color:
                                moves.append((row + 1, new_col))
        print(f"Peão {self.color} em {self.position} pode se mover para: {moves}")
        return moves
    def symbol(self):
        return '♟' if self.color == "white" else '♙'
class Rook(Piece):
    def possible_moves(self):
        return self.ray_moves([(1,0), (-1,0), (0,1), (0,-1)])
    def symbol(self):
        return '♜' if self.color == "white" else '♖'

class Bishop(Piece):
    def possible_moves(self):
        return self.ray_moves([(1,1), (1,-1), (-1,1), (-1,-1)])
    def symbol(self):
        return '♝' if self.color == "white" else '♗'

class Queen(Piece):
    def possible_moves(self):
        return self.ray_moves([
            (1,0), (-1,0), (0,1), (0,-1),
            (1,1), (1,-1), (-1,1), (-1,-1)
        ])
    def symbol(self):
        return '♛' if self.color == "white" else '♕'

    

def print_board(board):
    print(" a b c d e f g h")
    print("+---------------+")
    for row in board.board:
        print('|' + '|'.join(' ' if cell is None else cell.symbol() for cell in row) + '|')
    print("+---------------+")
    print(" a b c d e f g h")


print("\n==============================")
print("TESTE 1 — PEÃO: MOVIMENTO SIMPLES E DUPLO")
print("==============================")

board = Board()

pw = Pawn("white", board, (6, 4))
board.place_piece(pw)

print_board(board)
print("Esperado: (5,4) e (4,4)")
print(pw.possible_moves())

board.move_piece(pw, (4, 4))
print_board(board)


print("\n==============================")
print("TESTE 2 — PEÃO: BLOQUEIO FRONTAL")
print("==============================")

board = Board()

pw = Pawn("white", board, (6, 4))
pb = Pawn("black", board, (5, 4))

board.place_piece(pw)
board.place_piece(pb)

print_board(board)
print("Esperado: sem movimentos")
print(pw.possible_moves())


print("\n==============================")
print("TESTE 3 — PEÃO: CAPTURA DIAGONAL")
print("==============================")

board = Board()

pw = Pawn("white", board, (6, 4))
pb = Pawn("black", board, (5, 5))

board.place_piece(pw)
board.place_piece(pb)

print_board(board)
print("Esperado: captura em (5,5)")
print(pw.possible_moves())

board.move_piece(pw, (5, 5))
print_board(board)


print("\n==============================")
print("TESTE 4 — EN PASSANT")
print("==============================")

board = Board()

pw = Pawn("white", board, (6, 3))
pb = Pawn("black", board, (4, 4))

board.place_piece(pw)
board.place_piece(pb)

print_board(board)

board.move_piece(pw, (4, 3))  # duplo
print_board(board)

print("Esperado: en passant disponível (5,3)")
print(pb.possible_moves())

board.move_piece(pb, (5, 3))
print_board(board)


print("\n==============================")
print("TESTE 5 — TORRE: RAY CAST + BLOQUEIO")
print("==============================")

board = Board()

rw = Rook("white", board, (4, 4))
pw = Pawn("white", board, (4, 6))
pb = Pawn("black", board, (4, 2))

board.place_piece(rw)
board.place_piece(pw)
board.place_piece(pb)

print_board(board)
print("Esperado: torre para até (4,5) e captura em (4,2)")
print(rw.possible_moves())


print("\n==============================")
print("TESTE 6 — BISPO: DIAGONAIS")
print("==============================")

board = Board()

bw = Bishop("white", board, (4, 4))
pb = Pawn("black", board, (2, 2))

board.place_piece(bw)
board.place_piece(pb)

print_board(board)
print("Esperado: diagonal até (2,2)")
print(bw.possible_moves())


print("\n==============================")
print("TESTE 7 — RAINHA: TORRE + BISPO")
print("==============================")

board = Board()

qw = Queen("white", board, (4, 4))
pb = Pawn("black", board, (4, 7))
pw = Pawn("white", board, (2, 4))

board.place_piece(qw)
board.place_piece(pb)
board.place_piece(pw)

print_board(board)
print("Esperado: captura em (4,7), bloqueio em (2,4)")
print(qw.possible_moves())


print("\n==============================")
print("TESTE 8 — TURNOS")
print("==============================")

board = Board()

rw = Rook("white", board, (7, 0))
rb = Rook("black", board, (0, 0))

board.place_piece(rw)
board.place_piece(rb)

print_board(board)

print("Tentando mover preto fora do turno:")
board.move_piece(rb, (1, 0))  # deve falhar

board.move_piece(rw, (6, 0))  # válido
print_board(board)

print("Agora preto pode jogar:")
board.move_piece(rb, (1, 0))
print_board(board)


print("\n==============================")
print("TESTE 9 — PROMOÇÃO")
print("==============================")

board = Board()

pw = Pawn("white", board, (1, 7))
board.place_piece(pw)

print_board(board)
board.move_piece(pw, (0, 7))

print("Esperado: ♛ branca")
print_board(board)

print("\n===== FIM DOS TESTES =====")
