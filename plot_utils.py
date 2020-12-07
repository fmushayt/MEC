import numpy as np
import seaborn as sns
sns.set()
import matplotlib.pyplot as plt
import os
import uuid
import glob
import imageio
import shutil

class Plotter:  # Helper class for plotting
    def __init__(self, run_id=None):
        """
        Example 1:
            plotter = Plotter("MyWelzlAnimation")
            plotter.set_P(P).plot_P()
            plotter.plot_circle(circle)
            plotter.show()

        Example 2:
            plotter = Plotter("MyBruteForceExperiment")
            plotter.set_P(P).plot_P()
            plotter.plot_circle(circle, color='red').save("myplot.png")

        :param run_id: string: name for experiment
        """
        if run_id is None: run_id = str(uuid.uuid4())
        self.run_id = run_id
        self.ax = None
        self.fig = None
        self.all_points = None
        self.is_P_plotted = False

    def set_P(self, points):
        self.all_points = np.asarray(points)
        return self

    def plot_P(self, **kwargs):
        if self.is_P_plotted:
            return self

        self.get_axes().scatter(self.all_points[:, 0], self.all_points[:, 1], **kwargs)
        self.is_P_plotted = True
        xmin, ymin = self.all_points.min(axis=0)
        xmax, ymax = self.all_points.max(axis=0)
        xbuf = np.abs(0.5 * (xmax - xmin) / 2)  # just some extra space
        ybuf = np.abs(0.5 * (ymax - ymin) / 2)
        extent = [xmin - xbuf, xmax + xbuf] if xbuf > ybuf else [ymin - ybuf, ymax + ybuf]

        self.get_axes().set_xlim(extent)
        self.get_axes().set_ylim(extent)
        self.get_axes().set_title(self.run_id)
        return self

    def get_axes(self):
        if self.ax is None:
            fig, ax = plt.subplots(figsize=(5, 5))
            self.ax = ax
            self.fig = fig
        return self.ax

    def set_axes(self, fig, ax):
        self.ax = ax
        self.fig = fig
        return self

    def plot_circle(self, circle, **kwargs):
        self.plot_P()
        circle_artist = plt.Circle(circle[0], circle[1], fill=False, **kwargs)
        self.get_axes().add_artist(circle_artist)

        return self

    def plot_points(self, points, **kwargs):
        points = np.asarray(points)
        self.plot_P()
        self.get_axes().scatter(points[:, 0], points[:, 1], **kwargs)
        return self

    def plot_point(self, point, **kwargs):
        self.plot_P()
        self.get_axes().scatter([point[0]], [point[1]], **kwargs)
        return self

    def show(self):
        plt.show()
        self.clear()
        return self

    def save(self, fname):
        plt.savefig(fname)
        self.clear()
        return self

    def clear(self):
        self.ax = None
        self.fig = None
        self.is_P_plotted = False
        return self

    def close(self):
        plt.close()
        self.clear()
        return self




class AnimatedPlotter(Plotter):  # Helper class to create gifs of progress of algorithms
    def __init__(self,run_id=None, save_dir="./saved"):
        super().__init__(run_id=run_id)

        self.save_animation_dir = os.path.join(save_dir, "animations")
        self.frame_dir = os.path.join(self.save_animation_dir, run_id, "frames")
        if os.path.exists(self.frame_dir):
            shutil.rmtree(self.frame_dir)
        os.makedirs(self.frame_dir)
        self._frame = 0

    def dump(self):
        plt.savefig(os.path.join(self.frame_dir, "{}.png".format(str(self._frame).zfill(4))))
        self._frame += 1
        return self

    def save_animation(self, fps=10):
        images = []
        fnames = glob.glob(os.path.join(self.frame_dir, "*"))
        for fname in fnames:
            images.append(imageio.imread(fname))

        for i in range(5):  # repeat last frame 3 times (result)
            images.append(images[-1])
        anim_path = os.path.join(self.save_animation_dir, "{}.gif".format(self.run_id))
        imageio.mimsave(anim_path, images, fps=fps)
        print("Animation saved to {}".format(anim_path))

    def dsc(self):  # shortcut for dump show clear
        return self.dump().show()

    def dcc(self):  # shortcut for dump close clear
        return self.dump().close()
