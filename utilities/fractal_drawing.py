from numba import jit, prange
import numpy as np
import plotly.graph_objs as go
from config import MAX_ITER
HEATMAP_COLORSCALE = [[0, 'rgb(0,0,0)'],[0.2, 'rgb(255,0,0)'],[0.45, 'rgb(255,0,255)'],
                      [0.60, 'rgb(100,0,255)'], [0.75, 'rgb(0,215,0)'], [0.9, 'rgb(255,127,80)'], [1, 'rgb(255,255,255)']]

class ChartSizeParameters(dict):

    def __init__(self, xmin, xmax, ymin, ymax, width=1500, height=1500):
        content = {
            'xmin': xmin,
            'xmax': xmax,
            'ymin': ymin,
            'ymax': ymax,
            'width': width,
            'height': height,

        }
        super(ChartSizeParameters, self).__init__(content)

    def get_x_related_params(self):
        return self["xmin"], self["xmax"], self["width"]

    def get_y_related_params(self):
        return self["ymin"], self["ymax"], self["height"]

    def get_size(self):
        return self["width"], self["height"]


@jit(nopython=True, cache=True, fastmath=True)
def mandelbrot(c, maxiter):
    """
    Given the real and imaginary parts of a complex number,
    determine if it is a candidate for membership in the Mandelbrot
    set given a fixed number of iterations.
    """
    z = c
    for i in prange(maxiter):
        z = z * z + c
        z_abs = z.real * z.real + z.imag * z.imag
        if z_abs >= 4:
            return i+1 - np.log(np.log2(z_abs))

    return 0


@jit(nopython=True, cache=True, fastmath=True)
def julia(z, c, maxiter):
    # the julia set is a picture in dynamical plane, that records ALL orbits for fixed C
    # this function calculates it for a given c-z pair
    for i in prange(maxiter):
        z_abs = z.real * z.real + z.imag * z.imag
        if z_abs >= 4:
            return i+1 - np.log(np.log2(z_abs))
        z = z * z + c
    return 0


@jit(nopython=True)
def initialize_picture_parameters(xmin, xmax, ymin, ymax, width, height):
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    n3 = np.empty(height, width)
    return r1, r2, n3


@jit(nopython=True, parallel=True, cache=True, fastmath=True)
def mandelbrot_set(xmin, xmax, ymin, ymax, maxiter=250, width=1500, height=1500):
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    n3 = np.empty((width, height))

    for i in prange(width):
        for j in prange(height):
            n3[i, j] = mandelbrot(r1[i] + 1j * r2[j], maxiter)

    return r1, r2, np.log(n3+1)


@jit(nopython=True, cache=True, fastmath=True)
def convert_iteration_number_to_color_value(iterations, z):
    return iterations + 1 - np.log(np.log2(z.real*z.real + z.imag*z.imag))

@jit(nopython=True, parallel=True, cache=True, fastmath=True)
def julia_set(c, xmin, xmax, ymin, ymax, maxiter=250, width=1500, height=1500):
    # notice that C is an input in this function
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    n3 = np.empty((width, height))
    for i in prange(width):
        for j in prange(height):
            n3[i, j] = julia(r1[i] + 1j * r2[j], c, maxiter)
    return r1, r2, np.log(n3+1)


def create_chart_from_matrix(r1, r2, n3):
    trace = go.Heatmap(x=r1,
                       y=r2,
                       z=n3.T,
                       showscale=False,
                       colorscale=HEATMAP_COLORSCALE,
                       zmin=0,
                       zmax=np.log(MAX_ITER),
                       zmid=np.log(MAX_ITER)/2
                       )

    data = [trace]

    layout = go.Layout(
        title='Fractal Plot',
        autosize=True,
        xaxis=dict(),
        yaxis=dict(
            showgrid=False,
            scaleanchor="x",
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        margin=dict(l=5, r=5, t=5, b=5),

    )

    fig = go.Figure(data=data, layout=layout)
    return fig
