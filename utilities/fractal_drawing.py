from numba import jit, njit, prange
import numpy as np
import plotly.graph_objs as go


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
def mandelbrot(c, max_iters):
    """
    Given the real and imaginary parts of a complex number,
    determine if it is a candidate for membership in the Mandelbrot
    set given a fixed number of iterations.
    """
    z = c
    for i in prange(max_iters):
        z = z * z + c
        if (z.real * z.real + z.imag * z.imag) >= 4:
            return i

    return 0


@jit(nopython=True, cache=True, fastmath=True)
def julia(z, c, maxiter):
    # the julia set is a picture in dynamical plane, that records ALL orbits for fixed C
    # this function calculates it for a given c-z pair
    for n in prange(maxiter):
        if (z.real * z.real + z.imag * z.imag) >= 4:
            return n
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

    return r1, r2, n3


@jit(nopython=True, parallel=True, cache=True, fastmath=True)
def julia_set(c, xmin, xmax, ymin, ymax, maxiter=250, width=1500, height=1500):
    # notice that C is an input in this function
    r1 = np.linspace(xmin, xmax, width)
    r2 = np.linspace(ymin, ymax, height)
    n3 = np.empty((width, height))
    for i in prange(width):
        for j in prange(height):
            n3[i, j] = julia(r1[i] + 1j * r2[j], c, maxiter)
    return r1, r2, n3


def create_chart_from_matrix(r1, r2, n3):
    trace = go.Heatmap(x=r1,
                       y=r2,
                       z=n3.T)

    data = [trace]

    layout = go.Layout(
        title='Mandelbrot Plot',
        width=1250,
        height=1250,
        xaxis=dict(
        ),
        yaxis=dict(
            scaleanchor="x",
        ),
    )

    fig = go.Figure(data=data, layout=layout)
    return fig
