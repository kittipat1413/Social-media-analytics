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


df_channel_account_top_engagement = pd.read_csv(DATA_PATH.joinpath("df_channel_account_top_engagement.csv"))
df_ig_img_video = pd.read_csv(DATA_PATH.joinpath("df_ig_img_video.csv"))
df_fb_funnel = pd.read_csv(DATA_PATH.joinpath("df_fb_funnel.csv"))

layout = html.Div([
                
                    # First row
                    html.Div([
                        # First part in row
                        html.Div([
                            html.H2("Most popular influencers by channel"),
                            
                            dcc.Dropdown(
                                        id='channel2',
                                        options=[{"value": x, "label": x}
                                                for x in channel],
                                        value='facebook'
                                        ),

                            dcc.Dropdown(
                                        id='top_filter',
                                        options=[{"value": x, "label": "Top " + str(x) }
                                        for x in range(5,16,5)],
                                        value='5'
                                        ),

                            dcc.Graph(id="graph4")
                                
                            ],className="box",
                            style={
                                'width': '100%',
                            })

                        ], className="customrow"),

                    # Second row
                    html.Div([
                        # First part in row
                        html.Div([
                                html.H3("Comparing performance between image and video post in Instagram"),                             
                                html.Br(),
                                dcc.Graph(id="graph5")
                            ],className="box",
                            style={
                                'width': '35%',
                            }),

                        # Second part in row
                        
                        html.Div([
                                html.H3("Comparing performance between pages in same catagory of Facebook"),
                                html.Br(),
                                html.Div([
                                    html.Div([

                                        dcc.Dropdown(
                                                    id='page1_filter',
                                                    options=[{"value": x, "label": x}
                                                            for x in df_fb_funnel['account_display_name'].drop_duplicates()],
                                                    value='ปันโปร - Punpromotion'
                                                    )
                                                    ], className="five columns"),

                                    html.Div([

                                        dcc.Dropdown(
                                                    id='page2_filter',
                                                    options=[{"value": x, "label": x}
                                                    for x in df_fb_funnel['account_display_name'].drop_duplicates()],
                                                    value='SALE HERE'
                                                    )
                                                    ], className="five columns")],
                                className="row"),

                                dcc.Graph(id="graph6")],className="box",
                                style={
                                'width': '65%',
                            })
                            
                    ],
                    className="customrow"),
                    
                    # # Third row

                    # html.Div([
                    #     # First part in row
                    #     html.Div([
                    #         html.H2("Comparing performance between image and video post in Instagram"),
                    #         dcc.Graph(id="graph5")
                    #     ], className="six columns"),

                    #     # Second part in row
                    #     html.Div([
                    #         html.H2("Comparing performance between pages in same catagory"),
                    #         dcc.Graph(id="graph6")
                    #     ], className="six columns"),

                    # ], className="row")
                ])

@app.callback(
    [Output("graph4", "figure"),
    Output("graph5", "figure"),
    Output("graph6", "figure")], 
    [Input("channel2", "value"),
    Input("top_filter", "value"), 
    Input("page1_filter", "value"),
    Input("page2_filter", "value")])
def change_channel(channel_drop, top_drop, page1_drop, page2_drop):

    # Stack bar chart
    fig_stack = go.Figure(go.Bar
                            (x=df_channel_account_top_engagement[(df_channel_account_top_engagement['channel'] == channel_drop) & (df_channel_account_top_engagement['type_value'] == 'average_engagement_per_post')].head(int(top_drop))['value'], 
                            y=df_channel_account_top_engagement[(df_channel_account_top_engagement['channel'] == channel_drop) & (df_channel_account_top_engagement['type_value'] == 'average_engagement_per_post')].head(int(top_drop))['account_display_name'], 
                            name='Average engagement per post',
                            orientation='h',
                            marker=dict(
                                            color='rgba(255,99,71, 0.6)',
                                            line=dict(color='rgba(255,99,71, 1.0)', width=3)
                                        ),
                            text=df_channel_account_top_engagement[(df_channel_account_top_engagement['channel'] == channel_drop) & (df_channel_account_top_engagement['type_value'] == 'average_engagement_per_post')].head(int(top_drop))['value']
                            )
                        )   
                    
                                    
    fig_stack.add_trace(go.Bar
                        (x=df_channel_account_top_engagement[(df_channel_account_top_engagement['channel'] == channel_drop) & (df_channel_account_top_engagement['type_value'] == 'fan')].head(int(top_drop))['value'], 
                        y=df_channel_account_top_engagement[(df_channel_account_top_engagement['channel'] == channel_drop) & (df_channel_account_top_engagement['type_value'] == 'fan')].head(int(top_drop))['account_display_name'], 
                        name='Fan',
                        orientation='h',
                        marker=dict(
                                        color='rgba(74,128,140, 0.6)',
                                        line=dict(color='rgba(74,128,140, 1.0)', width=3)
                                    ),
                        text=df_channel_account_top_engagement[(df_channel_account_top_engagement['channel'] == channel_drop) & (df_channel_account_top_engagement['type_value'] == 'fan')].head(int(top_drop))['value'],
                        )
                    )

    fig_stack.update_traces(texttemplate='%{text:.3s}', textposition='inside')
    fig_stack.update_layout(barmode='stack', yaxis={'categoryorder':'total ascending'})

    # Bar chart
    #fig_bar = px.bar(df_ig_img_video, x='avg_engagement', y='post_type', orientation='h', text='avg_engagement', color='post_type', color_discrete_sequence=['#9400D3', '#A9A9A9'])
    fig_bar = px.bar(df_ig_img_video, x='post_type', y='avg_engagement', text='avg_engagement', color='post_type', color_discrete_sequence=['#9400D3', '#A9A9A9'])
    fig_bar.update_traces(texttemplate='%{text:.2s}', textposition='inside')
    fig_bar.update_layout(uniformtext_minsize=15, uniformtext_mode='hide')

    fig_funnel = go.Figure()

    list_y = ['Engagement', 'Reaction', 'Positive Reaction', 'Share', 'Tag friend', 'Purchase intention']
    fig_funnel.add_trace(go.Funnel(
        name = df_fb_funnel[df_fb_funnel['account_display_name'] == page1_drop]['account_display_name'].unique()[0],
        y = list_y,
        x = df_fb_funnel[df_fb_funnel['account_display_name'] == page1_drop]['value'],
        textposition = "auto",
        textinfo = "percent initial",
        constraintext='outside',
        textfont=dict(
                        size=14,
                        color="black"
                      ),
        marker={"color": ["#A9A9A9", "#A9A9A9", "#A9A9A9", "#A9A9A9", "#A9A9A9"]}
        ))

    fig_funnel.add_trace(go.Funnel(
        name = df_fb_funnel[df_fb_funnel['account_display_name'] == page2_drop]['account_display_name'].unique()[0],
        orientation = "h",
        y = list_y,
        x = df_fb_funnel[df_fb_funnel['account_display_name'] == page2_drop]['value'],
        textposition = "auto",
        textinfo = "percent initial",
        constraintext='outside',
        textfont=dict(
                        size=14,
                        color="black"
                      ),
        marker={"color": ["#B0C4DE", "#B0C4DE", "#B0C4DE", "#B0C4DE", "#B0C4DE"]}
        ))

    return fig_stack, fig_bar, fig_funnel

