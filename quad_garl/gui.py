import sys

import matplotlib.pyplot as plt
import mpl_toolkits.mplot3d.axes3d as Axes3D
import numpy as np

from quad_garl.quad_utils import rotation_matrix


class GUI():
    # 'quad_list' is a dictionary of format: quad_list = {'quad_1_name':{'position':quad_1_position,'orientation':quad_1_orientation,'arm_span':quad_1_arm_span}, ...}
    def __init__(self, quads):
        self.quads = quads
        self.fig = plt.figure()
        self.ax = Axes3D.Axes3D(self.fig)
        self.ax.set_xlim3d([-2.0, 2.0])
        self.ax.set_xlabel('X')
        self.ax.set_ylim3d([-2.0, 2.0])
        self.ax.set_ylabel('Y')
        self.ax.set_zlim3d([0, 5.0])
        self.ax.set_zlabel('Z')
        self.ax.set_title('Quadcopter Simulation')
        self.init_plot()
        self.fig.canvas.mpl_connect('key_press_event', self.keypress_routine)

    def init_plot(self):
        for key in self.quads:
            self.quads[key]['l1'], = self.ax.plot([], [], [], color='blue', linewidth=3, antialiased=False)
            self.quads[key]['l2'], = self.ax.plot([], [], [], color='red', linewidth=3, antialiased=False)
            self.quads[key]['hub'], = self.ax.plot([], [], [], marker='o', color='green', markersize=6,
                                                   antialiased=False)

    def update(self):
        print("GUI UPDATE")
        for key in self.quads:
            R = rotation_matrix(self.quads[key]['orientation'])
            L = self.quads[key]['L']
            points = np.array([[-L, 0, 0], [L, 0, 0], [0, -L, 0], [0, L, 0], [0, 0, 0], [0, 0, 0]]).T
            points = np.dot(R, points)
            points[0, :] += self.quads[key]['position'][0]
            points[1, :] += self.quads[key]['position'][1]
            points[2, :] += self.quads[key]['position'][2]
            self.quads[key]['l1'].set_data(points[0, 0:2], points[1, 0:2])
            self.quads[key]['l1'].set_3d_properties(points[2, 0:2])
            self.quads[key]['l2'].set_data(points[0, 2:4], points[1, 2:4])
            self.quads[key]['l2'].set_3d_properties(points[2, 2:4])
            self.quads[key]['hub'].set_data(points[0, 5], points[1, 5])
            self.quads[key]['hub'].set_3d_properties(points[2, 5])
        plt.pause(0.000000000000001)

    def keypress_routine(self, event):
        sys.stdout.flush()
        if event.key == 'x':
            y = list(self.ax.get_ylim3d())
            y[0] += 0.2
            y[1] += 0.2
            self.ax.set_ylim3d(y)
        elif event.key == 'w':
            y = list(self.ax.get_ylim3d())
            y[0] -= 0.2
            y[1] -= 0.2
            self.ax.set_ylim3d(y)
        elif event.key == 'd':
            x = list(self.ax.get_xlim3d())
            x[0] += 0.2
            x[1] += 0.2
            self.ax.set_xlim3d(x)
        elif event.key == 'a':
            x = list(self.ax.get_xlim3d())
            x[0] -= 0.2
            x[1] -= 0.2
            self.ax.set_xlim3d(x)
