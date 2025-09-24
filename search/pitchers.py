# GUI for the pitchers problem. Invokes the problem definition from pitchers_problem.py 
# and BFS from search.py. You can change the problem instance in line 199.

import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (170, 170, 255)
FONT_SIZE = 30
PITCHER_WIDTH = 70
PITCHER_HEIGHT = 300
ARROW_LENGTH = 30

# Function to create a pitcher
def create_pitcher(capacity):
    return {'capacity': capacity, 'current': 0}

# Function to fill a pitcher
def fill_pitcher(pitcher):
    pitcher['current'] = pitcher['capacity']

# Function to empty a pitcher
def empty_pitcher(pitcher):
    pitcher['current'] = 0

# Function to pour from one pitcher to another
def pour_pitcher(source, target):
    space_available = target['capacity'] - target['current']
    if source['current'] <= space_available:
        target['current'] += source['current']
        source['current'] = 0
    else:
        source['current'] -= space_available
        target['current'] = target['capacity']

def draw_arrow(
        surface: pygame.Surface,
        start: pygame.Vector2,
        end: pygame.Vector2,
        color: pygame.Color,
        body_width: int = 4,
        head_width: int = 20,
        head_height: int = 10,
    ):
    """Draw an arrow between start and end with the arrow head at the end.

    Args:
        surface (pygame.Surface): The surface to draw on
        start (pygame.Vector2): Start position
        end (pygame.Vector2): End position
        color (pygame.Color): Color of the arrow
        body_width (int, optional): Defaults to 2.
        head_width (int, optional): Defaults to 4.
        head_height (float, optional): Defaults to 2.
    """
    arrow = start - end
    angle = arrow.angle_to(pygame.Vector2(0, -1))
    body_length = arrow.length() - head_height

    # Create the triangle head around the origin
    head_verts = [
        pygame.Vector2(0, head_height / 2),  # Center
        pygame.Vector2(head_width / 2, -head_height / 2),  # Bottomright
        pygame.Vector2(-head_width / 2, -head_height / 2),  # Bottomleft
    ]
    # Rotate and translate the head into place
    translation = pygame.Vector2(0, arrow.length() - (head_height / 2)).rotate(-angle)
    for i in range(len(head_verts)):
        head_verts[i].rotate_ip(-angle)
        head_verts[i] += translation
        head_verts[i] += start

    pygame.draw.polygon(surface, color, head_verts)

    # Stop weird shapes when the arrow is shorter than arrow head
    if arrow.length() >= head_height:
        # Calculate the body rect, rotate and translate into place
        body_verts = [
            pygame.Vector2(-body_width / 2, body_length / 2),  # Topleft
            pygame.Vector2(body_width / 2, body_length / 2),  # Topright
            pygame.Vector2(body_width / 2, -body_length / 2),  # Bottomright
            pygame.Vector2(-body_width / 2, -body_length / 2),  # Bottomleft
        ]
        translation = pygame.Vector2(0, body_length / 2).rotate(-angle)
        for i in range(len(body_verts)):
            body_verts[i].rotate_ip(-angle)
            body_verts[i] += translation
            body_verts[i] += start

        pygame.draw.polygon(surface, color, body_verts)
        
