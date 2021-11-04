import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pathlib
from app import app
import base64

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()
IMG_PATH = PATH.joinpath("../Image").resolve()


channel = ['facebook', 'instagram', 'twitter', 'youtube']


df_sunburst = pd.read_csv(DATA_PATH.joinpath("df_sunburst.csv"))
df_view_vs_fan = pd.read_csv(DATA_PATH.joinpath("df_view_vs_fan.csv"))
df_ig_img_video = pd.read_csv(DATA_PATH.joinpath("df_ig_img_video.csv"))
df_fb_funnel = pd.read_csv(DATA_PATH.joinpath("df_fb_funnel.csv"))

# change fan_range column to categorical type 
cats = ['300K-500K', '500K-1M', '1M-9M']
from pandas.api.types import CategoricalDtype
cat_type = CategoricalDtype(categories=cats, ordered=True)
df_fb_funnel['fan_range'] = df_fb_funnel['fan_range'].astype(cat_type)

encoded_fb_image = base64.b64encode(open(IMG_PATH.joinpath('fb.png'), 'rb').read())
encoded_tw_image = base64.b64encode(open(IMG_PATH.joinpath('tw.png'), 'rb').read())
encoded_ig_image = base64.b64encode(open(IMG_PATH.joinpath('ig.png'), 'rb').read())
encoded_yt_image = base64.b64encode(open(IMG_PATH.joinpath('yt.png'), 'rb').read())

layout = html.Div([
                
                    # First Header
                    html.Div([

                        # First row
                        html.Div([
                            # First part in row
                            html.Div([
                                        html.Img(src='data:image/png;base64,{}'.format(encoded_fb_image.decode()), height=80)
                                    ], className="one column"),

                            # Second part in row
                            html.Div([
                                        html.H2("Performance between accounts by category")
                                    ], className="eleven columns")
                            
                                ], className="row"),

                        # Second row
                        html.Div([
                            # First part in row
                            html.Div([
                                        html.H5("Category")
                                    ]),
                            # Second part in row
                            html.Div([
                                        dcc.Dropdown(
                                                        id='categ_filter',
                                                        options=[{"value": x, "label": x}
                                                                for x in df_fb_funnel['category'].drop_duplicates()],
                                                        value='Sales and review',
                                                        
                                                    )
                                    ], className="five columns")

                                ], style=dict(display='flex')),

                        # Third row
                        html.Div([

                            # First part in row
                            html.Div([
                                        html.H5("Fan range")
                                    ]),
                                       
                            # Second part in row
                            html.Div([
                                        dcc.Dropdown(
                                                        id='fan_amount_filter',
                                                        value='1M-9M'
                                                    )
                                    ],className="five columns")
                                ], style=dict(display='flex')),

                        #Forth row
                        html.Div([
                            
                            # First part in row
                            html.Div([
                                html.H5("Account1"),
                                dcc.Dropdown(
                                            id='page1_filter',
                                            value='ปันโปร Punpromotion'
                                            )], 
                                            
                                            className="five columns"),
                            # Second part in row
                            html.Div([
                                html.H5("Account2"),
                                dcc.Dropdown(
                                            id='page2_filter',
                                            value='SALE HERE'
                                            )]
                                            
                                            , className="five columns")],
                            className="row"),

                        # Funnel graph
                        dcc.Graph(id="graph9")
                        ,

                    ], className="row"),

                    # Second Header
                    html.Div([
                        # First part in row
                        html.Div([
                            html.Img(src='data:image/png;base64,{}'.format(encoded_ig_image.decode()), height=80)

                                ], className="one column"),

                        # Second part in row
                        html.Div([
                                    html.H2("Performance between image and video post")
                                ], className="nine columns")

                            ], className="row"),

                    # Bar graph
                    dcc.Graph(id="graph8"),

                    # Third header
                    html.Div([
                        
                        # First part in row    
                        html.Div([
                                    html.Img(src='data:image/png;base64,{}'.format(encoded_tw_image.decode()), height=80)
                                ], className="one column"),

                        # Second part in row
                        html.Div([
                                    html.H2("Most popular twitter hashtag in 2020")
                                ], className="six columns")
                        
                            ], className="row"),

                    # Sunburst graph
                    dcc.Graph(id="graph6"),
                    

                    # Forth Header
                    html.Div([

                        # First part in row
                        html.Div([
                            html.Img(src='data:image/png;base64,{}'.format(encoded_yt_image.decode()), height=60)
                                ], className="one column"),
                                
                        # Second part in row
                        html.Div([
                                    html.H2("Relationship between view on average and number of subscriber")
                                ], className="ten columns")

                            ], className="row"),

                    html.Header('Subscriber'),
                    # Fan Slider
                    dcc.RangeSlider(
                                    id='my-slider1',
                                    min=100000,
                                    max=df_view_vs_fan['fan'].max(),
                                    step=5000,
                                    value=[0, df_view_vs_fan['fan'].max()],
                                    tooltip={"placement": "bottom", "always_visible": True},
                                    marks={
                                            100000: {'label': 'Silver', 'style': {'color': '#000000'}},
                                            999999: {'label': 'Gold', 'style': {'color': '#000000'}},
                                            10000000: {'label': 'Diamond', 'style': {'color': '#000000'}}
                                        }
                                    ),

                    html.Header('Average View'),
                    # View Slider
                    dcc.RangeSlider(
                                    id='my-slider2',
                                    min=0,
                                    max=df_view_vs_fan['avg_view'].max(),
                                    step=5000,
                                    value=[0, df_view_vs_fan['avg_view'].max()],
                                    tooltip={"placement": "bottom", "always_visible": True},
                                    marks={
                                            0: {'label': '0%', 'style': {'color': '#000000'}},
                                            df_view_vs_fan['avg_view'].max()*0.25: {'label': '25%', 'style': {'color': '#000000'}},
                                            df_view_vs_fan['avg_view'].max()*0.5: {'label': '50%', 'style': {'color': '#000000'}},
                                            df_view_vs_fan['avg_view'].max()*0.75: {'label': '75%', 'style': {'color': '#000000'}},
                                            int(df_view_vs_fan['avg_view'].max()): {'label': '100%', 'style': {'color': '#000000'}}
                                        }
                                    ),

                    # Scatter graph
                    dcc.Graph(id="graph7"),
                ])

