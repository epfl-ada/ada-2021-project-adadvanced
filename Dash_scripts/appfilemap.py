import dash
import plotly.express as px
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import geojson

# Initialize the app
app = dash.Dash(__name__)
server = app.server

# Import the mapping between ISO and countries
current_countries = pd.read_csv("datas/countries_to_ISO3.csv")

# Define the select by year function
def select_by_year(low, high, dash_df):
    filter_df = dash_df[(dash_df.date >= low) & (dash_df.date <= high)]
    filter_df.drop(columns="date", inplace=True)
    filter_df = filter_df.groupby("sentiment_score").sum()
    count = filter_df.sum(axis=0)
    filter_df = (filter_df * 100 / filter_df.sum(axis=0)).T.reset_index().rename(columns={"index":"country"})
    filter_df["count"] = count.values
    filter_df = filter_df[filter_df["count"] > 40]
    filter_df["Sentiment"] = -1*filter_df.Negative + filter_df.Positive
    filter_df = pd.merge(filter_df,current_countries,left_on="country",right_on="Country",how="left").drop(columns=["country"])
    return filter_df

# Get the geojson file
with open("datas/countries.geojson") as file:
    country_gj = geojson.load(file)

# Get the datas 
dash_data = pd.read_csv("datas/dash_data_country.csv.gz",compression="infer")

marks_slider = {year:{"label" : str(year),
               "style" : {"color":"black","font-family":"Helvetica","font-size": 18}} 
               for year in range(dash_data.date.min()+1,dash_data.date.max()+1)}

# Define the layout of the application
app.layout = html.Div([
        html.P("Year",style={"display": "flex",
                             "font-family":"Helvetica",
                             "font-size": 18,
                             "align-items": "center",
                             "justify-content": "center"}),
        dcc.RangeSlider(
            id='range-slider',
            min=dash_data.date.min()+1, max=dash_data.date.max(), step=1,
            marks=marks_slider,
            value=[2016,2020]),
        dcc.Loading(
            id="loading-map",
            type="circle",
            children=[html.Div(dcc.Graph(id="map-plot",responsive=True))])
        ]
        )

@app.callback(Output("map-plot", "figure"),
              Input("range-slider","value"))
def update_map(slider_range):
    low, high = slider_range
    country_analysis = select_by_year(low, high, dash_data)
    fig = px.choropleth_mapbox(country_analysis, geojson=country_gj, locations='ISO3', color='Sentiment',
                               featureidkey="properties.ISO_A3",
                               range_color=[-10,35],
                               color_continuous_scale="RdYlGn",
                               mapbox_style="carto-positron",
                               zoom=2.5, center = {"lat": 48.856613, "lon": 2.352222},
                               opacity=0.6,hover_data=["Country","count"])
    fig.update_layout(title={'text': "Evolution of the sentiment towards Brexit over the countries [" + str(low) + " - "+ str(high) + "]",
                             'y':0.03,
                             'x':0.5,
                             'xanchor': 'center',
                             'yanchor': 'bottom'},legend_font_family="Helvetica",legend_xanchor="center",
                             legend_yanchor="bottom",
                             title_font_family="Helvetica",title_font_size=20)
    fig.update_layout(height=1200,width=1600)
    return fig

if __name__ == '__main__':
    app.run_server()