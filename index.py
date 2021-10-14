import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app
from app import server

# Connect to your app pages
from layouts import page1
from layouts import page2

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link(' Page1 ',id='page1', href='/page1'),
        dcc.Link(' Page2 ',id='page2', href='/page2'),
    ], className="topnav"),
    dcc.Loading(type="default",fullscreen=True, style={'backgroundColor': 'transparent'},children=html.Div(id='page-content'))
])


@app.callback([Output('page-content', 'children'),Output('page1', 'className'),Output('page2', 'className')],
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page1':
        return page1.layout,"active","" 
    if pathname == '/page2':
        return page2.layout,"","active"
    else:
        return page1.layout,"active",""


if __name__ == '__main__':
    app.run_server(debug=True)
