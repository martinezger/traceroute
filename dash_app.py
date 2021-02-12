import random

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import os


def map_trace(df_traces, trace_color, index):
    return go.Scattergeo(
        locationmode="USA-states",
        lon=[df_traces["LONGITUDE"][index - 1], df_traces["LONGITUDE"][index]],
        lat=[df_traces["LATITUDE"][index - 1], df_traces["LATITUDE"][index]],
        mode="lines+text",
        text=[df_traces['CITY'][index - 1], df_traces['CITY'][index]],
        line=dict(width=2, color=trace_color),
        hovertext=f"{df_traces['CITY'][index]} - {df_traces['DATE_CREATED'][index]}",
    )


def random_color():
    r = lambda: random.randint(0, 255)
    return ('#%02X%02X%02X' % (r(), r(), r()))


def create_app():
    external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

    app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

    df_traces = pd.read_csv(os.getenv("CSV_DATA"))
    df_traces.head()

    fig = go.Figure()
    control_cut = "red"

    for i in range(1, len(df_traces)):
        fig.add_trace(
            map_trace(df_traces=df_traces, trace_color=random_color(), index=i)
        )

    fig.update_layout(
        title_text="Traces",
        showlegend=False,
        geo=dict(
            projection_type="natural earth",
            showland=True,
            landcolor="rgb(243, 243, 243)",
            countrycolor="rgb(204, 204, 204)",
        ),
    )

    app.layout = html.Div(
        children=[
            html.H1(children="Traces Dashboard"),
            html.Div(
                children="""
            Traces.
        """
            ),
            dcc.Graph(id="example-graph", figure=fig, style={"height": 800},),
        ]
    )
    return app


if __name__ == "__main__":
    app = create_app()
    app.run_server(debug=True)