# Function to draw the pitchers and explain moves
def draw_pitchers(screen, pitchers, moves, move_index):
    screen.fill(WHITE)
    num_pitchers = len(pitchers)
    gap = WIDTH // (num_pitchers + 1)
 
    for i, pitcher in enumerate(pitchers):
        x = (i + 1) * gap - PITCHER_WIDTH // 2
        pygame.draw.rect(screen, BLACK, (x, HEIGHT - PITCHER_HEIGHT, PITCHER_WIDTH, PITCHER_HEIGHT), 2)

        # Calculate the filled height of the pitcher
        filled_height = PITCHER_HEIGHT * pitcher['current'] // pitcher['capacity']
        pygame.draw.rect(screen, BLUE, (x, HEIGHT - filled_height, PITCHER_WIDTH, filled_height))

        # Display capacity and current amount
        font = pygame.font.SysFont(None, FONT_SIZE)
        text = font.render(f"{pitcher['current']}/{pitcher['capacity']}", True, BLACK)
        text_rect = text.get_rect(center=(x + PITCHER_WIDTH // 2, HEIGHT - PITCHER_HEIGHT // 2))
        screen.blit(text, text_rect)

        # Draw arrows for moves
        if move_index < len(moves) - 1:
            move = moves[move_index+1]
            if move.startswith('f:'):
                fill_index = int(move.split(':')[1])
                if fill_index == i:
                    top_text = font.render(f"Next move: Fill {fill_index}", True, BLACK)
                    text_rect = top_text.get_rect(center=(WIDTH // 2,50))
                    screen.blit(top_text, text_rect)
                    pygame.draw.polygon(screen, BLACK, [(x + PITCHER_WIDTH // 2, HEIGHT - PITCHER_HEIGHT - ARROW_LENGTH),
                                                         (x + PITCHER_WIDTH // 2 - 10, HEIGHT - PITCHER_HEIGHT - 10),
                                                         (x + PITCHER_WIDTH // 2 + 10, HEIGHT - PITCHER_HEIGHT - 10)])
            elif move.startswith('e:'):
                empty_index = int(move.split(':')[1])
                if empty_index == i:
                    top_text = font.render(f"Next move: Empty {empty_index}", True, BLACK)
                    text_rect = top_text.get_rect(center=(WIDTH // 2,50))
                    screen.blit(top_text, text_rect)
                    pygame.draw.polygon(screen, BLACK, [(x + PITCHER_WIDTH // 2, HEIGHT - PITCHER_HEIGHT + ARROW_LENGTH),
                                                         (x + PITCHER_WIDTH // 2 - 10, HEIGHT - PITCHER_HEIGHT + 10),
                                                         (x + PITCHER_WIDTH // 2 + 10, HEIGHT - PITCHER_HEIGHT + 10)])
            elif move.startswith('p:'):
                source_index, target_index = map(int, move.split(':')[1:])
                if source_index == i:
                    top_text = font.render(f"Next move: Pour {source_index} to {target_index}", True, BLACK)
                    text_rect = top_text.get_rect(center=(WIDTH // 2,50))
                    screen.blit(top_text, text_rect)
                    draw_arrow(screen, pygame.Vector2(x + PITCHER_WIDTH // 2, HEIGHT - PITCHER_HEIGHT - ARROW_LENGTH), pygame.Vector2((target_index + 1) * gap - PITCHER_WIDTH // 2, HEIGHT - PITCHER_HEIGHT - ARROW_LENGTH), BLUE)
 
    pygame.display.update()

# Main function
def main(capacities, moves):
    # Initialize the display
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Pitchers Puzzle")

    # Create the pitchers
    pitchers = [create_pitcher(capacity) for capacity in capacities]

    # Main game loop
    running = True
    move_index = -1

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if move_index < len(moves)-1:
            draw_pitchers(screen, pitchers, moves, move_index)
            move_index += 1
            pygame.time.wait(5000)
            move = moves[move_index]
            if move.startswith('f:'):
                pitcher_index = int(move.split(':')[1])
                fill_pitcher(pitchers[pitcher_index])
            elif move.startswith('e:'):
                pitcher_index = int(move.split(':')[1])
                empty_pitcher(pitchers[pitcher_index])
            elif move.startswith('p:'):
                source_index, target_index = map(int, move.split(':')[1:])
                pour_pitcher(pitchers[source_index], pitchers[target_index])
        if move_index >= len(moves)-1:
            draw_pitchers(screen, pitchers, moves, move_index)
            pygame.time.wait(2000)
            running = False

    # Check if all pitchers have the desired amount
    font = pygame.font.SysFont(None, FONT_SIZE)
    text = font.render("Desired amount achieved!", True, BLACK)
    text_rect = text.get_rect(center=(WIDTH // 2, 100))
    screen.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(3000)  # Display message for 3 seconds

# Run the main function
from pitchers_problem import PitchersState, PitchersPuzzleSearchProblem
import search
if __name__ == "__main__":
    puzzle = PitchersState([4, 5, 3, 0, 0]) #[1, 3, 8, 12, 0, 0, 0]) #[1, 2, 5, 10, 0, 0, 0])
    problem = PitchersPuzzleSearchProblem(puzzle)
    path = search.breadthFirstSearch(problem)
    print('BFS found a path of %d moves: %s' % (len(path), str(path)))
    main(puzzle.capacities, path)
