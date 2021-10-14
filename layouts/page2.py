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


df_sunburst = pd.read_csv(DATA_PATH.joinpath("df_sunburst.csv"))
df_view_vs_fan = pd.read_csv(DATA_PATH.joinpath("df_view_vs_fan.csv"))
df_ig_img_video = pd.read_csv(DATA_PATH.joinpath("df_ig_img_video.csv"))
df_fb_funnel = pd.read_csv(DATA_PATH.joinpath("df_fb_funnel.csv"))

layout = html.Div([
                
                    # First row
                    html.Div([
                        # First part in row
                        html.Div([
                            html.H2("Twitter:"),
                            html.H2("Most popular twitter hashtag in 2020"),
                            
                            dcc.Graph(id="graph6")

                                ]),

                            ], className="row"),

                    # Second row
                    html.Div([
                        # First part in row
                        html.Div([
                            html.H2("Youtube:"),
                            html.H2("Relationship between youtube average view and fan"),

                            dcc.Graph(id="graph7")

                                ]),

                            ], className="row"),

                    # Third row
                    html.Div([
                        # First part in row
                        html.Div([
                            html.H2("Instagram:"),
                            html.H2("Comparing performance between image and video post"),

                            dcc.Graph(id="graph8")

                                ]),

                            ], className="row"),

                    # Forth row
                    html.Div([
                        # First part in row
                        html.H2("Facebook:"),
                        html.H2("Comparing performance between pages in same catagory of Facebook"),

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
                                            )]
                                            
                                            , className="five columns")],
                            className="row"),

                        dcc.Graph(id="graph9")
                        ,

                    ], className="row"),
                ])

@app.callback(
    [Output("graph6", "figure"),
    Output("graph7", "figure"),
    Output("graph8", "figure"),
    Output("graph9", "figure")], 
    [Input("page1_filter", "value"),
    Input("page2_filter", "value")])
def change_filter(page1_drop, page2_drop):

    # Sunburst chart
    color_cat=['', '#ABDEE6', '#CBAACB', 'FFFFB5', '#FFCCB6', '#F3B0C3', '#FCB9AA', '#F6EAC2', '#ECEAE4', '#B5EAD7', '#55CBCD']
    fig_sunburst =go.Figure(go.Sunburst(
        labels=df_sunburst['All_label'].to_list(),
        parents=df_sunburst['Parent'].to_list(),
        values=df_sunburst['Value'].to_list(),
        branchvalues='total',
        maxdepth=2,
        marker_colors= color_cat
    ))
    fig_sunburst.update_layout(margin = dict(t=0, l=0, r=0, b=0), font_size=22)


    # Scatter plot
    fig_scatter = px.scatter(df_view_vs_fan, x="fan", y="avg_view", color="type_fan", 
                hover_data=['account_display_name'], 
                # facet_col="type_fan",
                color_discrete_sequence=['#B0C4DE', '#DAA520', '#483D8B'] 
                )


    # Bar chart
    fig_bar = px.bar(df_ig_img_video, x='avg_engagement', y='post_type', orientation='h', text='avg_engagement', color='post_type', color_discrete_sequence=['#BA55D3', '#A9A9A9'])
    # fig_bar = px.bar(df_ig_img_video, x='post_type', y='avg_engagement', text='avg_engagement', color='post_type', color_discrete_sequence=['#BA55D3', '#A9A9A9'])
    fig_bar.update_traces(texttemplate='%{text:.2s}', textposition='inside')
    fig_bar.update_layout(uniformtext_minsize=15, uniformtext_mode='hide', height=300)


    # Funnel chart
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

    return fig_sunburst, fig_scatter, fig_bar, fig_funnel

