import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pathlib
from app import app

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

channel = ['facebook', 'instagram', 'twitter', 'youtube']

df_day_vs_time = pd.read_csv(DATA_PATH.joinpath("df_day_vs_time.csv"))
df_day_vs_time.set_index(['channel', 'day'], inplace=True)
df_channel_engagement = pd.read_csv(DATA_PATH.joinpath("df_channel_engagement.csv"))
df_channel_account_top_engagement = pd.read_csv(DATA_PATH.joinpath("df_channel_account_top_engagement.csv"))

layout = html.Div([

                    # First row
                    html.Div([
                        # First part in row
                        html.Div([
                            html.H2("Most popular channel by influencer"),
                            dcc.Graph(id="graph")
                                ], className="six columns"),

                        # Second part in row
                        html.Div([
                            html.H2("Most popular channel by engagement"),
                            dcc.Graph(id="graph2")
                                ], className="six columns"),

                            ], className="row"),

                    # Second row
                    html.Div([
                        
                        # First part in row
                        html.Div([
                            html.H2("Best time to post by channel"),

                            dcc.Dropdown(
                                        id='channel',
                                        options=[{"value": x, "label": x}
                                                for x in channel],
                                        value='facebook'
                                        ),

                            dcc.Graph(id="graph3")
                                ]),

                            ], className="row")
                ])

@app.callback(
    [Output("graph", "figure"),
    Output("graph2", "figure"),
    Output("graph3", "figure")], 
    Input("channel", "value"))
def change_channel(channel_drop):
    
    # define donut color
    donut_colors=['#104E8B', '#9A32CD', 'lightskyblue', '#B22222']

    # Donut graph1
    fig_donut = go.Figure(data=[go.Pie(labels=df_channel_engagement['channel'], values=df_channel_engagement['account_id'], hole=.5, marker_colors=donut_colors, sort=False)])
    fig_donut.update_layout(annotations=[dict(text='Channel', x=0.5, y=0.5, font_size=20, showarrow=False)])

    # Donut graph2
    fig_donut2 = go.Figure(data=[go.Pie(labels=df_channel_engagement['channel'], values=df_channel_engagement['new_engagement'], hole=.5, marker_colors=donut_colors, sort=False)])
    fig_donut2.update_layout(annotations=[dict(text='Channel', x=0.5, y=0.5, font_size=20, showarrow=False)])

    # Heatmap chart
    fig_heat3 = px.imshow(df_day_vs_time.loc[channel_drop],
                labels=dict(y="Day of Week", x="Time of Day", color="Engagment(%)"),
                x=df_day_vs_time.columns,
                y=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                color_continuous_scale='blues'
               )
    fig_heat3.update_layout(xaxis_tickangle=-45)

    return fig_donut, fig_donut2, fig_heat3

