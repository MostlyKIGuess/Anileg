import pygame
import pygame_gui
import subprocess

# Initialize Pygame and Pygame GUI
pygame.init()
pygame.display.set_caption('Anileg')
screen = pygame.display.set_mode((1280, 1024))
manager = pygame_gui.UIManager((1280, 1024))

# Create a dictionary to store the buttons
buttons = {}

# Create the buttons for the main menu
buttons['LA'] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((590, 200), (100, 50)),
                                             text='LA',
                                             manager=manager,
                                             object_id='#LA')
buttons['IC'] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((590, 300), (100, 50)),
                                             text='IC',
                                             manager=manager,
                                             object_id='#IC')
buttons['AEC'] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((590, 400), (100, 50)),
                                              text='AEC',
                                              manager=manager,
                                              object_id='#AEC')
buttons['TECHNO TRIB'] = pygame_gui.elements.UIButton(relative_rect=pygame.Rect((590, 500), (100, 50)),
                                                      text='TECHNO TRIB',
                                                      manager=manager,
                                                      object_id='#TECHNO_TRIB')


# ...
# Main loop
running = True
while running:
    time_delta = pygame.time.Clock().tick(60)/1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.USEREVENT:
            if event.user_type == pygame_gui.UI_BUTTON_PRESSED:
                if event.ui_element == buttons['LA']:
                    subprocess.run(['python3', 'LA.py'])
                elif event.ui_element == buttons['IC']:
                    subprocess.run(['python3', 'IC.py'])
                elif event.ui_element == buttons['AEC']:
                    subprocess.run(['python3', 'AEC.py'])
                elif event.ui_element == buttons['TECHNO TRIB']:
                    subprocess.run(['python3', 'techno.py'])

        manager.process_events(event)

    manager.update(time_delta)

    screen.fill((222, 166, 129))
    manager.draw_ui(screen)

    pygame.display.update()

pygame.quit()