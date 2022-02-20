import dash
from dash import dcc
from dash import html

from app import app
from layouts import world, us, individual

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/apps/world':
        return world
    elif pathname == '/apps/us':
        return us
    elif pathname == '/apps/individual':
        return individual
    else:
        return world


if __name__ == '__main__':
    app.run_server(debug=True)
