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