# Set fan_amount dropdown option
@app.callback(
    Output('fan_amount_filter', 'options'),
    Input('categ_filter', 'value'))
def set_fan_amount_options(selected_categ):

    return [{'label': i, 'value': i} for i in df_fb_funnel[df_fb_funnel['category'] == selected_categ]['fan_range'].sort_values().drop_duplicates()]

# Set fan_amount dropdown value
@app.callback(
    Output('fan_amount_filter', 'value'),
    Input('fan_amount_filter', 'options'))
def set_fan_amount_value(available_options):
    return available_options[-1]['value']

# Set page dropdown option
@app.callback(
    [Output('page1_filter', 'options'),
    Output('page2_filter', 'options')],
    [Input('categ_filter', 'value'),
    Input('fan_amount_filter', 'value')])
def set_page_options(selected_categ, selected_fan_amount):
    list_option = [{'label': i, 'value': i} for i in df_fb_funnel[(df_fb_funnel['category'] == selected_categ) & (df_fb_funnel['fan_range'] == selected_fan_amount)]['account_display_name'].drop_duplicates()]    

    return list_option, list_option
# Set page dropdown value
@app.callback(
    [Output('page1_filter', 'value'),
    Output('page2_filter', 'value')],
    [Input('page1_filter', 'options'),
    Input('page2_filter', 'options')])
def set_page_value(available_options1, available_options2):

    return available_options1[0]['value'], available_options2[0]['value']


