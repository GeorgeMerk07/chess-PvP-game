import copy 

from piece import Pawn, King, Bishop, Rook, Queen, Knight
from const import ROWS, COLS

class AI:

    PIECE_VALUE = {
        Pawn: 1,
        Knight: 3,
        Bishop: 3,
        Rook: 5,
        Queen: 9,
        King: 0,
    }

    def __init__(self, color='black', depth=2):
        self.color = color
        self.depth = depth

    def evaluete_board(self, board):
        score = 0
        for row in range(ROWS):
            for col in range(COLS):
                square = board.squares[row][col]
                if square.has_piece():
                    piece = square.piece
                    value = self.PIECE_VALUE.get(type(piece), 0)
                    score += value if piece.color == self.color else -value
        return score
    
    # Generate all legal moves for a color on a given board

    def get_all_moves(self, board, color):
        all_moves = []
        for row in range(ROWS):
            for col in range(COLS):
                square = board.squares[row][col]
                if square.has_piece() and square.piece.color == color:
                    piece = square.piece
                    piece.clear_moves()
                    board.calc_moves(piece, row, col, bool=True)
                    for move in piece.moves:
                        all_moves.append((piece, move, row, col))
        
        return all_moves
    
    #MINIMAX WITH 

    def minmax(self,board, depth, alpha, beta, maximizing, color):
        if depth == 0:
            return self.evaluete_board(board), None
        
        opponent_color = 'white' if color == 'black' else 'black'
        moves = self.get_all_moves(board, color)

        if not moves:
            return self.evaluete_board(board), None
        
        best_moves = None

        if maximizing:
            best_score = float(-9999)
            for piece, move, row, col in moves:
                board_copy = copy.deepcopy(board)
                piece_copy = board_copy.squares[row][col].piece
                board_copy.move(piece_copy, move, testing=True)

                score, _ = self.minmax(
                    board_copy, depth - 1, alpha, beta, True, opponent_color
                )

                if score > best_score:
                    best_score = score
                    best_move = (piece, move)

                beta = min(beta, score)
                if beta <= alpha:
                    break
        
        else:
            best_score = float('inf')
            for piece, move, row, col in moves:
                board_copy = copy.deepcopy(board)
                piece_copy = board_copy.squares[row][col].piece
                board_copy.move(piece_copy, move, testing=True)

                score, _ = self.minmax(
                    board_copy, depth -1, alpha,beta, True, opponent_color
                )

                if score < best_score:
                    best_score = score
                    best_move = (piece, move)
                    if beta <= alpha:
                        break
        
        return best_score, best_move
    
    # Public entry point

    def get_best_move(self, board):
        _, best_move = self.minmax(
            board, self.depth, -9999, 9999, True, self.color
        )
        return best_move