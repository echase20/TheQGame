#!/usr/bin/env python3
from PIL import Image, ImageDraw
import math


# Class for rendering and saving shapes and images
class ShapeRenderer:
    # Length of the sides of the canvas
    length = 50
    # Midpoint of the canvas
    mid_point = length / 2
    # The space between the edges of the shape and the canvas
    padding = 0  # Set padding to 0 to touch the canvas edges
    # Rightmost point of the triangle's coordinate
    corner = length - (mid_point * 2 - mid_point / 2)
    # The space between the edges specifically for the star and 8star
    s_padding = 2 * length / 10

    def __init__(self, max_col):
        self.curr_shapes = 0  # # of current shapes
        self.images = []
        self.row = 0  # Track the current row
        self.col = 0  # Track the current column
        self.max_col = max_col

    # Rotate the given set of coordinates
    def rotate(self, points, angle, center):
        angle = math.radians(angle)
        cos_val = math.cos(angle)
        sin_val = math.sin(angle)
        cx, cy = center
        new_points = []
        for x_old, y_old in points:
            x_old -= cx
            y_old -= cy
            x_new = x_old * cos_val - y_old * sin_val
            y_new = x_old * sin_val + y_old * cos_val
            new_points.append([x_new + cx, y_new + cy])
        return new_points

    # Render the given shape specifications onto the canvas
    def make_shape(self, shape, color):
        img = Image.new("RGB", (self.length, self.length), "white")
        draw = ImageDraw.Draw(img)

        if shape == "":
            pass
        elif shape == "square":
            square_size = self.length
            draw.rectangle([(self.padding, self.padding), (square_size, square_size)], fill=color, outline=None)
        elif shape == "circle":
            circle_diameter = self.length
            draw.ellipse([(self.padding, self.padding), (circle_diameter, circle_diameter)], fill=color, outline=None)
        elif shape == "star":
            # Coordinates of one triangle in the star shape
            tri = [
                (0, 0),
                (self.corner + self.s_padding / 2, self.mid_point + self.s_padding),
                (self.mid_point + self.s_padding, self.corner + self.s_padding / 2)
            ]
            # Print all four angles
            for a in range(0, 360, 90):
                tri_rotated = self.rotate(tri, a, (self.mid_point, self.mid_point))
                flattened_tri = [coord for point in tri_rotated for coord in point]
                draw.polygon(flattened_tri, fill=color, outline=None)
        elif shape == "8star":
            # Coordinates of one triangle in the star shape
            tri = [
                (self.s_padding, self.s_padding),
                (self.corner + self.s_padding, self.mid_point + self.s_padding / 2),
                (self.mid_point + self.s_padding / 2, self.corner + self.s_padding)
            ]
            # Print all eight angles
            for a in range(0, 360, 45):
                tri_rotated = self.rotate(tri, a, (self.mid_point, self.mid_point))
                flattened_tri = [coord for point in tri_rotated for coord in point]
                draw.polygon(flattened_tri, fill=color, outline=None)
        elif shape == "diamond":
            diamond_size = self.length
            diamond_points = [
                (self.mid_point, self.padding),
                (self.padding, self.mid_point),
                (self.mid_point, diamond_size - self.padding),
                (diamond_size - self.padding, self.mid_point)
            ]
            draw.polygon(diamond_points, fill=color, outline=None)
        elif shape == "clover":


            draw.ellipse([(1/4 * self.length, 0), (self.length - 1/4 * self.length, self.length - 1)], fill=color, outline=None)
            draw.ellipse([(0, 1/4 * self.length), (self.length - self.padding - 1, self.length - 1/4 * self.length)], fill=color, outline=None)
        
            #draw.ellipse([(1/4 * self.length + 1, 1), (self.length - 1/4 * self.length - 1, self.length - 2)], fill=color, outline=None)
            #draw.ellipse([(1, 1/4 * self.length + 1), (self.length - self.padding - 2, self.length - 1/4 * self.length - 1)], fill=color, outline=None)
        
        # Putting all of the shapes next to the shape before it
        x_position = self.col * self.length
        y_position = self.row * self.length
        img_width, _ = img.size
        self.images.append((img, (x_position, y_position, x_position + img_width, y_position + self.length)))

        self.col += 1
        if self.col > self.max_col:
            self.col = 1
            self.row += 1

    # Save the rendered images as a single sequence
    def save_images(self, filename):
        if self.images:
            total_width = self.col * self.length
            total_height = (self.row + 1) * self.length
            result_image = Image.new("RGB", (total_width, total_height), "white")

            for img, img_position in self.images:
                result_image.paste(img, img_position)

            result_image.save(filename, 'PNG')
            #result_image.show()
    def return_file(shape,color):
            s = ShapeRenderer(3)
            s.make_shape(shape,color)
            s.save_images("file.png")
"""
def main():
    ShapeRenderer.return_file("square","green")

if __name__ == "__main__":
    main()"""
        #test