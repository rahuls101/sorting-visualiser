import pygame
import sys

FONT_PATH = "assets/pixel_font.ttf"

def show_menu(screen):
    font = pygame.font.Font(FONT_PATH, 48)
    small_font = pygame.font.Font(FONT_PATH, 32)

    WHITE = (255, 255, 255)
    GRAY = (100, 100, 100)
    BLACK = (0, 0, 0)

    clock = pygame.time.Clock()

    button_texts = [
        "Bubble Sort",
        "Insertion Sort",
        "Selection Sort"
    ]

    # compute the width of the widest button label
    padding_x = 40  # horizontal padding inside buttons
    padding_y = 10  # vertical padding inside buttons
    button_surfaces = [small_font.render(text, True, BLACK) for text in button_texts]
    max_width = max(surface.get_width() for surface in button_surfaces) + padding_x
    button_height = max(surface.get_height() for surface in button_surfaces) + padding_y

    # center buttons horizontally
    screen_width = screen.get_width()
    start_y = 250
    spacing = 20

    buttons = []
    for i, text in enumerate(button_texts):
        x = (screen_width - max_width) // 2
        y = start_y + i * (button_height + spacing)
        rect = pygame.Rect(x, y, max_width, button_height)
        buttons.append((text, rect))

    while True:
        screen.fill(BLACK)

        # Draw title
        title_surface = font.render("Sorting Visualiser", True, WHITE)
        title_rect = title_surface.get_rect(center=(screen_width // 2, 100))
        screen.blit(title_surface, title_rect)

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
                return text.lower().split()[0]  # returns 'bubble', 'insertion', or 'selection'

        pygame.display.flip()
        clock.tick(60)
