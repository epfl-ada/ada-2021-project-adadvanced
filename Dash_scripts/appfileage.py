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

# Colors to be used in the bar chart
color_discrete_map = ['#FF5B5B',"#FFF992",'#7BD787']

# Import the datas
age_df = pd.read_csv("datas/dash_data_age.csv",index_col="Age")
age_df_percentage = (age_df*100) / age_df.sum(axis=1).values.reshape(-1,1)

# Import the datas
UK_age_df = pd.read_csv("datas/dash_data_UK_age.csv",index_col="Age")
UK_age_df_percentage = (UK_age_df*100) / UK_age_df.sum(axis=1).values.reshape(-1,1)

# Get p-values files
P_val_df = pd.read_csv("datas/dash_datas_age_p_value.csv",index_col=0)
P_val_df_UK = pd.read_csv("datas/dash_datas_age_UK_p_value.csv",index_col=0)

# X values for the bar chart
x_values = list(age_df.index.astype(str))
x_values = ["Age " + age for age in x_values]

# Options available 
graph_type = ["Percentage","Absolute"]

options = [{"label": gtype, "value": gtype,
            "style" : {"color":"black","font-family":"Helvetica","font-size": 18}} 
            for gtype in list(graph_type)]

UK_opt = ["World","United kingdom"]

options_UK = [{"label": gtype, "value": gtype,
                "style" : {"color":"black","font-family":"Helvetica","font-size": 18}} 
                for gtype in list(UK_opt)]

# Define the layout of the application
app.layout = html.Div([dcc.Graph(id="heat-map",responsive=True),
                      html.Div([
                        html.Div([dcc.RadioItems(id='drop-down',
                                       options=options,
                                       labelStyle={'display': 'inline-block',
                                                "color":"black",
                                                "font-family":"Helvetica",
                                                "font-size": 18},
                                       value="Percentage")],
                                    style={"display":"inline-block","margin-left":"5%"}),
                        html.Div([dcc.RadioItems(id='drop-down-UK',
                                       options=options_UK,
                                       labelStyle={'display': 'inline-block',
                                                "color":"black",
                                                "font-family":"Helvetica",
                                                "font-size": 18},
                                       value="World")],
                                    style={"display":"inline-block","margin-left":"5%"}),]),
                        dcc.Graph(id="bar-chart",responsive=True)
    ]
)


# Update the bar chart
@app.callback([Output("bar-chart", "figure"),Output("heat-map", "figure")],
              [Input("drop-down","value"),Input("drop-down-UK","value")])
def update_bars(value_selected,value_UK):
    # Percentage or absolute 
    if value_UK == "United kingdom":
        df = UK_age_df
    else:
        df = age_df
    if value_selected == "Percentage":
        df = (df*100) / df.sum(axis=1).values.reshape(-1,1)

    fig = go.Figure()

    # for each type of sentiment 
    for i,col in enumerate(df.columns):
        trace = go.Bar(name = col, x=x_values, y = df[col].values, 
                       marker=dict(color=color_discrete_map[i]))
        fig.add_trace(trace)
    
    # Tune the figure
    fig.update_layout(paper_bgcolor="white",plot_bgcolor="white",
                      title = {'text': "Perception of Brexit by the different age groups",
                      'y':0.03,
                      'x':0.5,
                      'xanchor': 'center',
                      'yanchor': 'bottom',"font":{"family":"Helvetica","size":22}},
                      legend={"font":{"family":"Helvetica","size":16},
                      "orientation":"h",
                      "yanchor":"top",
                      "y":1.2,
                      "xanchor":"center",
                      "x":0.5})
    
    # Do not show y axis if it is percentage 
    if value_selected == "Percentage":
        fig.update_yaxes(title=dict(text="Percentage",font={"family":"Helvetica"}))
    else:
        fig.update_yaxes(title=dict(text="Number of speakers",font={"family":"Helvetica"}))

    fig_heat = make_subplots(rows=1,cols=2,horizontal_spacing=0.2,
                            subplot_titles=("Result of the Welch's t-test (p-values) <br>[United Kingdom]",
                                                           "Result of the Welch's t-test (p-values)"))

    # Heat maps 
    fig_world = px.imshow(P_val_df,range_color=[0,1],labels=dict(color="p-value"))
    fig_UK = px.imshow(P_val_df_UK,range_color=[0,1],labels=dict(color="p-value"))
    # Add the trace 
    for trace in fig_UK["data"]:
        fig_heat.add_trace(trace,1,1)
    for trace in fig_world["data"]:
        fig_heat.add_trace(trace,1,2)
    
    fig_heat['layout']['xaxis']['title']['font']['family'] = 'Helvetica'
    fig_heat['layout']['xaxis2']['title']['font']['family'] = 'Helvetica'
    fig_heat['layout']['yaxis']['title']['font']['family'] = 'Helvetica'
    fig_heat['layout']['yaxis2']['title']['font']['family'] = 'Helvetica'
    fig_heat['layout']['titlefont']['family'] = 'Helvetica'
    return fig, fig_heat

if __name__ == '__main__':
    app.run_server()