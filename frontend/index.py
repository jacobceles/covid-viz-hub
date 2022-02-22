import dash
from dash import dcc
from dash import html

from app import app
from layouts import global_layout, us_layout, individual_layout

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/global':
        return global_layout
    elif pathname == '/apps/us':
        return us_layout
    elif pathname == '/apps/individual':
        return individual_layout
    else:
        return global_layout


if __name__ == '__main__':
    app.run_server(debug=True)
