from dash import html
from dash import dcc
import dash_bootstrap_components as dbc

layout = html.Div([
    dbc.Container([
        dbc.Row([
            dbc.Col(html.H1("Welcome to the COVID-19 dashboard!", className="text-center"), className="mb-5 mt-5")
        ]),
        dbc.Row([
            dbc.Col(html.H5(children='We help you take better, informed decisions.', style={'font-style': 'italic'}),
                    className="mb-4 text-center")
        ]),
        dbc.Row([
            dbc.Col(dcc.Markdown(
                children='''
                \nAccording to WHO, as of December 2020, COVID-19 had infected over 82M people and killed 
                more than 3M worldwide. 
                \nMillions of people are at risk of falling into extreme poverty, while the number of undernourished 
                people are over 690 million.
                \nWe need ways to help people assess the risks, understand what is happening around them - helping them 
                take better, informed decisions.
                \nDashboards are an iconic interface to understand the coronavirus pandemic. These visual displays 
                gives us the information needed to act wisely.''',
                style={'text-align': 'center', 'text-justify': 'inter-word', 'list-style-position': 'inside'}),
                className="mb-5 text-center")
        ]),
        dbc.Row([
            dbc.Col(dbc.Card(children=[html.H3(children='Get the original datasets used in this dashboard',
                                               className="text-center"),
                                       dbc.Row([dbc.Col(dbc.Button("CDC Data",
                                                                   href="https://data.cdc.gov/Case-Surveillance/"
                                                                        "COVID-19-Case-Surveillance-Public-Use-Data-"
                                                                        "with-Ge/n8mc-b4w4",
                                                                   target="_blank",
                                                                   color="primary", className="mt-3"),
                                                        className="mx-auto"),
                                                dbc.Col(dbc.Button("JHU Data",
                                                                   href="https://github.com/CSSEGISandData/COVID-19/"
                                                                        "tree/master/csse_covid_19_data/"
                                                                        "csse_covid_19_time_series",
                                                                   target="_blank",
                                                                   color="primary", className="mt-3"),
                                                        className="mx-auto")],
                                               justify="center")],
                             body=True, color="dark", outline=True), width=4, className="mb-4 text-center"),

            dbc.Col(dbc.Card(children=[html.H3(children='Access the code used to build this dashboard',
                                               className="text-center"),
                                       dbc.Button("GitHub", href="https://github.com/jacobceles/covid-viz-hub",
                                                  target="_blank", color="primary", className="mt-3"), ],
                             body=True, color="dark", outline=True), width=4, className="mb-4 text-center"),
            dbc.Col(dbc.Card(children=[html.H3(children='Start exploring the Covid Viz-Hub dashboard',
                                               className="text-center"),
                                       dbc.Button("Let's Go!", href="/global", color="primary", className="mt-3"), ],
                             body=True, color="dark", outline=True), width=4, className="mb-4 text-center")
        ], className="mb-5"),
    ])
])
