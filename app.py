import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Output, State, Input
import plotly.graph_objs as go
import numpy as np
from utilities import fractal_drawing as fd
import time

XMIN_DEFAULT = -2
XMAX_DEFAULT = 0.5
YMIN_DEFAULT = -1
YMAX_DEFAULT = 1

styles = {
    'pre': {
        'border': 'thin lightgrey solid',
        'overflowX': 'scroll'
    }
}

app = dash.Dash()

app.layout = html.Div([
    ################################################################################
    # Title
    html.H2('Zoom Application',
            style={
                'position': 'relative',
                'top': '0px',
                'left': '10px',
                'font-family': 'Dosis',
                'display': 'inline',
                'font-size': '4.0rem',
                'color': '#4D637F'
            }),
    html.H2('for',
            style={
                'position': 'relative',
                'top': '0px',
                'left': '20px',
                'font-family': 'Dosis',
                'display': 'inline',
                'font-size': '2.0rem',
                'color': '#4D637F'
            }),
    html.H2('MandelBrot',
            style={
                'position': 'relative',
                'top': '0px',
                'left': '27px',
                'font-family': 'Dosis',
                'display': 'inline',
                'font-size': '4.0rem',
                'color': '#4D637F'
            }),

    ################################################################################
    html.Br(),

    html.Div([

        dcc.Graph(
            id='graph',
            figure=fd.create_chart_from_matrix(*fd.mandelbrot_set(XMIN_DEFAULT, XMAX_DEFAULT, YMIN_DEFAULT, YMAX_DEFAULT))
        ),

        dcc.Slider(
            id='iterations',
            min=0,
            max=500,
            marks={int(val): {'label': str(int(val))} for val in np.linspace(0, 500, 11)},
            value=250,
        ),

    ])
])


@app.callback(
    Output('graph', 'figure'),
    [Input('iterations', 'value'),
     Input('graph', 'relayoutData')])
def display_selected_data(iterations, relayoutData):
    start = time.time()

    if relayoutData:
        xmin = relayoutData['xaxis.range[0]']
        xmax = relayoutData['xaxis.range[1]']
        ymin = relayoutData['yaxis.range[0]']
        ymax = relayoutData['yaxis.range[1]']
    else:
        xmin=XMIN_DEFAULT
        xmax=XMAX_DEFAULT
        ymin=YMIN_DEFAULT
        ymax=YMAX_DEFAULT

    fig = fd.create_chart_from_matrix(*fd.mandelbrot_set(xmin, xmax, ymin, ymax, maxiter=iterations))
    end = time.time()
    print(end - start)
    return fig


################################################################################


if __name__ == '__main__':
    app.run_server(debug=True)
