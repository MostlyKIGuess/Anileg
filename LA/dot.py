import pygame
import numpy as np
from manim import *
from pygame.locals import *
import threading
from moviepy.editor import VideoFileClip
import time


# Initialize Pygame
pygame.init()

# Create a display surface
screen = pygame.display.set_mode((1920, 1080))



screen_width, screen_height = screen.get_size()


center_x = screen_width // 2
center_y = screen_height // 2


relative_input_box_positions = [(-60, -30), (60, -30), (-60, 30), (60, 30), (-60, 60), (60, 60)]


input_box_positions = [(center_x + x, center_y + y) for x, y in relative_input_box_positions]


input_boxes = [pygame.Rect(x, y, 100, 100) for x, y in input_box_positions]

# Initialize the text in the input boxes
text = ['' for _ in input_boxes]

# Define the font for the text
font = pygame.font.Font(None, 32)

image2d = pygame.image.load('images/dot.png')   

# Get the size of the screen
screen_width, screen_height = screen.get_size()

    # Calculate the center position of the screen
center_x = screen_width // 2
center_y = screen_height // 2

screen.fill((17, 17, 17))
screen.blit(image2d, (150, center_y - 500))

# Game loop
clock = pygame.time.Clock()
running = True
active_box = None  # To keep track of the active input box
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False
        elif event.type == MOUSEBUTTONDOWN:
            for i, box in enumerate(input_boxes):
                if box.collidepoint(event.pos):
                    active_box = i
                    break
            else:
                active_box = None
        elif event.type == KEYDOWN:
            if active_box is not None:
                if event.key == K_RETURN:
                    # Convert the input to a matrix
                    vector_a = np.array([float(t) for t in text[:3]])
                    vector_b = np.array([float(t) for t in text[3:6]])

                    # Calculate the dot product
                    dot_product = np.dot(vector_a, vector_b)

                    # Display the dot product
                    print(f"The dot product is {dot_product}")

    #drawing input boxes
   
    for i, box in enumerate(input_boxes):
        pygame.draw.rect(screen, (255, 255, 255) if i == active_box else (127, 127, 127), box)
        txt_surface = font.render(text[i], True, (0, 0, 0))
        screen.blit(txt_surface, (box.x+5, box.y+5))


    pygame.display.flip()