import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, State, Input
from app_elements import app_elements as ae
import dash_bootstrap_components as dbc
import numpy as np
from utilities import fractal_drawing as fd
import time
import json

DEFAULT_AXES = {
    'mandelbrot': {
        'xmin': -2,
        'xmax': 0.5,
        'ymin': -1,
        'ymax': 1,
    },
    'julia': {
        'xmin': -2,
        'xmax': 2,
        'ymin': -2,
        'ymax': 2,
    }

}

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css", dbc.themes.SUPERHERO]
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div([
    ################################################################################
    # Title
    ae.generate_title(),
    ################################################################################
    html.Br(),
    # charts in 2 columns
    ae.charts_in_2_columns(DEFAULT_AXES),
])


@app.callback(
    Output('mandelbrot_set', 'figure'),
    [Input('iterations_mandelbrot', 'value'),
     Input('mandelbrot_set', 'relayoutData')])
def display_selected_data_mandelbrot(iterations, relayoutData):
    start = time.time()

    if relayoutData:
        xmin = relayoutData.get('xaxis.range[0]', DEFAULT_AXES['mandelbrot']['xmin'])
        xmax = relayoutData.get('xaxis.range[1]', DEFAULT_AXES['mandelbrot']['xmax'])
        ymin = relayoutData.get('yaxis.range[0]', DEFAULT_AXES['mandelbrot']['ymin'])
        ymax = relayoutData.get('yaxis.range[1]', DEFAULT_AXES['mandelbrot']['ymax'])
    else:
        xmin = DEFAULT_AXES['mandelbrot']['xmin']
        xmax = DEFAULT_AXES['mandelbrot']['xmax']
        ymin = DEFAULT_AXES['mandelbrot']['ymin']
        ymax = DEFAULT_AXES['mandelbrot']['xmax']

    fig = fd.create_chart_from_matrix(*fd.mandelbrot_set(xmin, xmax, ymin, ymax, maxiter=iterations))
    end = time.time()
    print(end - start)
    return fig


@app.callback(
    Output('julia_set', 'figure'),
    [Input('mandelbrot_set', 'clickData'),
    Input('iterations_julia', 'value'),
     Input('julia_set', 'relayoutData')])
def display_click_data(clickData, iterations, relayoutData):
    if clickData:
        coords = clickData['points'][0]
    else:
        coords = {
            'x': 0,
            'y': 0,
        }
    if relayoutData:
        xmin = relayoutData.get('xaxis.range[0]', DEFAULT_AXES['julia']['xmin'])
        xmax = relayoutData.get('xaxis.range[1]', DEFAULT_AXES['julia']['xmax'])
        ymin = relayoutData.get('yaxis.range[0]', DEFAULT_AXES['julia']['ymin'])
        ymax = relayoutData.get('yaxis.range[1]', DEFAULT_AXES['julia']['ymax'])
    else:
        xmin = DEFAULT_AXES['julia']['xmin']
        xmax = DEFAULT_AXES['julia']['xmax']
        ymin = DEFAULT_AXES['julia']['ymin']
        ymax = DEFAULT_AXES['julia']['ymax']

    fig = fd.create_chart_from_matrix(*fd.julia_set(coords['x'] + 1j * coords['y'], xmin, xmax, ymin, ymax, iterations))
    return fig


################################################################################


if __name__ == '__main__':
    app.run_server(debug=True)
