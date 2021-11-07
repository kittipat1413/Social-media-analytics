import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pathlib
from app import app

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()

channel = ['facebook', 'instagram', 'twitter', 'youtube']

df_day_vs_time = pd.read_csv(DATA_PATH.joinpath("df_day_vs_time.csv"))
df_day_vs_time.set_index(['channel', 'day'], inplace=True)
df_channel_engagement = pd.read_csv(DATA_PATH.joinpath("df_channel_engagement.csv"))
df_channel_account_top_engagement = pd.read_csv(DATA_PATH.joinpath("df_channel_account_top_engagement.csv"))
df_unique_name_channel = pd.read_csv(DATA_PATH.joinpath("df_unique_name_channel.csv"))
df_fan_each_month = pd.read_csv(DATA_PATH.joinpath("df_fan_each_month.csv"))


layout = html.Div([

                    # First row
                    html.Div([
                        # First part in row
                        html.Div([
                            html.H2("Most popular social media platform by account"),
                            dcc.Graph(id="graph")
                                ], className="six columns"),

                        # Second part in row
                        html.Div([
                            html.H2("Most popular social media platform by engagement"),
                            dcc.Graph(id="graph2")
                                ], className="six columns"),

                            ], className="row"),

                    # Second row
                    html.Div([
                        
                        html.Div([
                            html.H2("Top account by platform"),

                            dcc.Dropdown(
                                        id='channel2',
                                        options=[{"value": x, "label": x}
                                                for x in channel],
                                        value='youtube'
                                        ),

                            dcc.Dropdown(
                                        id='top_filter',
                                        options=[{"value": x, "label": "Top " + str(x) }
                                        for x in range(5,16,5)],
                                        value='5'
                                        ),

                            dcc.Graph(id="graph4")

                                ]),

                            ], className="row"),

                    # Third row
                    html.Div([
                        
                        # First part in row
                        
                        html.H2("Fan growth by account in 2020"),

                        dcc.Dropdown(
                                    id='mapped_name',
                                    options=[{"value": x, "label": x}
                                            for x in df_unique_name_channel['mapped_name'].drop_duplicates()],
                                    value='Kayavine'
                                    ),

                        dcc.Graph(id="graph5"),

                            ], className="row"),

                    # Forth row
                    html.Div([
                        
                        # First part in row
                        html.Div([
                            html.H2("Best time to post on social media"),

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
    Output("graph3", "figure"),
    Output("graph4", "figure"),
    Output("graph5", "figure")], 
    [Input("channel", "value"),
    Input("channel2", "value"),
    Input("top_filter", "value"),
    Input("mapped_name", "value")])
def change_filter(channel_drop, channel_drop2, top_drop, mapped_name):
    
    # define donut color
    donut_colors=['#4169E1', '#BA55D3', 'lightskyblue', '#CD5C5C']

    # Donut graph1
    fig_donut = go.Figure(data=[go.Pie(labels=df_channel_engagement['channel'], values=df_channel_engagement['account_id'], hole=.5, marker_colors=donut_colors, sort=False)])
    fig_donut.update_layout(annotations=[dict(text='', x=0.5, y=0.5, font_size=20, showarrow=False)])

    # Donut graph2
    fig_donut2 = go.Figure(data=[go.Pie(labels=df_channel_engagement['channel'], values=df_channel_engagement['new_engagement'], hole=.5, marker_colors=donut_colors, sort=False)])
    fig_donut2.update_layout(annotations=[dict(text='', x=0.5, y=0.5, font_size=20, showarrow=False)])

    # Heatmap chart graph3
    fig_heat3 = px.imshow(df_day_vs_time.loc[channel_drop],
                labels=dict(y="Day of Week", x="Time of Day", color="Engagment"),
                x=df_day_vs_time.columns,
                y=['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'],
                color_continuous_scale='blues'
               )
    fig_heat3.update_layout(xaxis_tickangle=-45)


    # Stack bar chart graph4
    fig_stack = go.Figure(go.Bar
                            (x=df_channel_account_top_engagement[(df_channel_account_top_engagement['channel'] == channel_drop2) & (df_channel_account_top_engagement['type_value'] == 'average_engagement_per_post')].head(int(top_drop))['value'], 
                            y=df_channel_account_top_engagement[(df_channel_account_top_engagement['channel'] == channel_drop2) & (df_channel_account_top_engagement['type_value'] == 'average_engagement_per_post')].head(int(top_drop))['account_display_name'], 
                            name='Average engagement per post',
                            orientation='h',
                            marker=dict(
                                            color='rgba(255,160,122, 0.6)',
                                            line=dict(color='rgba(255,160,122, 1.0)', width=3)
                                        ),
                            text=df_channel_account_top_engagement[(df_channel_account_top_engagement['channel'] == channel_drop2) & (df_channel_account_top_engagement['type_value'] == 'average_engagement_per_post')].head(int(top_drop))['value']
                            )
                        )   
                    
                                    
    fig_stack.add_trace(go.Bar
                        (x=df_channel_account_top_engagement[(df_channel_account_top_engagement['channel'] == channel_drop2) & (df_channel_account_top_engagement['type_value'] == 'fan')].head(int(top_drop))['value'], 
                        y=df_channel_account_top_engagement[(df_channel_account_top_engagement['channel'] == channel_drop2) & (df_channel_account_top_engagement['type_value'] == 'fan')].head(int(top_drop))['account_display_name'], 
                        name='Fan',
                        orientation='h',
                        marker=dict(
                                        color='rgba(135,206,235, 0.6)',
                                        line=dict(color='rgba(135,206,235, 1.0)', width=3)
                                    ),
                        text=df_channel_account_top_engagement[(df_channel_account_top_engagement['channel'] == channel_drop2) & (df_channel_account_top_engagement['type_value'] == 'fan')].head(int(top_drop))['value'],
                        )
                    )

    fig_stack.update_traces(texttemplate='%{text:.3s}', textposition='inside')
    fig_stack.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'})


    # Line chart
    # Define row and column for subplot
    fig_line = make_subplots(rows=4, cols=1)

    df_mapped_name = df_unique_name_channel.loc[df_unique_name_channel['mapped_name'] == mapped_name]
    for index in range(len(df_mapped_name)):

        # set line color
        if df_mapped_name.iloc[index]['channel'] == 'facebook':
            line_col = '#4169E1'
        elif df_mapped_name.iloc[index]['channel'] == 'instagram':
            line_col = '#BA55D3'
        elif df_mapped_name.iloc[index]['channel'] == 'twitter':
            line_col = 'lightskyblue'
        elif df_mapped_name.iloc[index]['channel'] == 'youtube':
            line_col = '#CD5C5C'

        filters = (df_fan_each_month['mapped_name'] == df_mapped_name.iloc[index]['mapped_name']) & (df_fan_each_month['channel'] == df_mapped_name.iloc[index]['channel'])

        fig_line.add_trace(
                    go.Scatter(
                                x=df_fan_each_month.loc[filters, 'month'],
                                y=df_fan_each_month.loc[filters, 'fan'],
                                name=df_mapped_name.iloc[index]['channel'], # legend name
                                line=dict(color=line_col, width=2),
                                connectgaps=True # override default to connect the gaps
                            
                    ),row=index+1, col=1,)

    fig_line.update_layout(height=700)
    fig_line.update_yaxes(title_text='Fan')


    return fig_donut, fig_donut2, fig_heat3, fig_stack, fig_line

