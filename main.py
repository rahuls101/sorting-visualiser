import pygame
from menu import show_menu
from visualiser import run_visualisation

pygame.init()

if __name__ == "__main__":
    running = True
    
    while running:
        screen = pygame.display.set_mode((800, 600))
        pygame.display.set_caption("Sorting Visualiser")

        selected_sort = show_menu(screen)

        if selected_sort:  # If user clicked a sort button
            # If run_visualisation returns True, we'll loop back to the menu
            # If it returns None/False (e.g., user quits), we'll exit
            return_to_menu = run_visualisation(selected_sort)
            if not return_to_menu:
                running = False


