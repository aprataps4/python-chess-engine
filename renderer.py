from enum import Enum
from constants import *
from pathlib import Path
import pygame

class Phase(Enum):
    """
    Enum representing different interaction phases in the game.
    """
    CHOOSING_COLOR = 1   # Player is selecting their color
    WAITING_SOURCE = 2   # Waiting for the player to select the piece to move
    WAITING_DEST = 3     # Waiting for the player to select the destination square
    PROMOTING = 4        # Waiting for promotion piece selection

    
class Renderer:
    """
    Renderer class for drawing the chessboard, pieces, highlights, text, and animations using Pygame.
    """
    def __init__(self, screen, img_folder: Path):
        """
        Initialize the renderer with the display screen and path to piece images.

        Args:
            screen (pygame.Surface): The main display surface.
            img_folder (Path): Path to the folder containing piece image files.
        """
        self.screen = screen
        self.img_folder = img_folder
        self._load_images()
        self.font = pygame.font.Font(None, FONT_SIZE)

    def _load_images(self):
        """
        Load all piece images into memory from the specified folder.
        """
        PIECE_MAP = {
            'P': 'wP.png', 'N': 'wN.png', 'B': 'wB.png',
            'R': 'wR.png', 'Q': 'wQ.png', 'K': 'wK.png',
            'p': 'bP.png', 'n': 'bn.png', 'b': 'bB.png',
            'r': 'bR.png', 'q': 'bQ.png', 'k': 'bK.png'
        }
        self.images = {}
        for sym, fname in PIECE_MAP.items():
            path = self.img_folder / fname
            self.images[sym] = pygame.image.load(str(path)).convert_alpha()

    def draw_board(self):
        """
        Draw the chessboard squares on the screen.
        """
        for r in range(ROWS):
            for c in range(COLS):
                color = WHITE if (r + c) % 2 == 0 else GREEN
                rect = (c * SQUARE_SIZE, r * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)
                pygame.draw.rect(self.screen, color, rect)

    def draw_pieces(self, board):
        """
        Draw all pieces currently on the board.

        Args:
            board (chess.Board): The current game state.
        """
        for sq, piece in board.piece_map().items():
            row = 7 - (sq // 8)
            col = sq % 8
            img = self.images[piece.symbol()]
            pos = (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE // 2)
            rect = img.get_rect(center=pos)
            self.screen.blit(img, rect.topleft)

    def highlight(self, square):
        """
        Highlight legal destination squares for the selected piece.

        Args:
            square (dict): Contains legal moves from a selected square under the key 'moves'.
        """
        # yellow dot on legal destinations
        for move in square['moves']:
            dest = move.to_square
            r = 7 - (dest // 8)
            c = dest % 8
            center = (c * SQUARE_SIZE + SQUARE_SIZE // 2, r * SQUARE_SIZE + SQUARE_SIZE // 2)
            pygame.draw.circle(self.screen, (255, 255, 0), center, SQUARE_SIZE // 6)

    def show_text(self, message):
        """
        Display a centered message on the screen.

        Args:
            message (str): The message to be displayed.
        """
        text = self.font.render(message, True, (255, 255, 255))
        rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, rect)
        
    def animate_move(self, board, piece_img, from_sq, to_sq, duration=0.25):
        """
        Animate a piece moving from one square to another over the specified duration.

        Args:
            board (chess.Board): The current board state.
            piece_img (pygame.Surface): The image of the moving piece.
            from_sq (int): Index of the source square (0–63).
            to_sq (int): Index of the destination square (0–63).
            duration (float): Duration of the animation in seconds (default is 0.25).
        """
        fps = 60
        clock = pygame.time.Clock()
        total_frames = int(duration * fps)

        def sq_to_px(sq):
            """
            Convert board square index to screen pixel coordinates (center of the square).
            """
            row = 7 - (sq // 8)
            col = sq % 8
            return (
                col * SQUARE_SIZE + SQUARE_SIZE // 2,
                row * SQUARE_SIZE + SQUARE_SIZE // 2
            )

        start_pos = sq_to_px(from_sq)
        end_pos   = sq_to_px(to_sq)

        for frame in range(total_frames + 1):
            t = frame / total_frames
            cur_x = start_pos[0] + (end_pos[0] - start_pos[0]) * t
            cur_y = start_pos[1] + (end_pos[1] - start_pos[1]) * t

            # Keep window responsive
            for ev in pygame.event.get():
                if ev.type == pygame.QUIT:
                    pygame.quit()
                    return

            # 1) Draw board
            self.draw_board()

            # 2) Draw all stationary pieces
            for sq, pc in board.piece_map().items():
                if sq == from_sq:
                    continue
                img = self.images[pc.symbol()]
                r = 7 - (sq // 8)
                c = sq % 8
                pos = (c * SQUARE_SIZE + SQUARE_SIZE // 2,
                    r * SQUARE_SIZE + SQUARE_SIZE // 2)
                rect = img.get_rect(center=pos)
                self.screen.blit(img, rect.topleft)

            # 3) Draw the moving piece at its interpolated position
            moving_rect = piece_img.get_rect(center=(cur_x, cur_y))
            self.screen.blit(piece_img, moving_rect.topleft)

            # 4) Show it and wait for next frame
            pygame.display.flip()
            
        clock.tick(fps)