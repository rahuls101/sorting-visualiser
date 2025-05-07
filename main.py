import sys, random, pygame, math 
from pygame.locals import *  #provides QUIT, KEYDOWN, etc. 

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
sort_type = '' 

screen = pygame.display.set_mode((screen_width, screen_height))

# number of towers that fit across the screen 
num_of_towers = screen_width // tower_width

#CREATE A ARRAY OF TOWER HEIGHTS 
towers = []
for i in range(num_of_towers): 
    towers.append((i+1)*tower_width) #nice sorted array of tower heights
towers = random.sample(towers, num_of_towers) #shuffles the tower heights array



#main game loop 

while True: 
    for event in pygame.event.get(): #constantly running loop for handling logic and detecting user inputs (events)
        if event.type == QUIT: #user closes window
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN: 
            if event.key == K_UP: #user wants to reshuffle tower heights
                towers = random.sample(towers, num_of_towers)
                sorting, finished = False, False
                sortingindex, finished_index = 0, 0

            elif event.key == K_i:
                sorting = True 
                sort_type = 'insertion'
            elif event.key == K_b: 
                sorting = True 
                sort_type = 'bubble'
            elif event.key == K_s:
                sorting = True
                sort_type = 'selection'

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

    else: #draw black bars on the white screen, representing tower heights
        screen.fill((255,255,255)) # white screen 
        for i in range(len(towers)): #
            pygame.draw.rect(screen, (0,0,0), (i*tower_width, 0, tower_width, screen_height-towers[i]))

    pygame.display.flip() #redraw the screen 
    pygame.time.Clock().tick(100) # sets the fps of the animation to 100 or else

