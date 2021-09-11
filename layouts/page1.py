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
                        html.H2("Time VS Day by engagement of each channel"),

                        dcc.Dropdown(
                            id='channel',
                            options=[{"value": x, "label": x}
                                    for x in channel],
                            value='facebook'
                        ),

                        dcc.Graph(id="graph")
                    ], className="eight columns"),

                    # Second part in row
                    html.Div([
                        html.H2("Ratio of engagement of each channel"),

                        html.Br(),

                        dcc.Graph(id="graph2")
                    ], className="four columns"),

                ], className="row"),

                # Second row
                html.Div([
                    
                    # First part in row
                    html.Div([
                        
                        html.H2("Top 15 engagement of each platform"),

                        dcc.Dropdown(
                            id='channel2',
                            options=[{"value": x, "label": x}
                                    for x in channel],
                            value='facebook'
                        ),

                        dcc.Dropdown(
                            id='top_filter',
                            options=[{"value": x, "label": "Top " + str(x) }
                                    for x in range(5,31,5)],
                            value='5'
                        ),

                        dcc.Graph(id="graph3")
                    ], className="eight columns"),

                    # Second part in row
                    html.Div([
                        html.H2("Ratio of engagement of each channel"),

                        html.Br(),

                        dcc.Graph(id="graph4")
                    ], className="four columns"),

                ], className="row")
])

@app.callback(
    [Output("graph", "figure"),
    Output("graph2", "figure"),
    Output("graph3", "figure"),
    Output("graph4", "figure")], 
    [Input("channel", "value"),
    Input("channel2", "value"),
    Input("top_filter", "value")])
def change_channel(channel_drop, channel_drop2, top_drop):
    fig_graph1 = px.imshow(df_day_vs_time.loc[channel_drop],
                labels=dict(y="Day of Week", x="Time of Day", color="Engagment(%)"),
                x=df_day_vs_time.columns,
                y=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                color_continuous_scale='blues'
               )


    fig_graph2 = go.Figure(data=[go.Pie(labels=df_channel_engagement['channel'], values=df_channel_engagement['engagement'], hole=.5)])
    fig_graph2.update_layout(annotations=[dict(text='Channel', x=0.5, y=0.5, font_size=20, showarrow=False)])


    fig_graph3 = go.Figure()
    fig_graph3.add_trace(go.Bar(
        y=df_channel_account_top_engagement[df_channel_account_top_engagement['channel'] == channel_drop2].tail(int(top_drop))['account_display_name'],
        x=df_channel_account_top_engagement[df_channel_account_top_engagement['channel'] == channel_drop2].tail(int(top_drop))['engagement'],
        orientation='h',
        marker=dict(
            color='rgba(14, 159, 102, 0.6)',
            line=dict(color='rgba(14, 159, 102, 1.0)', width=3)
        )
    ))


    fig_graph4 = go.Figure(data=[go.Pie(labels=df_channel_engagement['channel'], values=df_channel_engagement['engagement'], hole=.5)])
    fig_graph4.update_layout(annotations=[dict(text='Channel', x=0.5, y=0.5, font_size=20, showarrow=False)])

    return fig_graph1, fig_graph2, fig_graph3, fig_graph4

