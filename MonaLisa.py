import random
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from problem import Problem
import cv2

class MonaLisa(Problem):

    def calculate_fitness(self, chromosome):
        # Calculate the fitness of a chromosome
        # Load the original Mona Lisa image
        original_image = Image.open('mona_lisa.jpg')
        original_pixels = np.array(original_image)

        test_image = Image.open('mona_lisa_test.jpg')
        test_image = test_image.resize(original_image.size)  # Resize test_image to match original_image dimensions
        test_pixels = np.array(test_image)

        # Create a blank canvas to draw the polygons on
        canvas_size = (original_image.width, original_image.height)
        canvas = Image.new('RGB', canvas_size)
        canvas_pixels = np.array(canvas)

        # Draw the polygons on the canvas
        print(chromosome)
        for polygon in chromosome:
            x = polygon['x']
            y = polygon['y']
            color = polygon['color']

            poly = np.column_stack([x, y])
            canvas_pixels = cv2.fillPoly(canvas_pixels, [poly], (0,0,255))

        # Calculate the fitness as the mean squared error between the original and generated image
        fitness = np.mean((original_pixels - test_pixels) ** 2)

        return fitness
    
    def crossover(self, parent1, parent2):
        # Perform crossover to create a new chromosome from two parents
        crossover_point = random.randint(1, len(parent1))

        # Create a new chromosome by combining parts of both parents
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]

        fitness1 = self.calculate_fitness(child1)
        fitness2 = self.calculate_fitness(child2)

        offsprings = [(child1, fitness1), (child2, fitness2)]
        return offsprings

    def random_chromosome(self):
        # Generate a random chromosome for the Mona Lisa problem
        num_polygons = 5
        canvas_size = (100, 100)
        polygons = []
        for i in range(num_polygons):
            x = [random.randint(0, canvas_size[0]) for j in range(3)]
            y = [random.randint(0, canvas_size[1]) for j in range(3)]
            color = (random.random(), random.random(), random.random(), random.random())
            # color = 'blue'
            polygons.append({'x': x, 'y': y, 'color': color})
        self.plot_polygons(polygons)
        fitness = self.calculate_fitness(polygons)
        print("printing random chromosome",fitness)
        return (polygons, fitness)
    
    def draw_polygons(self, polygons, canvas_size=(100, 100)):
        canvas = Image.new('RGB', canvas_size)
        canvas_pixels = np.array(canvas)
        # Draw the polygons on a canvas and display the image
        for polygon in polygons:
            x = polygon['x']
            y = polygon['y']
            color = polygon['color']

            poly = np.column_stack([x, y])
            canvas_pixels = cv2.fillPoly(canvas_pixels, [poly], color)

        # Display the image
        plt.imshow(canvas_pixels)
        plt.axis('off')
        plt.show()


    def plot_polygons(self, polygons, canvas_size=(100, 100)):
        print(polygons)
        fig, ax = plt.subplots(facecolor='black')  # Set the facecolor of the figure to black
        ax.set_xlim(0, canvas_size[0])
        ax.set_ylim(0, canvas_size[1])
        ax.set_aspect('equal', 'box')

        for polygon in polygons:
            x = polygon['x']
            y = polygon['y']
            color = polygon['color']

            poly = Polygon(np.column_stack([x, y]), closed=True, facecolor=color, edgecolor='none')
            ax.add_patch(poly)

        ax.axis('off')  # Turn off the axis
        ax.grid(False)  # Turn off the grid lines

        plt.show()

def plot_polygons(polygons, canvas_size=(100, 100)):
    print(polygons)
    fig, ax = plt.subplots()
    ax.set_xlim(0, canvas_size[0])
    ax.set_ylim(0, canvas_size[1])
    ax.set_aspect('equal', 'box')

    for polygon in polygons:
        x = polygon['x']
        y = polygon['y']
        color = polygon['color']

        poly = Polygon(np.column_stack([x, y]), closed=True, facecolor=color, edgecolor='none')
        ax.add_patch(poly)

    ax.axis('off')  # Turn off the axis
    ax.grid(False)  # Turn off the grid lines

    plt.show()
# Example usage
polygon = [{'x': [1, 26, 4], 'y': [24, 53, 87], 'color': 'blue'}, {'x': [38, 28, 11], 'y': [16, 37, 63], 'color': 'blue'}, {'x': [70, 21, 29], 'y': [37, 28, 77], 'color': 'blue'}, {'x': [78, 83, 53], 'y': [77, 13, 10], 'color': 'blue'}, {'x': [41, 90, 4], 'y': [99, 15, 98], 'color': 'blue'}]
# plot_polygons(polygon)

