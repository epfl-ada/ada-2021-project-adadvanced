import dash
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd

# Initialize the app
app = dash.Dash(__name__)
server = app.server

color_discrete_map = ['#FF5B5B', "#FFF992", '#7BD787']

age_df = pd.read_csv("datas/dash_data_age.csv", index_col="Age")
age_df_percentage = (age_df * 100) / age_df.sum(axis=1).values.reshape(-1, 1)

x_values = list(age_df.index.astype(str))
x_values = ["Age " + age for age in x_values]

graph_type = ["Percentage", "Absolute"]

options = [{"label": gtype, "value": gtype,
            "style": {"color": "black", "font-family": "Helvetica", "font-size": 18}}
           for gtype in list(graph_type)]

# Define the layout of the application
app.layout = html.Div([
    dcc.Dropdown(id='drop-down',
                 style={"color": "black",
                        "font-family": "Helvetica",
                        "margin-left": "30%",
                        "width": "40%",
                        "margin-right": "30%",
                        "font-size": 18},
                 options=options,
                 searchable=False,
                 value="Percentage"),
    dcc.Graph(id="bar-chart", responsive=True)
]
)


@app.callback(Output("bar-chart", "figure"),
              Input("drop-down", "value"))
def update_bars(value_selected):
    if value_selected == "Percentage":
        df = age_df_percentage
    else:
        df = age_df

    fig = go.Figure()

    for i, col in enumerate(df.columns):
        trace = go.Bar(name=col, x=x_values, y=df[col].values,
                       marker=dict(color=color_discrete_map[i]))
        fig.add_trace(trace)

    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white",
                      title={'text': "How does each age category feels Brexit ?",
                             'y': 0.03,
                             'x': 0.5,
                             'xanchor': 'center',
                             'yanchor': 'bottom', "font": {"family": "Helvetica", "size": 22}},
                      legend={"font": {"family": "Helvetica", "size": 16},
                              "orientation": "h",
                              "yanchor": "top",
                              "y": 1.2,
                              "xanchor": "center",
                              "x": 0.5})

    if value_selected == "Percentage":
        fig.update_yaxes(showticklabels=False)

    return fig


if __name__ == '__main__':
    app.run_server()