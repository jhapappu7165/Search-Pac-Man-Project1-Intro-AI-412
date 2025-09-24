# GUI for the eightpuzzle problem. Invokes the problem definition from eightpuzzle_problem.py 
# and BFS from search.py. Can play in either 'Human' mode or 'AI' (search) mode. If 'AI' mode 
# crashes, it's probably because there is no solution.

import pygame
import sys
import random
import time
from eightpuzzle_problem import EightPuzzleSearchProblem, EightPuzzleState
import search

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 600, 700
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
FONT_SIZE = 30
BUTTON_WIDTH = 100
BUTTON_HEIGHT = 50
BUTTON_COLOR = (150, 150, 150)
BUTTON_TEXT_COLOR = (255, 255, 255)
BUTTON_FONT_SIZE = 20
BUTTON_X, BUTTON_Y = WIDTH//2 + BUTTON_WIDTH//2, 10 #HEIGHT - WIDTH

# Function to create the initial board state
def create_board(size, numbers=None):
    if not numbers:
        numbers = list(range(1, size**2)) + [0]  # Create a list of numbers from 1 to n^2-1 and 0 for the empty cell
        random.shuffle(numbers)
    board = [numbers[i:i+size] for i in range(0, size**2, size)]
    return board

# Function to check if the board is solved
def is_solved(board):
    #size = len(board)
    #return all(board[i][j] == i*size + j + 1 for i in range(size) for j in range(size - 1)) and board[size - 1][size - 1] == 0
    current = 0
    for row in range( len(board) ):
        for col in range( len(board) ):
            if current != board[row][col]:
                return False
            current += 1
    return True

# Function to draw the board
def draw_board(screen, board, moves, text_font, cell_font,ai_mode=False):
    screen.fill(WHITE)
    size = len(board)
    cell_size = (HEIGHT - 2 * BUTTON_HEIGHT) // size
    text_height = BUTTON_HEIGHT - BUTTON_FONT_SIZE // 2

    # Draw number of moves & mode at the top
    mode = "AI" if ai_mode else "Human"
    moves_text = text_font.render(f"Moves: {moves}  Mode: {mode}", True, BLACK)
    screen.blit(moves_text, (10, 10))

    # Draw mode toggle button 
    button_rect = pygame.Rect(BUTTON_X, BUTTON_Y, BUTTON_WIDTH*2, BUTTON_HEIGHT)
    pygame.draw.rect(screen, BLUE, button_rect, 1)
    cell_text = text_font.render("Toggle Mode", True, BLACK)
    text_rect = cell_text.get_rect(center=button_rect.center)
    screen.blit(cell_text, text_rect)
    
    # Draw the board cells
    for i in range(size):
        for j in range(size):
            cell_value = board[i][j]
            cell_rect = pygame.Rect(j * cell_size, i * cell_size+2*BUTTON_HEIGHT, cell_size, cell_size)
            pygame.draw.rect(screen, BLACK, cell_rect, 1)
            if cell_value != 0:
                cell_text = cell_font.render(str(cell_value), True, BLACK)
                text_rect = cell_text.get_rect(center=cell_rect.center)
                screen.blit(cell_text, text_rect)

    pygame.display.update()

# Function to perform a move
def move_tile(board, row, col): #return success/failure
    size = len(board)
    empty_row, empty_col = find_empty_cell(board)
    if (abs(row - empty_row) == 1 and col == empty_col) or (abs(col - empty_col) == 1 and row == empty_row):
        board[empty_row][empty_col], board[row][col] = board[row][col], board[empty_row][empty_col]
        return True
    else:
        return False

# Function to find the empty cell
def find_empty_cell(board):
    size = len(board)
    for i in range(size):
        for j in range(size):
            if board[i][j] == 0:
                return i, j

# Function to solve the puzzle using AI
def solve_puzzle(inp_board):
    print("Initial config:", inp_board,"\nSearching...")
    puzzle = EightPuzzleState(sum(inp_board, []))
    problem = EightPuzzleSearchProblem(puzzle)
    path = search.breadthFirstSearch(problem) #To do: Try A* with a good heuristic for 4X4 or larger
    print('BFS found a path of %d moves: %s' % (len(path), str(path)))

    board = inp_board.copy()
    directions = {'up': (-1,0), 'down': (1,0), 'left': (0,-1), 'right': (0,1)}
    moves = []
    empty_row, empty_col = find_empty_cell(board)
    for move in path:
        dx, dy = directions[move]
        empty_row += dx
        empty_col += dy
        moves.append((empty_row, empty_col))
    return moves

# Main function
def main(size):
    # Initialize the display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption(f"{size}x{size} Sliding Tile Puzzle")

    # Create fonts
    text_font = pygame.font.SysFont(None, FONT_SIZE)
    cell_font = pygame.font.SysFont(None, FONT_SIZE * 2)

    # Create the initial board state
    #board = create_board(size, [4, 3, 2, 7, 0, 5, 1, 6, 8]) #Initialize with known config
    board = create_board(size) #Initialize randomly (Beware, may have no solution)

    # Variables
    moves = 0
    solved = is_solved(board)
    ai_mode = False
    draw_board(screen, board, moves, text_font, cell_font)

    # Main game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if not solved:
                    x, y = pygame.mouse.get_pos()
                    if x >= BUTTON_WIDTH and y >= BUTTON_HEIGHT:
                        row = (y - BUTTON_HEIGHT) // ((HEIGHT - BUTTON_HEIGHT) // size)
                        col = (x - BUTTON_WIDTH) // ((WIDTH - BUTTON_WIDTH) // size)
                        if move_tile(board, row, col): 
                            moves += 1
                            solved = is_solved(board)
                    elif BUTTON_X <= x <= BUTTON_X+BUTTON_WIDTH*2 and BUTTON_Y <= y <= BUTTON_Y+BUTTON_WIDTH:
                        ai_mode = not ai_mode
                        if ai_mode:
                            moves = 0
                            draw_board(screen, board, moves, text_font, cell_font, ai_mode)
                            move_list = solve_puzzle(board)
                            if len(move_list)<=0:
                                print("No solution!")
                                sys.exit()
                            for m in move_list:
                                move_tile(board, m[0], m[1])
                                moves += 1
                                draw_board(screen, board, moves, text_font, cell_font, ai_mode)
                                time.sleep(2)
                            solved = is_solved(board)
                draw_board(screen, board, moves, text_font, cell_font, ai_mode)

        # Check if the puzzle is solved
        if solved:
            font = pygame.font.SysFont(None, FONT_SIZE)
            txt_str = "Done!" if ai_mode else "Congratulations! Puzzle Solved."
            text = font.render(txt_str, True, BLUE)
            text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            screen.blit(text, text_rect)
            pygame.display.update()

# Run the main function
if __name__ == "__main__":
    main(3)  # Change the argument to set the size of the puzzle (e.g., 3 for a 3x3 puzzle)
