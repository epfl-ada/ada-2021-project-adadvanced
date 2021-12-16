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

# Colors that will be displayed on the pie charts 
color_discrete_map = ['#FF5B5B',"#FFF992",'#7BD787',"#000000"]

# Define a function that will be used in further studies 
# This function returns a subset of features about quotations
# And this function filters also the dataset according to a year range
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
P_val_df = pd.read_csv("datas/dash_datas_sector_p_values.csv",index_col=0)

# Get the list of the occupations
occupations = list(dash_data.columns[:-2])

# Define the marks for the slider 
marks_slider = {year:{"label" : str(year),
               "style" : {"color":"black","font-family":"Helvetica","font-size": 18}} 
               for year in range(dash_data.date.min()+1,dash_data.date.max()+1)}

# Define the options for the dropdown
options = [{"label": occup, "value": occup,
            "style" : {"color":"black","font-family":"Helvetica","font-size": 18}} 
            for occup in list(occupations)]

# Define the layout of the application
app.layout = html.Div([
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
                            style = {"width":"60%","margin-bottom":25,"margin-left":"20%","width":"60%","margin-right":"20%"}),
        html.Div([dcc.Dropdown(id='drop-down',multi=True,
                               style={"color":"black","font-family":"Helvetica","font-size": 18},
                               options=options,value=["Art","Health","Economy"])],
                 style = {"width":"60%","margin-left":"20%","margin-right":"20%"}),
        html.Div([dcc.Graph(id="pie-chart",responsive=True)])
    ])


# function that will update pies and drop down values 
@app.callback(Output("pie-chart", "figure"),
              [Input("range-slider","value"),Input("drop-down","value")])
def update_pies(slider_range,values_selected):
    # get the year range wanted 
    low, high = slider_range
    # Filter according to the year 
    sector_analysis = select_by_year_occupation(low,high,dash_data)
    # Filter by the sectors that are specified in the dropdown list
    sector_analysis = sector_analysis[sector_analysis["occupation"].isin(values_selected)]
    # labels for graph
    labels = list(sector_analysis.columns[-4:-1])
    # Initialize the figure 
    fig = make_subplots(rows=1,cols=len(sector_analysis),specs=[[{"type":"domain"}]*len(sector_analysis)])
    start = 1
    # Sort by count 
    sector_analysis.sort_values(by="count",ascending=False,inplace=True)
    # Loop over the sector analysis rows 
    for index, row in sector_analysis.iterrows():
        # If count lower than 40 then not enough data to well represent the sector
        if row["count"] < 40:
            trace = go.Pie(labels=labels + ["Not enough data"],
                           values=[0,0,0,1],
                           name=row["occupation"],
                           title=row["occupation"])
        else:
            trace = go.Pie(labels=labels,
                            values=row[labels].values,
                            name=row["occupation"],
                            title=row["occupation"])
        # Add the trace 
        fig.add_trace(trace,row =1,col=start)
        start += 1
    # Tune the figure 
    fig.update_traces(hole=.4, hoverinfo="label+percent+name",marker = dict(colors=color_discrete_map),textinfo='none')
    fig.update_layout(title = {'text': "Semtiment towards Brexit by sector",
                        'y':0.05,
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'bottom',"font":{"family":"Helvetica","size":20}},
                        legend={"font":{"family":"Helvetica","size":16},
                        "orientation":"h",
                        "yanchor":"top",
                        "y":1.2,
                        "xanchor":"center",
                        "x":0.5})
    return fig

if __name__ == '__main__':
    app.run_server()