import dash_html_components as html
import dash_core_components as dcc
from utilities import fractal_drawing as fd
import numpy as np
import dash_bootstrap_components as dbc
import config as c

def generate_title():
    # Title
    return html.H1('Mandelbrot and Julia sets',
                   style={
                       'position': 'relative',
                       'top': '0px',
                       'left': '10px',
                       'display': 'inline',
                       'color': 'White'
                   })


def create_mandelbrot_chart(xmin, xmax, ymin, ymax):
    return dcc.Graph(id='mandelbrot_set', figure=fd.create_chart_from_matrix(
        *fd.mandelbrot_set(xmin, xmax, ymin, ymax))
                     )


def create_julia_chart(c, xmin, xmax, ymin, ymax):
    return dcc.Graph(id='julia_set', figure=fd.create_chart_from_matrix(
        *fd.julia_set(c, xmin, xmax, ymin, ymax))
                     )

def charts_in_2_columns(axes_limits):

    return html.Div([
        dbc.Row([
            dbc.Col(
                html.Div([
                    html.H3('Mandelbrot Set'),
                    create_mandelbrot_chart(**axes_limits['mandelbrot']),
                    dcc.Slider(
                        id='iterations_mandelbrot',
                        min=0,
                        max=c.MAX_ITER,
                        marks={int(val): {'label': str(int(val))} for val in np.linspace(0, c.MAX_ITER, 11)},
                        value=c.DEFAULT_ITER,
                    ),

                ], className='container'), width=6),
            dbc.Col(
                html.Div([
                    html.H3('Julia Set'),
                    create_julia_chart(0, **axes_limits['julia']),
                    dcc.Slider(
                        id='iterations_julia',
                        min=0,
                        max=c.MAX_ITER,
                        marks={int(val): {'label': str(int(val)), 'style':{'color':'white'}} for val in np.linspace(0, c.MAX_ITER, 11)},
                        value=c.DEFAULT_ITER,
                    ),

                ], className='container'), width=6)
        ],
        )
    ], className='container'
    )
