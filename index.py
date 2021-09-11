import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

# Connect to main app.py file
from app import app

# Connect to your app pages
from layouts import page1


app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div([
        dcc.Link('Page1 |', href='/page1'),
        dcc.Link(' Page2', href='/page2'),
    ], className="row"),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page1':
        return page1.layout
    if pathname == '/page2':
        return page1.layout
    else:
        return "404 Page Error!"


if __name__ == '__main__':
    app.run_server(debug=False)