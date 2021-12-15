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

# X values for the bar chart
x_values = list(age_df.index.astype(str))
x_values = ["Age " + age for age in x_values]

# Options available 
graph_type = ["Percentage","Absolute"]

options = [{"label": gtype, "value": gtype,
            "style" : {"color":"black","font-family":"Helvetica","font-size": 18}} 
            for gtype in list(graph_type)]

# Define the layout of the application
app.layout = html.Div([
                        html.Div([dcc.RadioItems(id='drop-down',
                                       options=options,
                                       labelStyle={'display': 'inline-block',
                                                "color":"black",
                                                "font-family":"Helvetica",
                                                "font-size": 18},
                                       value="Percentage")],
                                    style={"margin-left":"43%","width":"20%","margin-right":"37%"}),
                        dcc.Graph(id="bar-chart",responsive=True)
    ]
)


# Update the bar chart
@app.callback(Output("bar-chart", "figure"),
              Input("drop-down","value"))
def update_bars(value_selected):
    # Percentage or absolute 
    if value_selected == "Percentage":
        df = age_df_percentage
    else:
        df = age_df

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
    
    return fig

if __name__ == '__main__':
    app.run_server()