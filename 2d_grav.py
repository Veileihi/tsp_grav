from cmath import sqrt
import numpy as np

class Grav:
    def __init__(self, nbodies, fieldstrength, time_steps):
        # number of bodies
        self.nbodies = nbodies

        # initial coords of bodies in space
        x_values = np.random.uniform(low = 0.0, high = 100.0, size = nbodies)
        y_values = np.random.uniform(low = 0.0, high = 100.0, size = nbodies)
        self.initial_coords = [[x, y] for x, y in zip(x_values, y_values)]
        
        # strength of the gravitational force
        self.fstrength = fieldstrength

        # number of simulation steps
        self.steps = time_steps

        # collisions
        self.collisions = {f'body{i + 1}_body{j + 1}' : 0 for i in range(self.nbodies) for j in range(self.nbodies - i)}

        # body history
        self.history = {f'body{i + 1}' : [self.initial_coords[i][0], self.initial_coords[i][1]] for i in range(self.nbodies)}

    # calculates the unit vector of one body in the direction of another
    def unit_vector(self, i, j):
        x1, y1 = self.initial_coords[i]
        x2, y2 = self.initial_coords[j]
        abs_distance = np.sqrt((y2 - y1)**2 + (x2 - x1)**2)

        return [(x2 - x1)/abs_distance, (y2 - y1)/abs_distance]

    # calculate the gravitational force of one body in the direction of another
    def force(self, i, j):
        x1, y1 = self.initial_coords[i]
        x2, y2 = self.initial_coords[j]
        dist_sq = (y2 - y1)**2 + (x2 - x1)**2

        # correction for close bodies, since force approaches infinity
        if dist_sq < 0.1:
            self.collisions[f'body{i + 1}_body{j + 1}'] += 1
            return np.log(self.fstrength / dist_sq)

        return (self.fstrength / dist_sq)

    # simulates the gravitational system of bodies and extracts the relevent data
    def simulate(self):

        # copy of initial co-ords to be updated
        co_ords = {f'body{i + 1}' : self.initial_coords[i] for i in range(self.nbodies)}
        initial_co_ords = co_ords.copy()

        step = 0
        while step < self.time_steps:
            # hash map containing hash maps, that contain the direction vectors from body (i + 1) to body (j + 1)
            direction_vectors = {f'body{i + 1}' : {f'body{j + 1}' : self.unit_vector(co_ords[i], co_ords[j]) for j in range(self.nbodies) if i != j} \
                                for i in range(self.nbodies)}

            # hash map containing hash maps, that contain the forces from body (i + 1) to body (j + 1)
            forces = {f'body{i + 1}' : {f'body{j + 1}' : self.force(co_ords[i], co_ords[j]) for j in range(self.nbodies) if i != j} \
                    for i in range(self.nbodies)}

            # each body must be nudged by the resultant force from each other body
            for bodyi in range(self.nbodies):
                for bodyj in range(self.nbodies):
                    for ord in range(2):
                        co_ords[f'body{bodyi}'][ord] += forces[f'body{bodyi}'][f'body{bodyj}'] * direction_vectors[f'body{bodyi}'][f'body{bodyj}'][ord]

            for i in range(self.nbodies):
                for ord in range(2):
                    self.history[f'body{i + 1}'][ord].append(co_ords[f'body{i + 1}'][ord])

            step += 1

        return initial_co_ords, co_ords, self.collisions, self.history

        