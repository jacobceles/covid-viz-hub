import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import dash
import dash_bootstrap_components as dbc

from dash import dcc, html
from app import app, server
from dash.dependencies import Input, Output, State
from apps import home_layout, architecture_layout, global_layout, us_layout, individual_layout


# Building the navigation bar
dropdown = dbc.DropdownMenu(children=[dbc.DropdownMenuItem("Architecture", href="/architecture"),
                                      dbc.DropdownMenuItem("Global", href="/global"),
                                      dbc.DropdownMenuItem("US", href="/us"),
                                      dbc.DropdownMenuItem("Individual", href="/individual"), ],
                            nav=True, in_navbar=True, label="Explore", )

navbar = dbc.Navbar(
    dbc.Container([
        html.A(dbc.Row([dbc.Col(html.Img(src="assets/logo.png", height="30px")),
                        dbc.Col(dbc.NavbarBrand("COVID VIZ-HUB", className="ml-2")), ],
                       align="center", className="g-0", ), href="/home", ),
        dbc.NavbarToggler(id="navbar-toggle2"),
        dbc.Collapse(dbc.Nav([dropdown], className="ms-auto", navbar=True), id="navbar-collapse2", navbar=True, ),
    ]), color="dark", dark=True, className="mb-4", )

for i in [2]:
    app.callback(Output(f"navbar-collapse{i}", "is_open"), [Input(f"navbar-toggle{i}", "n_clicks")],
                 [State(f"navbar-collapse{i}", "is_open")],)(lambda n, is_open: not is_open if n else is_open)


# Adding navigation to main page
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')
])


# Setting up navigation
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/architecture':
        return architecture_layout.layout
    elif pathname == '/global':
        return global_layout.layout
    elif pathname == '/us':
        return us_layout.layout
    elif pathname == '/individual':
        return individual_layout.layout
    else:
        return home_layout.layout


if __name__ == '__main__':
    app.run_server(debug=True)
