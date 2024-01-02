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

# Define the input boxes

input_box_positions = [(50, 0, 200, 200), (200, 0, 200, 200), (50, 110, 200, 200), (200, 110, 200, 200)]
input_boxes = [pygame.Rect(x, y, w, h) for x, y, w, h in input_box_positions]

# Initialize the text in the input boxes
text = ['' for _ in input_boxes]

# Define the font for the text
font = pygame.font.Font(None, 32)

image2d = pygame.image.load('images/2D.png')   

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
                    matrix = np.array([float(t) for t in text]).reshape((2, 2))

                    # Create a Manim scene that performs the linear transformation
                    class LinearTransformationExample(Scene):
                        def construct(self):
                            plane = NumberPlane(x_range=[-10,10,1], y_range=[-10,10,1], x_length=9, y_length=9)
                            original_plane = plane.copy().set_opacity(0.15)
                            original_plane.color = WHITE
                            i_hat = Arrow(plane.c2p(0, 0), plane.c2p(1, 0), color=RED).set_opacity(1)
                            j_hat = Arrow(plane.c2p(0, 0), plane.c2p(0, 1), color=GREEN).set_opacity(1)
                            self.add(i_hat, j_hat)
                            transform_plane = ApplyMatrix(matrix, plane)
                            transform_i_hat = ApplyMatrix(matrix, i_hat)
                            transform_j_hat = ApplyMatrix(matrix, j_hat)
                            self.play(transform_plane, transform_i_hat, transform_j_hat, run_time=7)
                            
                            self.add(original_plane)
                            self.wait(4)

                    # threading.Thread(target=lambda: LinearTransformationExample().render()).start()
                    def render_and_play():
                            scene = LinearTransformationExample()
                            scene.render()
                            time.sleep(1)
                            clip = VideoFileClip("media/videos/1080p60/LinearTransformationExample.mp4")
                            clip.preview(fps=60)
                    threading.Thread(target=render_and_play).start()
                    # TODO: Play the video in the Pygame window
                else:
                    if event.key == K_BACKSPACE:
                        text[active_box] = text[active_box][:-1]
                    else:
                        text[active_box] += event.unicode

    screen_width, screen_height = screen.get_size()

    # Calculate the center position of the screen
    center_x = screen_width // 2
    center_y = screen_height // 2
    
    # Define the relative positions of the input boxes
    relative_input_box_positions = [(-60, -30), (180, -30), (-60, 30), (180, 30)]

    # Calculate the actual positions of the input boxes
    input_box_positions = [(center_x + x, center_y + y) for x, y in relative_input_box_positions]

    # Create the input boxes at the calculated positions
    input_boxes = [pygame.Rect(x, y, 100, 100) for x, y in input_box_positions]

    # Draw the input boxes and the text
    for i, box in enumerate(input_boxes):
        pygame.draw.rect(screen, (255, 255, 255) if i == active_box else (127, 127, 127), box)
        txt_surface = font.render(text[i], True, (0, 0, 0))
        screen.blit(txt_surface, (box.x+5, box.y+5))
    
    def render_multiline_text(surface, text, pos, font, color=pygame.Color('white')):
        lines = text.split('\n')
        for i, line in enumerate(lines):
            line_surface = font.render(line, True, color)
            surface.blit(line_surface, (pos[0], pos[1] + 18*i))


    # Define the relative positions of the labels
    relative_label_positions = [(-100, 100), (200, 100), (-100, 300), (200, 300)]

    # Calculate the actual positions of the labels
    label_positions = [(center_x + x, center_y + y) for x, y in relative_label_positions]

    # Draw the matrix labels
    label_font = pygame.font.Font(None, 18)
    labels = ['[', ']', '[', ']']
    for label, pos in zip(labels, label_positions):
        label_surface = label_font.render(label, True, (255, 255, 255))
        screen.blit(label_surface, pos)
        
     
     
    info_text = """
    You see, it's common to package these four numbers which characterize a given transformation into a 2x2 grid of numbers \n, called a “2-by-2 matrix”, where you can interpret the columns as the two special vectors where î and ĵ land.
    """
    
    
    # render_multiline_text(screen, info_text, (10, 10), pygame.font.Font("fonts/Roboto-Regular.ttf", 22))
    
    
    # Update the display
    pygame.display.flip()