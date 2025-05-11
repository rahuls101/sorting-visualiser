import pygame
from menu import show_menu
from visualiser import run_visualisation

pygame.init()

if __name__ == "__main__":
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Sorting Visualiser")

    selected_sort = show_menu(screen)

    if selected_sort:  # If user clicked a sort button
        run_visualisation(selected_sort)


