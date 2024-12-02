import pygame
import sys

# Initialize pygame
pygame.init()

# Constants
BOARD_WIDTH = 8
BOARD_HEIGHT = 5
TILE_SIZE = 100
SCREEN_WIDTH = BOARD_WIDTH * TILE_SIZE + TILE_SIZE  # Extra for labels
SCREEN_HEIGHT = BOARD_HEIGHT * TILE_SIZE + TILE_SIZE + 50  # Extra for labels and reset button
ROOK_COLOR = (255, 255, 0)  # Yellow for the rook
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LABEL_COLOR = (0, 0, 255)  # Blue for the row/column labels
BACKGROUND_COLOR = (169, 169, 169)  # Gray background

# Player 1 colors
LIGHT_RED = (255, 182, 193)  # Light red for available white squares
DARK_RED = (139, 0, 0)  # Dark red for available black squares

# Player 2 colors
LIGHT_BLUE = (173, 216, 230)  # Light blue for available white squares
DARK_BLUE = (0, 0, 139)  # Dark blue for available black squares

# Button colors
BUTTON_COLOR = (0, 200, 0)
BUTTON_HOVER_COLOR = (0, 255, 0)
BUTTON_TEXT_COLOR = (255, 255, 255)

# Initialize the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Totally Math Club Code to conduct Icebreaker')

# Load font
font = pygame.font.SysFont(None, 40)
popup_font = pygame.font.SysFont(None, 80)  # Increased font size

# Rook's initial position (a1, bottom-left)
rook_x = 0
rook_y = BOARD_HEIGHT - 1

# Game state
current_player = 1  # 1 = Player 1, 2 = Player 2
game_over = False
winner = None
available_moves = []  # To track available moves

# Function to reset the game
def reset_game():
    global rook_x, rook_y, current_player, game_over, winner
    rook_x = 0
    rook_y = BOARD_HEIGHT - 1
    current_player = 1
    game_over = False
    winner = None
    update_available_moves()

# Function to draw the chessboard with labels
def draw_board_with_labels():
    # Draw the chessboard
    for row in range(BOARD_HEIGHT):
        for col in range(BOARD_WIDTH):
            color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, color, (TILE_SIZE + col * TILE_SIZE, TILE_SIZE + row * TILE_SIZE, TILE_SIZE, TILE_SIZE))
    
    # Draw the row numbers (1-5)
    for row in range(BOARD_HEIGHT):
        label = font.render(str(BOARD_HEIGHT - row), True, LABEL_COLOR)
        screen.blit(label, (10, TILE_SIZE + row * TILE_SIZE + TILE_SIZE // 3))

    # Draw the column letters (a-h)
    for col in range(BOARD_WIDTH):
        label = font.render(chr(ord('a') + col), True, LABEL_COLOR)
        screen.blit(label, (TILE_SIZE + col * TILE_SIZE + TILE_SIZE // 3, 10))

# Function to draw the rook
def draw_rook(x, y):
    rook_rect = pygame.Rect(TILE_SIZE + x * TILE_SIZE, TILE_SIZE + y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
    pygame.draw.rect(screen, ROOK_COLOR, rook_rect)

# Function to draw available moves based on the current player
def update_available_moves():
    global available_moves
    available_moves = []

    if current_player == 1:
        light_color = LIGHT_RED
        dark_color = DARK_RED
    else:
        light_color = LIGHT_BLUE
        dark_color = DARK_BLUE

    # Right moves
    for col in range(rook_x + 1, BOARD_WIDTH):
        color = light_color if (rook_y + col) % 2 == 0 else dark_color
        available_moves.append((col, rook_y))
        pygame.draw.rect(screen, color, (TILE_SIZE + col * TILE_SIZE, TILE_SIZE + rook_y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

    # Upward moves
    for row in range(rook_y - 1, -1, -1):
        color = light_color if (row + rook_x) % 2 == 0 else dark_color
        available_moves.append((rook_x, row))
        pygame.draw.rect(screen, color, (TILE_SIZE + rook_x * TILE_SIZE, TILE_SIZE + row * TILE_SIZE, TILE_SIZE, TILE_SIZE))

# Function to move the rook based on clicked square
def move_rook(click_pos):
    global rook_x, rook_y, current_player, game_over, winner

    col = (click_pos[0] - TILE_SIZE) // TILE_SIZE
    row = (click_pos[1] - TILE_SIZE) // TILE_SIZE

    # Only move if the clicked square is an available move
    if (col, row) in available_moves:
        rook_x = col
        rook_y = row

        # Check for win condition (h5 is reached)
        if rook_x == BOARD_WIDTH - 1 and rook_y == 0:
            game_over = True
            winner = current_player

        # Switch players after a move if the game is not over
        if not game_over:
            current_player = 2 if current_player == 1 else 1
            update_available_moves()

# Function to display the winner
def display_winner():
    winner_text = f"Player {winner} Wins!"
    text_surface = popup_font.render(winner_text, True, (255, 255, 0))  # Bright yellow for popup
    background_rect = pygame.Rect(SCREEN_WIDTH // 2 - 300, SCREEN_HEIGHT // 2 - 100, 600, 200)  # Background for better visibility
    pygame.draw.rect(screen, (0, 0, 0), background_rect)  # Black background for contrast
    screen.blit(text_surface, (background_rect.x + 50, background_rect.y + 50))

# Function to draw the reset button
def draw_reset_button():
    button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 80, 200, 40)
    mouse_pos = pygame.mouse.get_pos()
    color = BUTTON_HOVER_COLOR if button_rect.collidepoint(mouse_pos) else BUTTON_COLOR
    pygame.draw.rect(screen, color, button_rect)
    button_text = font.render("Reset", True, BUTTON_TEXT_COLOR)
    screen.blit(button_text, (button_rect.x + 50, button_rect.y + 5))
    return button_rect

# Main loop
def main():
    global running
    running = True
    reset_game()  # Initialize the game state
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN and not game_over:
                if TILE_SIZE < event.pos[0] < SCREEN_WIDTH and TILE_SIZE < event.pos[1] < SCREEN_HEIGHT:
                    move_rook(event.pos)

            elif game_over:
                # Check if the reset button was clicked
                reset_button_rect = draw_reset_button()  # Draw the button and get its rect
                try:
                    if reset_button_rect.collidepoint(event.pos):
                        reset_game()
                except:
                    pass

        # Draw the background
        screen.fill(BACKGROUND_COLOR)

        # Draw the board, labels, rook, and available moves
        draw_board_with_labels()
        update_available_moves()
        draw_rook(rook_x, rook_y)

        # Display the winner if the game is over
        if game_over:
            display_winner()
            draw_reset_button()  # Ensure reset button is drawn after the game ends

        pygame.display.flip()

    pygame.quit()

# Run the game
if __name__ == "__main__":
    main()
