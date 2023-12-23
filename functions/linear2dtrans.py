from manim import *

class LinearTransformationExample(Scene):
    def construct(self):
        plane = NumberPlane(x_range=[-10,10,1], y_range=[-10,10,1], x_length=9, y_length=9)
        
        # Create a copy of the original plane with 60% opacity
        original_plane = plane.copy().set_opacity(0.6)
        original_plane.color = WHITE

        matrix = [[5, 6], [6, 5]]  # The transformation matrix

        # Create the basis vectors
        i_hat = Arrow(plane.c2p(0, 0), plane.c2p(1, 0), color=RED)
        j_hat = Arrow(plane.c2p(0, 0), plane.c2p(0, 1), color=GREEN)

        # Add the basis vectors to the scene
        self.add(i_hat, j_hat)

        # Create the transformations
        transform_plane = ApplyMatrix(matrix, plane)
        transform_i_hat = ApplyMatrix(matrix, i_hat)
        transform_j_hat = ApplyMatrix(matrix, j_hat)

        # Play the transformations over 10 seconds
        self.play(transform_plane, transform_i_hat, transform_j_hat, run_time=7)

        # Add the original plane to the scene after the animations
        self.add(original_plane)

        self.wait(3)