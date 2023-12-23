import pygame
import pygame_gui
import subprocess
# Initialize Pygame and Pygame GUI
pygame.init()
pygame.display.set_caption('LA')
screen = pygame.display.set_mode((1280, 1024))
manager = pygame_gui.UIManager((1280, 1024))

# Change the background color
screen.fill((222, 166, 129))

# Calculate the center of the screen
center_x = screen.get_width() // 2
center_y = screen.get_height() // 2

# Define the size of the buttons
button_width = 200
button_height = 50

# Create the buttons
buttons = {}
buttons['2D Transformation'] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((center_x - button_width // 2, center_y - 3 * button_height), (button_width, button_height)),
                                                            text='2D Transformation',
                                                            manager=manager,
                                                            object_id='#2D')
buttons['3D Transformation'] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((center_x - button_width // 2, center_y - button_height), (button_width, button_height)),
                                                            text='3D Transformation',
                                                            manager=manager,
                                                            object_id='#3D')
buttons['Dot Product'] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((center_x - button_width // 2, center_y + button_height), (button_width, button_height)),
                                                      text='Dot Product',
                                                      manager=manager,
                                                      object_id='#Dot')



# Main loop
running = True
while running:
    time_delta = pygame.time.Clock().tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == buttons['2D Transformation']:
                    subprocess.run(['python3', 'LA/2Dtrans.py'])
        manager.process_events(event)

        if event.type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == buttons['3D Transformation']:
                    subprocess.run(['python3', 'LA/3Dtrans.py'])
        manager.process_events(event)
        
        
        

    manager.update(time_delta)

    screen.fill((222, 166, 129))
    manager.draw_ui(screen)

    pygame.display.update()

pygame.quit()