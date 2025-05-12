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

    # Rainbow colors for the towers
    rainbow_colors = [
        (255, 0, 0),    # Red
        (255, 127, 0),  # Orange
        (255, 255, 0),  # Yellow
        (0, 255, 0),    # Green
        (0, 0, 255),    # Blue
        (75, 0, 130),   # Indigo
        (148, 0, 211)   # Violet
    ]
    
    # Function to get color based on tower position in sorted array
    def get_tower_color(index, total_towers):
        # Map the position to a color in the rainbow
        # Use total_towers instead of total_towers-1 to ensure full range
        position = index / total_towers
        
        # Calculate which color in the rainbow array
        # Adjust to ensure we use the full color range including the last color
        color_index = min(int(position * len(rainbow_colors)), len(rainbow_colors) - 1)
        return rainbow_colors[color_index]

    # flags + counters for the sorting process 
    sorting = False
    finished = False 
    sortingindex, finishedindex = 0, 0 

    #specifically for comb sort: 
    gap = screen_width // tower_width #starting gap is size of the list
    shrink_factor = 1.3 #used in comb sort
    swapped = False #to track if any swaps were made
    pass_counter = 0 
    
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

    # Get the maximum tower height for color mapping
    max_tower_height = max(towers)



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
            if towers == sorted(towers): #if towers are sorted, we have sorted successfully. 
                sorting = False 
                finished = True

            if sort_type == 'bubble': #performing one pass of a bubble sort on the towers array.
                for j in range(len(towers) - 1):
                    if towers[j] > towers[j + 1]: 
                        towers[j], towers[j + 1] = towers[j + 1], towers[j]


            elif sort_type == 'insertion': #performing one pass of an insertion sort on the towers array.
                if sortingindex < len(towers):
                    key = towers[sortingindex]
                    j = sortingindex - 1
                    while j >= 0 and key < towers[j]:
                        towers[j + 1] = towers[j]
                        j -= 1
                    towers[j + 1] = key
                    sortingindex += 1


            elif sort_type == 'selection': #performing one pass of an insertion sort on the towers array. 
                if sortingindex < len(towers):
                    min_index = sortingindex
                    for j in range(sortingindex + 1, len(towers)):
                        if towers[j] < towers[min_index]:
                            min_index = j
                    towers[sortingindex], towers[min_index] = towers[min_index], towers[sortingindex]
                    sortingindex += 1

            elif sort_type == 'comb': #performing a certain number of passes of a comb sort on the towers array. this is complicated
                if gap > 1:
                    gap = int(gap / shrink_factor)
                else:
                    gap = 1  # gap shouldn't go below 1

                '''
                the nature of comb sort means that it is quick towards the beginning, yet slow towards the end. however, the 
                visual process of this nature is not very visually appealing. therefore, we will implement a 'speed up' system, 
                where the number of operations performed per frame increases exponentially, creating a more visually appealing effect
                but still allowing viewers to see the beginning, more chaotic, nature of the sort.
                '''

                operations_per_frame = int(5 * (1.25 ** pass_counter)) 
                pass_counter += 0.02

                count = 0
                while sortingindex < len(towers) - gap and count < operations_per_frame:
                    if towers[sortingindex] > towers[sortingindex + gap]:
                        towers[sortingindex], towers[sortingindex + gap] = towers[sortingindex + gap], towers[sortingindex]
                        swapped = True
                    sortingindex += 1
                    count += 1

                # Once a full pass with the current gap is done, reset the gap and pass counter. 
                if sortingindex >= len(towers) - gap:
                    if gap == 1 and not swapped:
                        sorting = False
                        finished = True
                    else:
                        sortingindex = 0
                        swapped = False  # reset for the next pass


        if finished: #DRAWING A WHITE BAR ONCE PER LOOP
            pygame.draw.rect(screen, (255,255,255), (finishedindex*2, screen_height-finishedindex*2, 2, finishedindex*2))
            finishedindex += 1
            
            # Draw "Sort Again" button when sorting is finished
            button_color_current = button_hover_color if button_rect.collidepoint(mouse_pos) else button_color
            pygame.draw.rect(screen, button_color_current, button_rect, border_radius=8)
            
            # Render button text
            text_surface = font.render(button_text, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=button_rect.center)
            screen.blit(text_surface, text_rect)

        else: #draw colored bars on black background
            screen.fill((0, 0, 0)) # black background
            for i in range(len(towers)):
                # The tower height determines the height of the bar
                height = towers[i]
                
                # Get the position this tower would have in a sorted array
                sorted_position = sorted(towers).index(height)
                while sorted_position < len(towers) - 1 and sorted(towers)[sorted_position+1] == height:
                    sorted_position += 1
                    
                # Get color based on the tower's position in a sorted array
                # Use len(towers) instead of len(towers)-1 for better distribution
                tower_color = get_tower_color(sorted_position, len(towers))
                
                # Draw the colored tower
                pygame.draw.rect(screen, tower_color, (i*tower_width, screen_height-height, tower_width, height))

        pygame.display.flip() #refresh the screen 
        pygame.time.Clock().tick(100) # sets the fps of the animation to 100 
        

