import chess
from typing import Optional, List, Dict, Tuple

class ChessLogic:
    """
    A class encapsulating chess evaluation and move search logic using material scoring,
    piece-square tables, and a minimax search with alpha-beta pruning.

    Attributes:
        PIECE_VALUES (Dict[int, int]): Base material values for each type of piece in centipawns.
        PIECE_SQUARE_TABLES (Dict[int, List[List[float]]]): Positional score tables for pieces based on square location.
        search_depth (int): Maximum depth to explore in the minimax tree.
    """
    # Base piece values (centipawns)
    PIECE_VALUES: Dict[int, int] = {
        chess.PAWN:   10,
        chess.KNIGHT: 30,
        chess.BISHOP: 30,
        chess.ROOK:   50,
        chess.QUEEN:  90,
        chess.KING:   0,
    }

    # Piece-square tables: nested lists for 8x8 values.
    PIECE_SQUARE_TABLES: Dict[int, List[List[float]]] = {
        chess.KING: [
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-3.0, -4.0, -4.0, -5.0, -5.0, -4.0, -4.0, -3.0],
            [-2.0, -3.0, -3.0, -4.0, -4.0, -3.0, -3.0, -2.0],
            [-1.0, -2.0, -2.0, -2.0, -2.0, -2.0, -2.0, -1.0],
            [ 2.0,  2.0,  0.0,  0.0,  0.0,  0.0,  2.0,  2.0],
            [ 2.0,  3.0,  1.0,  0.0,  0.0,  1.0,  3.0,  2.0]
        ],
        chess.QUEEN: [
            [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0],
            [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
            [-1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
            [-0.5,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
            [ 0.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -0.5],
            [-1.0,  0.0,  0.5,  0.5,  0.5,  0.5,  0.0, -1.0],
            [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
            [-2.0, -1.0, -1.0, -0.5, -0.5, -1.0, -1.0, -2.0]
        ],
        chess.ROOK: [
            [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
            [ 0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5],
            [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
            [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
            [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
            [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
            [-0.5,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -0.5],
            [ 0.0,  0.0,  0.0,  0.5,  0.5,  0.0,  0.0,  0.0]
        ],
        chess.BISHOP: [
            [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0],
            [-1.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0, -1.0],
            [-1.0,  0.0,  0.5,  1.0,  1.0,  0.5,  0.0, -1.0],
            [-1.0,  0.5,  0.5,  1.0,  1.0,  0.5,  0.5, -1.0],
            [-1.0,  0.0,  1.0,  1.0,  1.0,  1.0,  0.0, -1.0],
            [-1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0, -1.0],
            [-1.0,  0.5,  0.0,  0.0,  0.0,  0.0,  0.5, -1.0],
            [-2.0, -1.0, -1.0, -1.0, -1.0, -1.0, -1.0, -2.0]
        ],
        chess.KNIGHT: [
            [-5.0, -4.0, -3.0, -3.0, -3.0, -3.0, -4.0, -5.0],
            [-4.0, -2.0,  0.0,  0.0,  0.0,  0.0, -2.0, -4.0],
            [-3.0,  0.0,  1.0,  1.5,  1.5,  1.0,  0.0, -3.0],
            [-3.0,  0.5,  1.5,  1.7,  1.7,  1.5,  0.5, -3.0],
            [-3.0,  0.0,  1.5,  1.7,  1.7,  1.5,  0.0, -3.0],
            [-3.0,  0.5,  1.0,  1.5,  1.5,  1.0,  0.5, -3.0],
            [-2.0, -2.0,  0.0,  0.5,  0.5,  0.0, -2.0, -2.0],
            [-3.0, -0.5,  0.0, -1.0, -1.0,  0.0, -0.5, -3.0]
        ],
        chess.PAWN: [
            [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0],
            [ 5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0,  5.0],
            [ 1.0,  1.0,  2.0,  3.0,  3.0,  2.0,  1.0,  1.0],
            [ 0.5,  0.5,  1.0,  2.5,  2.5,  1.0,  0.5,  0.5],
            [ 0.0,  0.0,  2.0,  2.0,  2.0,  2.0,  0.0,  0.0],
            [ 0.5, -0.5, -1.0,  2.0,  2.0, -1.0, -0.5,  0.5],
            [ 0.5,  1.0,  1.0,  1.0,  1.0,  1.0,  1.0,  0.5],
            [ 0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0,  0.0]
        ],
    }

    def __init__(self, depth: int = 3):
        """
        Initializes the ChessLogic object.

        Args:
            depth (int): Search depth for the minimax algorithm.
        """
        self.search_depth = depth
        # Transposition table: zobrist key -> (depth, score)
        self.transposition: Dict[int, Tuple[int, float]] = {}

    def piece_value(self, piece: chess.Piece) -> int:
        """
        Returns the material value of a piece.

        Args:
            piece (chess.Piece): The chess piece to evaluate.

        Returns:
            int: Material value in centipawns.
        """
        return self.PIECE_VALUES.get(piece.piece_type, 0)

    def quiesce(self, board, alpha, beta, qdepth=4):
        stand_pat = self.evaluate_board(board)
        if stand_pat >= beta:
            return beta
        alpha = max(alpha, stand_pat)

        # Only consider up to 3 top captures
        caps = [m for m in board.legal_moves if board.is_capture(m)]
        caps.sort(key=lambda m: self.capture_score(board, m), reverse=True)
        for mv in caps[:3]:
            if qdepth <= 0:
                break
            board.push(mv)
            score = -self.quiesce(board, -beta, -alpha, qdepth-1)
            board.pop()
            if score >= beta:
                return beta
            alpha = max(alpha, score)

        return alpha



    def pos_value(self, piece_type: int, pos: int, color: bool) -> float:
        """
        Returns the positional value of a piece based on its location.

        Args:
            piece_type (int): Type of the piece (e.g., chess.KNIGHT).
            pos (int): Square index (0-63).
            color (bool): True for white, False for black.

        Returns:
            float: Positional score from the piece-square table.
        """
        table = self.PIECE_SQUARE_TABLES[piece_type]
        row = pos // 8 if color else 7 - (pos // 8)
        col = pos % 8
        return table[row][col]

    def evaluate_board(self, board: chess.Board) -> float:
        """
        Evaluates the board based on material and positional scores.

        Args:
            board (chess.Board): The current board state.

        Returns:
            float: Evaluation score. Positive if white is better, negative if black is better.
        """
        if board.is_checkmate():
            return float('-inf') if board.turn else float('inf')
        elif board.is_stalemate() or board.is_insufficient_material() or board.can_claim_draw():
            return 0
        val = 0.0
        # Material
        for piece in board.piece_map().values():
            v = self.piece_value(piece)
            val += v if piece.color == chess.WHITE else -v
        # Positional
        for sq in range(64):
            piece = board.piece_at(sq)
            if piece:
                color = (piece.color == chess.WHITE)
                val += self.pos_value(piece.piece_type, sq, color)
        return val
    
    def capture_score(self, board, move):
        """
        Returns a score for a capture move using MVV-LVA heuristic.

        Args:
            board (chess.Board): The current board.
            move (chess.Move): The move being evaluated.

        Returns:
            int: Capture score. Higher values are better captures.
        """
        if board.piece_at(move.to_square) is None:
            return 0
        victim = board.piece_at(move.to_square).piece_type
        attacker = board.piece_at(move.from_square).piece_type
        return self.PIECE_VALUES[victim]*100 - self.PIECE_VALUES[attacker]

    def minimax(self, board: chess.Board, depth: int, alpha: float, beta: float, maximizing_player: bool) -> float:
        """
        Recursive minimax search with alpha-beta pruning.

        Args:
            board (chess.Board): Current board state.
            depth (int): Remaining depth to search.
            alpha (float): Alpha value for pruning.
            beta (float): Beta value for pruning.
            maximizing_player (bool): True if the current player is maximizing.

        Returns:
            Tuple[float, Optional[chess.Move]]: Best evaluation score and corresponding move.
        """
        # Transposition lookup using private key
        key = board._transposition_key()
        entry = self.transposition.get(key)
        if entry and entry[0] >= depth:
        # entry == (stored_depth, stored_score, stored_move)
            _, stored_score, stored_move = entry
            return stored_score, stored_move
        
        best_move = None
        
        if board.is_game_over():
            if board.is_checkmate():
                score = -float('inf') if maximizing_player else float('inf')
            else:
                score = 0
            return score, None
        elif depth == 0:
            score = self.evaluate_board(board)
            # score = self.quiesce(board, alpha, beta)
        else:
            moves = list(board.legal_moves)
            # MVV-LVA (Most Valuable Victim – Least Valuable Aggressor) based sorting
            moves.sort(key=lambda m: (board.is_capture(m), self.capture_score(board, m)), reverse=True)
            if maximizing_player:
                score = -float('inf')
                for mv in moves:
                    board.push(mv)
                    val, mmv = self.minimax(board, depth-1, alpha, beta, False)
                    board.pop()
                    if score < val:
                        score = val
                        best_move = mv
                    alpha = max(alpha, val)
                    if beta <= alpha:
                        break
            else:
                score = float('inf')
                for mv in moves:
                    board.push(mv)
                    val, mmv = self.minimax(board, depth-1, alpha, beta, True)
                    board.pop()
                    if score > val:
                        score = val
                        best_move = mv
                    beta = min(beta, val)
                    if beta <= alpha:
                        break
        # Store in transposition table
        self.transposition[key] = (depth, score,best_move)
        return score, best_move

    def get_move(self, board: chess.Board, turn : bool) -> Optional[chess.Move]:
        """
        Returns the best move for the current player using minimax search.

        Args:
            board (chess.Board): Current board state.
            turn (bool): True if it's white's turn, False for black.

        Returns:
            Optional[chess.Move]: The best move found, or None if no legal move exists.
        """
        self.transposition.clear()
        _, best_move =  self.minimax(board, self.search_depth, -float('inf'), float('inf'), turn)
        return best_move