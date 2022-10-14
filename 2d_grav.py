import numpy as np
import tsp_brute_force
# import matplotlib.pyplot as plt

class Grav:
    def __init__(self, nbodies, fieldstrength, time_steps, initial_loc = None):
        # number of bodies
        self.nbodies = nbodies

        # initial coords of bodies in space
        if initial_loc == None:
            x_values = np.random.uniform(low = 0.0, high = 10.0, size = nbodies)
            y_values = np.random.uniform(low = 0.0, high = 10.0, size = nbodies)
        else:
            x_values = [initial_loc[i][0] for i in range(self.nbodies)]
            y_values = [initial_loc[i][1] for i in range(self.nbodies)]

        self.initial_coords = [[x, y] for x, y in zip(x_values, y_values)]
        
        # strength of the gravitational force
        self.fstrength = fieldstrength

        # number of simulation steps
        self.steps = time_steps

        # collisions
        self.collisions = {f'body{i}_body{j}' : 0 for i in range(self.nbodies) for j in range(i + 1, self.nbodies)}

        # body history
        self.history = {f'body{i}' : [[self.initial_coords[i][0]], [self.initial_coords[i][1]]] for i in range(self.nbodies)}

    # calculates the unit vector of one body in the direction of another
    def unit_vector(self, i, j):
        x1, y1 = i
        x2, y2 = j
        abs_distance = np.sqrt((y2 - y1)**2 + (x2 - x1)**2)

        return [(x2 - x1)/abs_distance, (y2 - y1)/abs_distance]

    # calculate the gravitational force of one body in the direction of another
    def force(self, i, j, idx):
        x1, y1 = i
        x2, y2 = j
        dist_sq = (y2 - y1)**2 + (x2 - x1)**2

        # correction for close bodies, since force approaches infinity
        if dist_sq < 0.1:
            if idx[0] > idx[1]: idx[0], idx[1] = idx[1], idx[0]
            self.collisions[f'body{idx[0]}_body{idx[1]}'] += 1
            return 0

        return (self.fstrength / dist_sq)

    # simulates the gravitational system of bodies and extracts the relevent data
    def simulate(self):

        # copy of initial co-ords to be updated
        co_ords = {f'body{i}' : self.initial_coords[i] for i in range(self.nbodies)}
        initial_co_ords = co_ords.copy()

        step = 0
        while step < self.steps:


            # hash map containing hash maps, that contain the direction vectors from body (i + 1) to body (j + 1)
            direction_vectors = {f'body{i}' : {f'body{j}' : self.unit_vector(co_ords[f'body{i}'], co_ords[f'body{j}']) for j in range(self.nbodies) if i != j} for i in range(self.nbodies)}
            # hash map containing hash maps, that contain the forces from body (i + 1) to body (j + 1)
            forces = {f'body{i}' : {f'body{j}' : self.force(co_ords[f'body{i}'], co_ords[f'body{j}'], [i, j]) for j in range(self.nbodies) if i != j} for i in range(self.nbodies)}

            # each body must be nudged by the resultant force from each other body
            for bodyi in range(self.nbodies):
                for bodyj in range(self.nbodies):
                    if bodyi == bodyj: continue
                    for ord in range(2):
                        co_ords[f'body{bodyi}'][ord] += forces[f'body{bodyi}'][f'body{bodyj}'] * direction_vectors[f'body{bodyi}'][f'body{bodyj}'][ord]

            # update the history data for each time step
            for i in range(self.nbodies):
                for ord in range(2):
                    self.history[f'body{i}'][ord].append(co_ords[f'body{i}'][ord])

            step += 1

        return initial_co_ords, self.collisions, self.history

initial_loc = [[1.0, 1.0], [7.0, 5.0], [4.9, 2.3], [8.0, 3.0], [9.0, 9.0]]      
test = Grav(nbodies = 5, fieldstrength = 1, time_steps = 100, initial_loc = None)
initial_coords, collision_freq, history = test.simulate()

#plt.hist(collision_freq)
#plt.show()
tsp_result, bodies_result = tsp_brute_force.travelling_salesman(initial_coords)
print(bodies_result)
print(collision_freq)
# body0, body2, body3, body1, body4

