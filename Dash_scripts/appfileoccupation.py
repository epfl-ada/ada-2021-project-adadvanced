import dash
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd

# Initialize the app
app = dash.Dash(__name__)
server = app.server

color_discrete_map = ['#FF5B5B',"#FFF992",'#7BD787']

def select_by_year_occupation(low,high,dash_df):
    filter_df = dash_df[(dash_df.date >= low) & (dash_df.date <= high)]
    filter_df.drop(columns="date",inplace=True)
    filter_df = filter_df.groupby("sentiment_score").sum()
    count = filter_df.sum(axis=0)
    filter_df = filter_df.T.reset_index().rename(columns={"index":"occupation"})
    filter_df["count"] = count.values
    return filter_df

# Get the datas
dash_data = pd.read_csv("datas/dash_data_occupation.csv.gz",compression="infer")
occupations = list(dash_data.columns[:-2])

marks_slider = {year:{"label" : str(year),
               "style" : {"color":"black","font-family":"Helvetica","font-size": 18}}
               for year in range(dash_data.date.min()+1,dash_data.date.max()+1)}

options = [{"label": occup, "value": occup,
            "style" : {"color":"black","font-family":"Helvetica","font-size": 18}}
            for occup in list(occupations)]

# Define the layout of the application
app.layout = html.Div([
        html.Div([
        html.Div([html.P("Year",style={"display": "flex",
                                "font-family":"Helvetica",
                                "font-size": 18,
                                "align-items": "center",
                                "justify-content": "center"}),
                            dcc.RangeSlider(
                                id='range-slider',
                                min=dash_data.date.min()+1, max=dash_data.date.max(), step=1,
                                marks=marks_slider,
                                value=[dash_data.date.min()+1,dash_data.date.max()])],
                            style = {"display":"inline-block","width":"35%","margin-left":"5%"}),
        html.Div([dcc.Dropdown(id='drop-down',multi=True,
                               style={"color":"black","font-family":"Helvetica","font-size": 18},
                               options=options,value=["Art","Health","Economy"])],
                 style = {"display":"inline-block","width":"50%","margin-left":"5%","margin-right":"5%"})
        ]),
        dcc.Graph(id="pie-chart",responsive=True)
    ])


@app.callback([Output("pie-chart", "figure"),Output("drop-down","options")],
              [Input("range-slider","value"),Input("drop-down","value")])
def update_pies(slider_range,values_selected):
    low, high = slider_range
    sector_analysis = select_by_year_occupation(low,high,dash_data)
    occupations = list(sector_analysis.occupation)
    options = [{"label": occup, "value": occup,
                "style" : {"color":"black","font-family":"Helvetica","font-size": 18}}
                for occup in list(occupations)]
    values_selected = list(set(values_selected) & set(occupations))
    sector_analysis = sector_analysis[sector_analysis["occupation"].isin(values_selected)]
    labels = list(sector_analysis.columns[-4:-1])
    fig = make_subplots(rows=1,cols=len(sector_analysis),specs=[[{"type":"domain"}]*len(sector_analysis)])
    start = 1
    for index, row in sector_analysis.iterrows():
        trace = go.Pie(labels=labels,
                       values=sector_analysis.loc[index,labels].values,
                       name=row["occupation"],
                       title=row["occupation"])
        fig.add_trace(trace,row =1,col=start)
        start += 1
    fig.update_traces(hole=.4, hoverinfo="label+percent+name",marker = dict(colors=color_discrete_map),textinfo='none')
    return fig, options

if __name__ == '__main__':
    app.run_server()