import calendar
import plotly.express as px
import dash_bootstrap_components as dbc

from app import app
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output
from backend.functions import read_from_sql

""" Import data """
# Read data from SQL
deaths_global_df = read_from_sql('test', 'deaths_global')
available_countries = deaths_global_df['country/region'].unique()
latest_time_period = deaths_global_df['time_period'].max()
latest_year = latest_time_period.split("-")[0]
latest_month = calendar.month_name[int(latest_time_period.split("-")[1])]
deaths_global_df_latest = deaths_global_df[deaths_global_df['time_period'] == latest_time_period]\
    .groupby('continent', as_index=False).sum()

""" Create graphs """
deaths_pie = px.pie(deaths_global_df_latest, values='deaths', names='continent')
deaths_line = px.line(deaths_global_df, x="time_period", y="deaths", color="continent",
                      labels={'time_period': 'Month', 'deaths': 'Death Count', 'continent': 'Continents'})
deaths_choropleth = px.choropleth(deaths_global_df,
                                  locations="iso_alpha_3",
                                  color="deaths",
                                  hover_name="country/region",
                                  animation_frame="time_period",
                                  color_continuous_scale='agsunset',
                                  labels={'time_period': 'Month', 'deaths': 'Death Count'},
                                  height=600)

cumulative_deaths_pie = px.pie(deaths_global_df_latest, values='cumulative_deaths', names='continent')
cumulative_deaths_line = px.line(deaths_global_df, x="time_period", y="cumulative_deaths", color="continent",
                                 labels={'time_period': 'Month', 'deaths': 'Cumulative Death Count',
                                         'continent': 'Continents'})
cumulative_deaths_choropleth = px.choropleth(deaths_global_df,
                                             locations="iso_alpha_3",
                                             color="cumulative_deaths",
                                             hover_name="country/region",
                                             animation_frame="time_period",
                                             color_continuous_scale='amp',
                                             labels={'time_period': 'Month',
                                                     'cumulative_deaths': 'Cumulative Death Count'},
                                             height=600)

# change to app.layout if running as single page app instead
layout = html.Div([
    dbc.Container([
        dbc.Row([dbc.Col(html.H1(children='COVID-19 Worldwide at a glance'), className="mb-2")]),
        dbc.Row([dbc.Col(html.H6(children='Visualising trends across the world'), className="mb-4")]),

        dbc.Row([dbc.Col(dbc.Card(html.H3(children='Latest Update', className="text-center text-light bg-dark"),
                                  body=True, color="dark"),
                         className="mb-4")]),
        dcc.RadioItems(id='table_type', options=[{'label': i, 'value': i} for i in ['Condensed table', 'Full table']],
                       value='Condensed table', labelStyle={'display': 'inline-block', "margin-right": "20px"},
                       style={"text-align": "center"}),
        dash_table.DataTable(id='datatable', style_table={'overflowX': 'scroll', 'padding': 10},
                             style_header={'backgroundColor': '#25597f', 'color': 'white'},
                             style_cell={'backgroundColor': 'white', 'color': 'black', 'fontSize': 13,
                                         'font-family': 'Nunito Sans', "text-align": "center"}),

        dbc.Row([dbc.Col(dbc.Card(html.H3(children='Figures by Continent',
                                          className="text-center text-light bg-dark"),
                                  body=True, color="dark"),
                         className="mt-4 mb-4")]),
        dbc.Row([dbc.Col(html.H5(children='Latest updated: {} {}'.format(latest_month, latest_year),
                                 className="text-center"), width=4, className="mt-4"),
                 dbc.Col(html.H5(children='Monthly figures since 1 Jan 2020', className="text-center"),
                         width=8, className="mt-4"), ]),
        dbc.Row([dbc.Col(html.Div([dcc.Graph(figure=deaths_pie)])),
                 dbc.Col(html.Div([dcc.Graph(figure=deaths_line)]))]),
        dbc.Row([html.Div([dcc.Graph(figure=deaths_choropleth)])]),

        dbc.Row([dbc.Col(dbc.Card(html.H3(children='Cumulative Figures by Continent',
                                          className="text-center text-light bg-dark"),
                                  body=True, color="dark"),
                         className="mt-4 mb-4")]),
        dbc.Row([dbc.Col(html.Div([dcc.Graph(figure=cumulative_deaths_pie)])),
                 dbc.Col(html.Div([dcc.Graph(figure=cumulative_deaths_line)]))]),
        dbc.Row([html.Div([dcc.Graph(figure=cumulative_deaths_choropleth)])]),

        dbc.Row([dbc.Col(dbc.Card(html.H3(children='Figures by country', className="text-center text-light bg-dark"),
                                  body=True, color="dark"),
                         className="mb-4")]),
        dcc.Dropdown(id='countries', options=[{'label': i, 'value': i} for i in available_countries],
                     value=['United States', 'India'], multi=True,
                     style={'width': '70%', 'margin-left': '5px', 'align': 'center'}),
        dbc.Row([dbc.Col(html.H5(children='Monthly figures', className="text-center"), className="mt-4"), ]),
        dcc.Graph(id='deaths_country'),
        dbc.Row([dbc.Col(html.H5(children='Cumulative figures', className="text-center"), className="mt-4"), ]),
        dcc.Graph(id='cumulative_deaths_country'),
    ])
])


# choose between condensed table and full table
@app.callback([Output('datatable', 'data'),
               Output('datatable', 'columns')],
              [Input('table_type', 'value')])
def update_columns(value):
    df = deaths_global_df.tail(1)

    condensed_col = ['iso_alpha', 'country/region', 'time_period', 'deaths', 'cumulative_deaths']
    full_col = ['index', 'iso_alpha', 'country/region', 'province/state',
                'lat', 'long', 'time_period', 'deaths', 'cumulative_deaths']

    columns = [{"name": i, "id": i} for i in full_col]
    data = df.to_dict('records')
    if value == 'Condensed table':
        columns = [{"name": i, "id": i} for i in condensed_col]
        data = df.to_dict('records')

    return data, columns


# to allow comparison of cases or deaths among countries
@app.callback([Output('deaths_country', 'figure'),
               Output('cumulative_deaths_country', 'figure')],
              [Input('countries', 'value')])
def update_graph(countries_name):
    dfc = deaths_global_df.copy()
    dfc = dfc[dfc['country/region'].isin(countries_name)]

    deaths_line_country = px.line(dfc, x="time_period", y="deaths", color="country/region",
                                  labels={'time_period': 'Month', 'deaths': 'Death Count',
                                          'country/region': 'Countries'})
    cumulative_deaths_line_country = px.line(dfc, x="time_period", y="cumulative_deaths", color="country/region",
                                             labels={'time_period': 'Month', 'deaths': 'Cumulative Death Count',
                                                     'country/region': 'Countries'})

    return deaths_line_country, cumulative_deaths_line_country
