import sys, random, pygame, math, time
from pygame.locals import *  #provides QUIT, KEYDOWN, etc. 


def run_visualisation(sort_type):
    # Add font for the button
    font = pygame.font.Font("assets/pixel_font.ttf", 36)  
    
    
    #initialise pygame and set the window caption
    pygame.init() 
    pygame.display.set_caption('Sorting Algorithm Visualiser')

    #screen size 600x600 px, tower width 2px
    screen_width, screen_height = 600, 600 
    tower_width = 2

    # flags + counters for the sorting process 
    sorting = False
    finished = False 
    sortingindex, finishedindex = 0, 0 
    
    # Add delay timer
    start_time = pygame.time.get_ticks()
    delay_duration = 2000  # 2 seconds in milliseconds

    screen = pygame.display.set_mode((screen_width, screen_height))

    # Button properties
    button_text = "Sort Again"
    button_color = (100, 100, 100)
    button_hover_color = (150, 150, 150)
    button_width, button_height = 250, 50
    button_x = (screen_width - button_width) // 2
    button_y = screen_height - 100
    button_rect = pygame.Rect(button_x, button_y, button_width, button_height)

    # number of towers that fit across the screen 
    num_of_towers = screen_width // tower_width

    #CREATE A ARRAY OF TOWER HEIGHTS 
    towers = []
    for i in range(num_of_towers): 
        towers.append((i+1)*tower_width) #nice sorted array of tower heights
    towers = random.sample(towers, num_of_towers) #shuffles the tower heights array



    #main game loop 
    while True: 
        current_time = pygame.time.get_ticks()
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == KEYDOWN: 
                if event.key == K_UP:
                    towers = random.sample(towers, num_of_towers)
                    sorting, finished = False, False
                    sortingindex, finishedindex = 0, 0
                    # Reset timer when reshuffling
                    start_time = current_time
            
            # Check for button click when sorting is finished
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and finished:
                if button_rect.collidepoint(mouse_pos):
                    return True  # Return to main menu


        # Check if delay has passed before starting sorting
        if not sorting and not finished and current_time - start_time >= delay_duration:
            sorting = True

        if sorting: #SORTING LOGIC 
            if towers == sorted(towers): #if towers are sorted, we have sorted successfully
                sorting = False 
                finished = True

            if sort_type == 'bubble': #performing one pass of a bubble sort on the towers array. will be modularised later
                for j in range(len(towers) - 1):
                    if towers[j] > towers[j + 1]: 
                        towers[j], towers[j + 1] = towers[j + 1], towers[j]


            elif sort_type == 'insertion': #performing one pass of an insertion sort on the towers array. will be modularised later
                if sortingindex < len(towers):
                    key = towers[sortingindex]
                    j = sortingindex - 1
                    while j >= 0 and key < towers[j]:
                        towers[j + 1] = towers[j]
                        j -= 1
                    towers[j + 1] = key
                    sortingindex += 1


            elif sort_type == 'selection': #performing one pass of an insertion sort on the towers array. this will be modularised later
                if sortingindex < len(towers):
                    min_index = sortingindex
                    for j in range(sortingindex + 1, len(towers)):
                        if towers[j] < towers[min_index]:
                            min_index = j
                    towers[sortingindex], towers[min_index] = towers[min_index], towers[sortingindex]
                    sortingindex += 1


        if finished: #DRAWING A GREEN BAR ONCE PER LOOP
            pygame.draw.rect(screen, (0,255,0), (finishedindex*2, screen_height-finishedindex*2, 2, finishedindex*2))
            finishedindex += 1
            
            # Draw "Sort Again" button when sorting is finished
            button_color_current = button_hover_color if button_rect.collidepoint(mouse_pos) else button_color
            pygame.draw.rect(screen, button_color_current, button_rect, border_radius=8)
            
            # Render button text
            text_surface = font.render(button_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=button_rect.center)
            screen.blit(text_surface, text_rect)

        else: #draw black bars on the white screen, representing tower heights
            screen.fill((255,255,255)) # white screen 
            for i in range(len(towers)): #
                pygame.draw.rect(screen, (0,0,0), (i*tower_width, 0, tower_width, screen_height-towers[i]))

        pygame.display.flip() #refresh the screen 
        pygame.time.Clock().tick(100) # sets the fps of the animation to 100 or else
        

