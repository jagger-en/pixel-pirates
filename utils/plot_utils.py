#!/usr/bin/env python3
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from matplotlib.animation import PillowWriter


def create_animation_gif(file_path,
                        normalized_points,
                        title,
                        y_label_name,
                        x_label_name,
                        x_lim,
                        y_lim):
    '''
    normalized_points: (x, y)
    '''
    frames = len(normalized_points)

    fig, ax = plt.subplots(1, 1)
    fig.set_size_inches(5,5)

    def animate(idx):
        ax.clear()
        point = normalized_points[idx]
        x_point = point[0]
        y_point = point[1]
        ax.plot(x_point,
                y_point,
                color='green',
                label='original',
                marker='o')
        ax.set_xlim(x_lim)
        ax.set_ylim(y_lim)
        ax.set_ylabel(y_label_name)
        ax.set_xlabel(x_label_name)
        ax.set_title(title)

    ani = FuncAnimation(fig,
                        animate,
                        frames=frames,
                        interval=1,
                        repeat=False)
    plt.close()

    ani.save(file_path, dpi=300,
            writer=PillowWriter(fps=1))


# import matplotlib.pyplot as plt
# def plot_x_y_t(plt_data):
#     '''
#     plt_data: [(x,y,t)...]
#     '''
#     ax = plt.axes(projection='3d')

#     plt_data_x = [p[0] for p in plt_data]
#     plt_data_y = [p[1] for p in plt_data]
#     plt_data_t = [p[2] for p in plt_data]

#     ax.plot3D(plt_data_t, plt_data_x, plt_data_y, 'gray')
#     ax.set_xlabel('time')
#     ax.set_ylabel('x')
#     ax.set_zlabel('y')
#     plt.show()