@app.callback(
    [Output("graph6", "figure"),
    Output("graph7", "figure"),
    Output("graph8", "figure"),
    Output("graph9", "figure")], 
    [Input("page1_filter", "value"),
    Input("page2_filter", "value"),
    Input("categ_filter", "value"),
    Input("fan_amount_filter", "value"),
    Input("my-slider1", "value"),
    Input("my-slider2", "value")])
def change_filter(page1_drop, page2_drop, categ_drop , fan_amount_drop, fan_slider, view_slider):

    # Sunburst chart
    # color_cat=['', '#ABDEE6', '#CBAACB', 'FFFFB5', '#FFCCB6', '#F3B0C3', '#FCB9AA', '#F6EAC2', '#ECEAE4', '#B5EAD7', '#55CBCD']
    color_cat=['', '#ABDEE6', '#CBAACB', '#f8de7e', '#FFCCB6', '#F3B0C3', '#FCB9AA', '#a9ba9d', '#b5b9ff', '#B5EAD7', '#55CBCD']
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
    slide_filter = ((df_view_vs_fan['fan'] >= fan_slider[0]) & (df_view_vs_fan['fan'] <= fan_slider[1]) 
                    & (df_view_vs_fan['avg_view'] >= view_slider[0]) & (df_view_vs_fan['avg_view'] <= view_slider[1]))

    fig_scatter = px.scatter(df_view_vs_fan.loc[slide_filter].sort_values(by='type_fan'), x="fan", y="avg_view", color="type_fan", 
                hover_data=['account_display_name'], 
                # facet_col="type_fan",
                # color_discrete_sequence=['#483D8B', '#DAA520', '#B0C4DE'],
                color_discrete_map={
                "Diamond": "#483D8B",
                "Gold": "#DAA520",
                "Silver": "#B0C4DE"},
                labels={"type_fan": "Group of creator", "fan": "Subscriber", "avg_view": "Average view"}
                )

    # Bar chart
    fig_bar = px.bar(df_ig_img_video, x='avg_engagement', y='post_type', orientation='h', text='avg_engagement', color='post_type', color_discrete_sequence=['#BA55D3', '#A9A9A9'], labels={"post_type": "Post type", "avg_engagement": "Average engagement"})
    fig_bar.update_traces(texttemplate='%{text:.2s}', textposition='inside')
    fig_bar.update_layout(uniformtext_minsize=15, uniformtext_mode='hide', height=300)

    
    # Funnel chart
    fig_funnel = go.Figure()
    list_y = ['Total Engagement', 'Reaction', 'Share', 'Comment', 'Tag friend', 'Purchase intention']
    fig_funnel.add_trace(go.Funnel(
        name = page1_drop,
        y = list_y,
        x = df_fb_funnel[df_fb_funnel['account_display_name'] == page1_drop]['value'],
        textposition = "auto",
        textinfo = "value+percent initial",
        constraintext='outside',
        textfont=dict(
                        size=10,
                        color="black"
                      ),
        marker={"color": ["#A9A9A9", "#A9A9A9", "#A9A9A9", "#A9A9A9", "#A9A9A9", "#A9A9A9"]},
        texttemplate = "%{value:.2s} <br>(%{percentInitial})"
        ))

    fig_funnel.add_trace(go.Funnel(
        name = page2_drop,
        orientation = "h",
        y = list_y,
        x = df_fb_funnel[df_fb_funnel['account_display_name'] == page2_drop]['value'],
        textposition = "auto",
        textinfo = "value+percent initial",
        constraintext='outside',
        textfont=dict(
                        size=10,
                        color="black"
                      ),
        marker={"color": ["#B0C4DE", "#B0C4DE", "#B0C4DE", "#B0C4DE", "#B0C4DE", "#B0C4DE"]},
        texttemplate = "%{value:.2s} <br>(%{percentInitial})"
        ))

    return fig_sunburst, fig_scatter, fig_bar, fig_funnel

