import pandas as pd
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pathlib
from app import app
import base64
from pandas.api.types import CategoricalDtype

PATH = pathlib.Path(__file__).parent
DATA_PATH = PATH.joinpath("../datasets").resolve()
IMG_PATH = PATH.joinpath("../Image").resolve()


channel = ['facebook', 'instagram', 'twitter', 'youtube']


df_sunburst = pd.read_csv(DATA_PATH.joinpath("df_sunburst.csv"))
df_view_vs_fan = pd.read_csv(DATA_PATH.joinpath("df_view_vs_fan.csv"))
df_ig_img_video = pd.read_csv(DATA_PATH.joinpath("df_ig_img_video.csv"))
df_fb_funnel = pd.read_csv(DATA_PATH.joinpath("df_fb_funnel.csv"))

# change fan_range column to categorical type 
cats = ['Less than 0.5M', '0.5M-1M', 'More than 1M']
cat_type = CategoricalDtype(categories=cats, ordered=True)
df_fb_funnel['fan_range'] = df_fb_funnel['fan_range'].astype(cat_type)


# change fan_type column to categorical type fan_cats = ['Diamond', 'Gold', 'Silver', 'Highlighted']
fan_cats = ['Diamond', 'Gold', 'Silver', 'Filtered by dropdown']
fan_type = CategoricalDtype(categories=fan_cats, ordered=True)
df_view_vs_fan['type_fan'] = df_view_vs_fan['type_fan'].astype(fan_type)

# change fan_type column to categorical type fan_cats = ['Diamond', 'Gold', 'Silver', 'Highlighted']
month_cats = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
cat_type = CategoricalDtype(categories=month_cats, ordered=True)
df_view_vs_fan['month'] = df_view_vs_fan['month'].astype(cat_type)

encoded_fb_image = base64.b64encode(open(IMG_PATH.joinpath('fb.png'), 'rb').read())
encoded_tw_image = base64.b64encode(open(IMG_PATH.joinpath('tw.png'), 'rb').read())
encoded_ig_image = base64.b64encode(open(IMG_PATH.joinpath('ig.png'), 'rb').read())
encoded_yt_image = base64.b64encode(open(IMG_PATH.joinpath('yt.png'), 'rb').read())

layout = html.Div([
                
                    # First Header
                    html.Div([
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
                                                            value='More than 1M'
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
                            dcc.Loading(
                                        id="loading-1",
                                        type="default",
                                        children= dcc.Graph(id="graph9")
                                       )
                        
                        ],className="box"),
                    ],style={
                            'padding-top': '0.5%',
                            'padding-bottom': '0.5%'
                    }, className="row"),



                    # Second Header
                    html.Div([
                        html.Div([
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
                            dcc.Loading(
                                        id="loading-1",
                                        type="default",
                                        children= dcc.Graph(id="graph8")
                                       )

                        ],className="box"),
                    ],style={
                            'padding-bottom': '0.5%'
                    }, className="row"),




                    # Third header
                    html.Div([
                        html.Div([
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
                            dcc.Loading(
                                        id="loading-1",
                                        type="default",
                                        children= dcc.Graph(id="graph6")
                                       )
                        ],className="box"),
                    ],style={
                            'padding-bottom': '0.5%'
                    }, className="row"),




                    # Forth Header
                    html.Div([
                        html.Div([
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

                            html.Div([

                                html.Div([
                                            dcc.Dropdown(
                                                            id='account_filter',
                                                            options=[{"value": x, "label": x}
                                                                    for x in df_view_vs_fan['account_display_name'].drop_duplicates()],
                                                            placeholder="Please select account name to focus"
                                                        )

                                        ], className="five columns")

                            ], style=dict(display='flex')),
                    
                            # Scatter graph
                            dcc.Loading(
                                        id="loading-1",
                                        type="default",
                                        children= dcc.Graph(id="graph7")
                                       )

                        ],className="box"),
                    ],style={
                            'padding-bottom': '0.5%'
                    }, className="row"),



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
    Input("account_filter", "value")
    ])
def change_filter(page1_drop, page2_drop, categ_drop , fan_amount_drop, account_drop):

    # Sunburst chart
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


    # Animated Scatter plot
    filter_account = df_view_vs_fan['account_display_name'] == account_drop

    # Set annotation_text only for filtered account
    df_view_vs_fan['annotation_text'] = ''
    df_view_vs_fan.loc[filter_account, 'annotation_text'] = account_drop

    df_focus = df_view_vs_fan.copy()

    # Set type_fan = 'Filtered by dropdown' only for filtered account
    df_focus.loc[filter_account, 'type_fan'] = 'Filtered by dropdown'

    df_focus = df_focus.sort_values(by=['type_fan', 'account_display_name', 'month'])

    fig_scatter = px.scatter(df_focus, x="fan", y="avg_view", color="type_fan",
                animation_frame="month", animation_group="account_display_name", size="count", size_max=80,
                range_x=[int(df_focus['fan'].max() * -0.0714),int(df_focus['fan'].max() * 1.25)], range_y=[int(df_focus['avg_view'].max()* -0.15),int(df_focus['avg_view'].max() * 1.25)],
                hover_data=['account_display_name'], 
                text='annotation_text',
                color_discrete_map={
                "Diamond": "#483D8B",
                "Gold": "#DAA520",
                "Silver": "#A9A9A9",
                "Filtered by dropdown":"#CD5C5C"},
                labels={"type_fan": "Group of creator", "fan": "Subscriber", "avg_view": "Average view"}
                )

    fig_scatter.update_traces(textposition='top center')
    fig_scatter.update_layout(title_text = 'Size of bubble denotes frequency of video upload', title_x =0.88)

    # Update graph every frame of animation
    for button in fig_scatter.layout.updatemenus[0].buttons:
        button['args'][1]['frame']['redraw'] = True


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

