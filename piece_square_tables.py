"""
Python file containing the square table for each piece.
The tables were obtained from: https://www.chessprogramming.org/Simplified_Evaluation_Function
"""

WHITE_PAWNS = [[0 for i in range(8)],
            [50 for i in range(8)],
            [10, 10, 20, 30, 30, 20, 10, 10],
            [5, 5, 10, 25, 25, 10, 5, 5],
            [0, 0, 0, 30, 30, 0, 0, 0],
            [5, -5, -10, 0, 0, -10, -5, 5],
            [5, 10, 10, -20, -20, 10, 10, 5],
            [0 for i in range(8)]]

# Inverted list, as black is the other way around
BLACK_PAWNS = [WHITE_PAWNS[i] for i in range(7, -1, -1)]

WHITE_KNIGHTS = [[-40, -30, -20, -20, -20, -20, -30, -40],
              [-30, -20, 0, 0, 0, 0, -20, -30],
              [-20, 0, 10, 15, 15, 10, 0, -20],
              [-20, 5, 15, 20, 20, 15,  5,-20],
              [-20, 0, 15, 20, 20, 15,  0,-20],
              [-20, 5, 10, 15, 15, 10,  5,-20],
              [-30,-20,  0,  5,  5,  0,-20,-30],
              [-40,-30,-20,-20,-20,-20,-30,-40]]

BLACK_KNIGHTS = [WHITE_KNIGHTS[i] for i in range(7, -1, -1)]

WHITE_BISHOPS = [[-20, -10, -10, -10, -10, -10, -10, -20],
              [-10,  0,  0,  0,  0,  0,  0,-10],
              [-10,  0,  5, 10, 10,  5,  0,-10],
              [-10,  5,  5, 10, 10,  5,  5,-10],
              [-10,  0, 10, 10, 10, 10,  0,-10],
              [-10, 10, 10, 10, 10, 10, 10,-10],
              [-10,  5,  0,  0,  0,  0,  5,-10],
              [-20,-10,-10,-10,-10,-10,-10,-20]]

BLACK_BISHOPS = [WHITE_BISHOPS[i] for i in range(7, -1, -1)]

WHITE_ROOKS = [[0 for i in range(8)],
            [5, 10, 10, 10, 10, 10, 10,  5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [-5,  0,  0,  0,  0,  0,  0, -5],
            [0, 0, 0, 5, 5, 0 , 0, 0]]

BLACK_ROOKS = [WHITE_ROOKS[i] for i in range(7, -1, -1)]

WHITE_QUEEN = [[-20,-10,-10, -5, -5,-10,-10,-20],
            [-10,  0,  0,  0,  0,  0,  0,-10],
            [-10,  0,  5,  5,  5,  5,  0,-10],
            [-10,  0,  5,  5,  5,  5,  0, -10],
            [-10,  0,  5,  5,  5,  5,  0, -10],
            [-10,  5,  5,  5,  5,  5,  0,-10],
            [-10,  0,  5,  0,  0,  0,  0,-10],
            [-20,-10,-10, -5, -5,-10,-10,-20]]

BLACK_QUEEN = [WHITE_QUEEN[i] for i in range(7, -1, -1)]

WHITE_KING_MID = [[-30,-40,-40,-50,-50,-40,-40,-30],
               [-30,-40,-40,-50,-50,-40,-40,-30],
               [-30,-40,-40,-50,-50,-40,-40,-30],
               [-30,-40,-40,-50,-50,-40,-40,-30],
               [-20,-30,-30,-40,-40,-30,-30,-20],
               [-10,-20,-20,-20,-20,-20,-20,-10],
               [20, 20,  0,  0,  0,  0, 20, 20],
               [20, 30, 10,  0,  0, 10, 30, 20]]

BLACK_KING_MID = [WHITE_KING_MID[i] for  i in range(7, -1, -1)]

WHITE_KING_END = [[-50,-40,-30,-20,-20,-30,-40,-50],
               [-30,-20,-10,  0,  0,-10,-20,-30],
               [-30,-10, 20, 30, 30, 20,-10,-30],
               [-30,-10, 30, 40, 40, 30,-10,-30],
               [-30,-10, 30, 40, 40, 30,-10,-30],
               [-30,-10, 20, 30, 30, 20,-10,-30],
               [-30, -30,  0,  0,  0,  0,-30, -30],
               [-50, -30, -30, -30, -30, -30, -30, -50]]

PIECE_TABLES = {"white_P": WHITE_PAWNS,
                "black_P": BLACK_PAWNS,
                "white_N": WHITE_KNIGHTS,
                "black_N": BLACK_KNIGHTS,
                "white_B": WHITE_BISHOPS,
                "black_B": BLACK_BISHOPS,
                "white_R": WHITE_ROOKS,
                "black_R": BLACK_ROOKS,
                "white_Q": WHITE_QUEEN,
                "black_Q": BLACK_QUEEN,
                "white_K": WHITE_KING_MID,
                "black_K": BLACK_KING_MID}
