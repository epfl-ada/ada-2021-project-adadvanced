import dash
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import statsmodels

# Initialize the app
app = dash.Dash(__name__)
server = app.server

# Import the datas 
dash_datas_action = pd.read_csv("datas/dash_datas_stock_auction.csv.gz",compression="infer")
dash_datas_action.set_index("date",inplace=True)
dash_pearson = pd.read_csv("datas/dash_datas_stock_pearson.csv")
dash_pearson.set_index("action",inplace=True)

# Set the options 
options = [{"label": action, "value": action,
            "style" : {"color":"black","font-family":"Helvetica","font-size": 18}} 
            for action in list(dash_pearson.index)]

# Define the layout of the application
app.layout = html.Div([
                        dcc.Dropdown(id='drop-down',
                                    style={"color":"black",
                                           "font-family":"Helvetica",
                                           "margin-left":"15%",
                                           "width":"70%",
                                           "margin-right":"15%",
                                           "font-size": 18},
                                    options=options,
                                    searchable=False,
                                    value=dash_pearson.index.values[0]),
                        dcc.Graph(id="dashboard",responsive=True)
    ]
)

# Update the dashboard 
@app.callback(Output("dashboard", "figure"),
              Input("drop-down","value"))
def update_action_dashboard(action):
      # Style the dashboard 
      specs=[[{}, {"rowspan":2}],[{}, None]]
      # Initialize the figure 
      fig = make_subplots(rows=2,cols=2,shared_xaxes=True,vertical_spacing=0.25,specs=specs,column_widths=[0.6, 0.4],
                        subplot_titles=("","Pearson coefficient r = " + str(round(dash_pearson.loc[action,"pearson_value"],3)),""))
      # Derivative plot
      fig.add_trace(go.Scatter(x=dash_datas_action.index,y=dash_datas_action.quotes_differential,
                              mode="lines",name="Derivative [quotations]"),row=1,col=1)
      fig.add_trace(go.Scatter(x=dash_datas_action.index,y=dash_datas_action.loc[:,action],
                              mode="lines",name="Derivate's absolute value [" + action + "]"),row=2,col=1)
      # Scatter plots 
      regline_fig = px.scatter(dash_datas_action, x="quotes_differential", y=action, trendline="ols",
                              trendline_color_override="black",color_discrete_sequence=["#ff8812"])
      
      # Transfer trace to the figure 
      for trace in regline_fig["data"]:
            fig.add_trace(trace,row=1,col=2)

      # Tune the figure 
      fig.update_layout(legend=dict(
                        font={"family":"Helvetica"},
                        orientation="h",
                        yanchor="top",
                        y=1.2,
                        xanchor="left",
                        x=0),
                        )
      fig.update_layout(title = {'text': "Correlation between brexit agitation and '" + dash_pearson.loc[action,"Company Name"].lower() + "' auction",
                        'y':0.02,
                        'x':0.5,
                        'xanchor': 'center',
                        'yanchor': 'bottom',"font":{"family":"Helvetica","size":22}})
      fig.update_annotations(font_family='Helvetica')
      fig['layout']['xaxis']['rangeslider']['visible']=True
      fig['layout']['xaxis3']['title']='Date'
      fig['layout']['xaxis3']['title']['font']['family'] = 'Helvetica'
      fig['layout']['xaxis2']['title']='Derivative [quotations]'
      fig['layout']['yaxis2']['title']='Derivative [' + action + ']'
      fig['layout']['yaxis2']['side']= 'right'
      fig['layout']['yaxis2']['title']['font']['family'] = 'Helvetica'
      fig['layout']['xaxis2']['title']['font']['family'] = 'Helvetica'
      fig['layout']['titlefont']['family'] = 'Helvetica'

      fig.update_layout(height=1200)
      return fig

if __name__ == '__main__':
    app.run_server()