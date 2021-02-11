import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import pandas as pd
import os

external_stylesheets = ["https://codepen.io/chriddyp/pen/bWLwgP.css"]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df_traces = pd.read_csv(os.getenv("CSV_DATA"))
df_traces.head()

fig = go.Figure()

fig.add_trace(
    go.Scattergeo(
        locationmode="USA-states",
        lon=[df_traces["LONGITUDE"][0], df_traces["LONGITUDE"][1]],
        lat=[df_traces["LATITUDE"][0], df_traces["LATITUDE"][1]],
        mode="lines+text",
        text=[df_traces['CITY'][0], df_traces['CITY'][1]],
        line=dict(width=2, color="blue"),
        hovertext=f"{df_traces['CITY'][0]}",
    )
)

for i in range(1, len(df_traces)):
    fig.add_trace(
        go.Scattergeo(
            locationmode="USA-states",
            lon=[df_traces["LONGITUDE"][i - 1], df_traces["LONGITUDE"][i]],
            lat=[df_traces["LATITUDE"][i - 1], df_traces["LATITUDE"][i]],
            mode="lines+text",
            text=[df_traces['CITY'][i-1], df_traces['CITY'][i]],
            line=dict(width=2, color="blue"),
            hovertext=f"{df_traces['CITY'][i - 1]}",
        )
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

if __name__ == "__main__":
    app.run_server(debug=True)
