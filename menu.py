import pygame
import sys
import os 


def show_menu(screen):
    current_dir = os.path.dirname(__file__)
    font = pygame.font.Font(os.path.join(current_dir, "assets", "pixel_font.ttf"), 70)
    credit_font = pygame.font.Font(os.path.join(current_dir, "assets", "pixel_font.ttf"), 55)
    small_font = pygame.font.Font(os.path.join(current_dir, "assets", "pixel_font.ttf"), 40)

    WHITE = (255, 255, 255)
    GRAY = (100, 100, 100)
    BLACK = (0, 0, 0)

    clock = pygame.time.Clock()
    
    # Rainbow colors
    rainbow_colors = [
        (255, 0, 0),    # Red
        (255, 127, 0),  # Orange
        (255, 255, 0),  # Yellow
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (75, 0, 130),   # Indigo
        (148, 0, 211)   # Violet
    ]

    button_texts = [
        "Bubble Sort",
        "Insertion Sort",
        "Selection Sort",
        "Comb Sort"
    ]

    # compute the width of the widest button label
    padding_x = 40  # horizontal padding inside buttons
    padding_y = 10  # vertical padding inside buttons
    button_surfaces = [small_font.render(text, True, BLACK) for text in button_texts]
    max_width = max(surface.get_width() for surface in button_surfaces) + padding_x
    button_height = max(surface.get_height() for surface in button_surfaces) + padding_y

    # center buttons horizontally
    screen_width = screen.get_width()
    start_y = 275
    spacing = 20

    buttons = []
    for i, text in enumerate(button_texts):
        x = (screen_width - max_width) // 2
        y = start_y + i * (button_height + spacing)
        rect = pygame.Rect(x, y, max_width, button_height)
        buttons.append((text, rect))

    while True:
        screen.fill(BLACK)

        # Draw rainbow title
        title_text = "Pygame Sorting Visualiser"
        title_width = font.size(title_text)[0]
        
        # Create a surface for the title
        title_surface = pygame.Surface((title_width, font.get_height()), pygame.SRCALPHA)
        
        # Draw each character with a color from the rainbow
        x_offset = 0
        for i, char in enumerate(title_text):
            # Calculate which color to use based on position in text
            color_idx = int(i * len(rainbow_colors) / len(title_text))
            char_surf = font.render(char, True, rainbow_colors[color_idx])
            title_surface.blit(char_surf, (x_offset, 0))
            x_offset += font.size(char)[0]
        
        # Draw the title
        title_rect = title_surface.get_rect(center=(screen_width // 2, 100))
        screen.blit(title_surface, title_rect)

        # Draw credits to me :)
        credit_surface = credit_font.render("Created by rahuls101", True, WHITE)
        credit_rect = credit_surface.get_rect(center=(screen_width // 2, 175))
        screen.blit(credit_surface, credit_rect)

        mouse_pos = pygame.mouse.get_pos()
        click = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                click = True

        for i, (text, rect) in enumerate(buttons):
            color = GRAY if rect.collidepoint(mouse_pos) else WHITE
            pygame.draw.rect(screen, color, rect, border_radius=8)
            label = button_surfaces[i]
            label_rect = label.get_rect(center=rect.center)
            screen.blit(label, label_rect)

            if click and rect.collidepoint(mouse_pos):
                return text.lower().split()[0]  # returns 'bubble', 'insertion', 'selection', or 'comb'

        pygame.display.flip()
        clock.tick(60)
