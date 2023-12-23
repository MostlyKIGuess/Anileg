import pygame
import numpy as np
from manim import *
from pygame.locals import *
import threading
from moviepy.editor import VideoFileClip
import time
from manim import config

config["quality"] = "medium_quality"

# Initialize Pygame
pygame.init()


# Create a display surface
screen = pygame.display.set_mode((1920, 1080))
screen_width, screen_height = screen.get_size()

    # Calculate the center position of the screen
center_x = screen_width // 2
center_y = screen_height // 2



relative_input_box_positions = [(-60, -30, 100, 50), (60, -30, 100, 50), (180, -30, 100, 50),
                                (-60, 30, 100, 50), (60, 30, 100, 50), (180, 30, 100, 50),
                                (-60, 90, 100, 50), (60, 90, 100, 50), (180, 90, 100, 50)]

# Calculate the actual positions of the input boxes
input_box_positions = [(center_x + x, center_y + y, w, h) for x, y, w, h in relative_input_box_positions]
input_boxes = [pygame.Rect(x, y, w, h) for x, y, w, h in input_box_positions]

# Initialize the text in the input boxes
text = ['' for _ in input_boxes]


# Define the font for the text
font = pygame.font.Font(None, 32)

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
                    matrix = np.array([float(t) for t in text]).reshape((3, 3))

                    # Create a Manim scene that performs the linear transformation
                    class Linear3DTransformationExample(ThreeDScene):
                        def construct(self):
                               CONFIG = {
                            "x_axis_label": "$x$",
                            "y_axis_label": "$y$",
                            "basis_i_color": GREEN,
                            "basis_j_color": RED,
                            "basis_k_color": GOLD
                        }
                        def __init__(self,matrix):
                            self.matrix = matrix
                            self.basis_i_color = GREEN
                            self.basis_j_color = RED
                            self.basis_k_color = BLUE
                            super().__init__()
                        

                        def create_matrix(self, np_matrix):

                            m = Matrix(np_matrix)

                            m.scale(0.5)
                            m.set_column_colors(self.basis_i_color, self.basis_j_color, self.basis_k_color)

                            m.to_corner(UP + LEFT)

                            return m

                        def construct(self):

                            M = self.matrix

                            axes = ThreeDAxes()
                            axes.set_color(GRAY)
                            axes.add(axes.get_axis_labels())

                            self.set_camera_orientation(phi=75 * DEGREES, theta=-45 * DEGREES)

                            # # basis vectors i,j,k
                            basis_vector_helper = Tex("$i$", ",", "$j$", ",", "$k$")
                            basis_vector_helper[0].set_color(self.basis_i_color)
                            basis_vector_helper[2].set_color(self.basis_j_color)
                            basis_vector_helper[4].set_color(self.basis_k_color)

                            basis_vector_helper.to_corner(UP + RIGHT)

                            self.add_fixed_in_frame_mobjects(basis_vector_helper)

                            # matrix
                            matrix = self.create_matrix(M)

                            self.add_fixed_in_frame_mobjects(matrix)

                            # axes & camera
                            self.add(axes)

                            self.begin_ambient_camera_rotation(rate=0.2)

                            cube = Cube(side_length=1, fill_color=BLUE, stroke_width=2, fill_opacity=0.1)
                            cube.set_stroke(BLUE_E)

                            i_vec = Vector(np.array([1, 0, 0]), color=self.basis_i_color)
                            j_vec = Vector(np.array([0, 1, 0]), color=self.basis_j_color)
                            k_vec = Vector(np.array([0, 0, 1]), color=self.basis_k_color)

                            i_vec_new = Vector(M @ np.array([1, 0, 0]), color=self.basis_i_color)
                            j_vec_new = Vector(M @ np.array([0, 1, 0]), color=self.basis_j_color)
                            k_vec_new = Vector(M @ np.array([0, 0, 1]), color=self.basis_k_color)

                            self.play(
                                ShowCreationThenFadeOut(cube),
                                GrowArrow(i_vec),
                                GrowArrow(j_vec),
                                GrowArrow(k_vec),
                                Write(basis_vector_helper)
                            )

                            self.wait()

                            matrix_anim = ApplyMatrix(M, cube)

                            self.play(
                                matrix_anim,
                                Transform(i_vec, i_vec_new, rate_func=matrix_anim.get_rate_func(),
                                        run_time=5),
                                Transform(j_vec, j_vec_new, rate_func=matrix_anim.get_rate_func(),
                                        run_time=5),
                                Transform(k_vec, k_vec_new, rate_func=matrix_anim.get_rate_func(),
                                        run_time=5)
                            )

                            self.wait()
                            self.wait(4)

                    # threading.Thread(target=lambda: LinearTransformationExample().render()).start()
                    def render_and_play():
                            scene = Linear3DTransformationExample(matrix)
                            scene.render()
                            time.sleep(1)
                            clip = VideoFileClip("media/videos/720p30/Linear3DTransformationExample.mp4")
                            clip.preview(fps=60)
                    threading.Thread(target=render_and_play).start()
                    # TODO: Play the video in the Pygame window
                else:
                    if event.key == K_BACKSPACE:
                        text[active_box] = text[active_box][:-1]
                    else:
                        text[active_box] += event.unicode

   
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

    # Get the size of the screen
    screen_width, screen_height = screen.get_size()

    # Calculate the center position of the screen
    center_x = screen_width // 2
    center_y = screen_height // 2

    # Define the relative positions of the labels
    relative_label_positions = [(-60, -30), (180, -30), (-60, 30), (180, 30)]

    # Calculate the actual positions of the labels
    label_positions = [(center_x + x, center_y + y) for x, y in relative_label_positions]

    # Draw the matrix labels
    label_font = pygame.font.Font(None, 18)
    labels = ['[', ']', '[', ']']
    for label, pos in zip(labels, label_positions):
        label_surface = label_font.render(label, True, (255, 255, 255))
        screen.blit(label_surface, pos)
        
    info_text = """
    Lorem asfknlaskf aasla aal kjfl kaf lakff \n asfhasf \n alsjflas 
    """
    render_multiline_text(screen, info_text, (10, 10), pygame.font.Font("fonts/Roboto-Regular.ttf", 22))

    # Update the display
    pygame.display.flip()