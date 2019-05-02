from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt


class VisMatplotlib:
    def __init__(self):
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot(111, projection='3d')
        self.ax.set_xlim([-5,5])
        self.ax.set_ylim([-5,5])
        self.ax.set_zlim([0,3])
        self.ax.set_xlabel("X")
        self.ax.set_ylabel("Y")
        self.ax.set_zlabel("Z")
        self.plot = None
        self.timeAnnotation = self.ax.annotate("Time", xy=(0, 0), xycoords='axes fraction', fontsize=12, ha='right', va='bottom')

    def update(self, t, crazyflies, color):
        xs = []
        ys = []
        zs = []
        R = color[0]/255
        G = color[1]/255
        B = color[2]/255
        for cf in crazyflies:
            x, y, z = cf.position()
            xs.append(x)
            ys.append(y)
            zs.append(z)

        if self.plot is None:
            self.plot = self.ax.scatter(xs, ys, zs, s=30, c=[R,G,B], linewidths=0)
        else:
            self.plot._offsets3d = (xs, ys, zs)

        self.timeAnnotation.set_text("{} s".format(t))
        plt.pause(0.0001)
