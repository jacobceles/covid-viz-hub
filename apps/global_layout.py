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
deaths_global_df = read_from_sql('deaths_global')
available_countries = deaths_global_df['country'].unique()
latest_time_period = deaths_global_df['time_period'].max()
latest_year = latest_time_period.split("-")[0]
latest_month = calendar.month_name[int(latest_time_period.split("-")[1])]
deaths_global_latest_df = deaths_global_df[deaths_global_df['time_period'] == latest_time_period]\
    .groupby('continent', as_index=False).sum()

""" Create graphs """
deaths_pie = px.pie(deaths_global_latest_df, values='deaths', names='continent',
                    labels={'continent': 'Continent', 'deaths': 'Death Count'})
deaths_line = px.line(deaths_global_df.groupby(['continent', 'time_period'], as_index=False).sum(),
                      x="time_period", y="deaths", color="continent", markers=True,
                      labels={'time_period': 'Month', 'deaths': 'Death Count', 'continent': 'Continent'})
deaths_choropleth = px.choropleth(deaths_global_df,
                                  locations="iso_alpha_3",
                                  color="deaths",
                                  hover_name="country",
                                  animation_frame="time_period",
                                  color_continuous_scale='agsunset',
                                  labels={'time_period': 'Month', 'deaths': 'Death Count', 'iso_alpha_3': 'ISO Code'},
                                  height=600)

cumulative_deaths_pie = px.pie(deaths_global_latest_df, values='cumulative_deaths', names='continent',
                               labels={'continent': 'Continent', 'cumulative_deaths': 'Cumulative Death Count'})
cumulative_deaths_line = px.line(deaths_global_df.groupby(['continent', 'time_period'], as_index=False).sum(),
                                 x="time_period", y="cumulative_deaths", color="continent", markers=True,
                                 labels={'time_period': 'Month', 'cumulative_deaths': 'Cumulative Death Count',
                                         'continent': 'Continent'})
cumulative_deaths_choropleth = px.choropleth(deaths_global_df,
                                             locations="iso_alpha_3",
                                             color="cumulative_deaths",
                                             hover_name="country",
                                             animation_frame="time_period",
                                             color_continuous_scale='amp',
                                             labels={'time_period': 'Month', 'iso_alpha_3': 'ISO Code',
                                                     'cumulative_deaths': 'Cumulative Death Count'},
                                             height=600)

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
        dash_table.DataTable(id='datatable_global', style_table={'overflowX': 'scroll', 'padding': 10},
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
@app.callback([Output('datatable_global', 'data'),
               Output('datatable_global', 'columns')],
              [Input('table_type', 'value')])
def update_columns(value):
    df = deaths_global_df.tail(1)

    condensed_col = ['continent', 'country', 'iso_alpha_2', 'time_period', 'deaths', 'cumulative_deaths']
    full_col = ['index', 'iso_alpha_2', 'iso_alpha_3', 'country', 'continent',
                'time_period', 'deaths', 'cumulative_deaths']

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
    dfc = dfc[dfc['country'].isin(countries_name)]

    deaths_line_country = px.line(dfc, x="time_period", y="deaths", color="country", markers=True,
                                  labels={'time_period': 'Month', 'deaths': 'Death Count',
                                          'country': 'Country'})
    cumulative_deaths_line_country = px.line(dfc, x="time_period", y="cumulative_deaths", color="country", markers=True,
                                             labels={'time_period': 'Month',
                                                     'cumulative_deaths': 'Cumulative Death Count',
                                                     'country': 'Country'})

    return deaths_line_country, cumulative_deaths_line_country
