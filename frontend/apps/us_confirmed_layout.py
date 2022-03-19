from backend.functions import read_from_sql
import plotly.express as px
import dash_bootstrap_components as dbc
from dash import dcc
from dash import html
from dash import dash_table
from dash.dependencies import Input, Output

#JupyterDash.infer_jupyter_proxy_config()

""" Import data """
# Read data from SQL
confirmed_us_states_normalized = read_from_sql('test', 'confirmed_us_normalized')
confirmed_us_states = read_from_sql('test', 'confirmed_us')


""" Create graphs """
confirmed_choropleth = px.choropleth(confirmed_us_states,
                                  locations='state_code',
                                  color="confirmed",
                                  animation_frame="time_period",
                                  color_continuous_scale="orrd",
                                  locationmode='USA-states',
                                  hover_name="province_state",
                                  scope="usa",
                                  range_color=(0, 1000000),
                                  labels={'province_state': 'State', 'confirmed': 'confirmed Count', 'time_period': 'Month'},
                                  height=600)
confirmed_choropleth.show()
confirmed_us_bar = px.bar(confirmed_us_states_normalized, x="confirmed_percent", y="province_state", orientation='h',
                        labels={'province_state': 'State', 'confirm_percent': 'Percentage of confirm'})

states = ['Connecticut', 'Louisiana', 'Massachusetts', 'Mississippi', 'New York', 'New Jersey', 'Rhode Island']
confirmed_us_sunburst = px.sunburst(confirmed_us_states[confirmed_us_states['province_state'].isin(states)],
                                 path=['province_state', 'confirmed'], values='confirmed', height=600, template="plotly",
                                 labels={'province_state': 'State', 'admin2': 'Provinces', 'confirmed': 'Confirm Count'})


"""" Layout"""
#app = JupyterDash(__name__)
app.layout = html.Div([
    dbc.Container([
        dbc.Row([dbc.Col(html.H1(children='Covid-19 in the USA at a glance'), className="mb-2")]),
        dbc.Row([dbc.Col(html.H6(children='visualising trends across the different stages of '
                                          'the covid-19 outbreak in the USA'), className="mb-4")]),

        dbc.Row([dbc.Col(dbc.Card(html.H3(children='Latest Update', className="text-center text-light bg-dark"),
                                  body=True, color="dark"),
                         className="mb-4")]),
        dcc.RadioItems(id='table_type', options=[{'label': i, 'value': i} for i in ['Condensed table', 'Full table']],
                       value='Condensed table', labelStyle={'display': 'inline-block', "margin-right": "20px"},
                       style={"text-align": "center"}),
        dash_table.DataTable(id='datatable_us', style_table={'overflowX': 'scroll', 'padding': 10},
                             style_header={'backgroundColor': '#25597f', 'color': 'white'},
                             style_cell={'backgroundColor': 'white', 'color': 'black', 'fontSize': 13,
                                         'font-family': 'Nunito Sans', "text-align": "center"}),

        dbc.Row([dbc.Col(dbc.Card(html.H3(children='Situation across different periods of the outbreak',
                                          className="text-center text-light bg-dark"),
                                  body=True, color="dark"),
                         className="mt-4 mb-4")]),

        dbc.Row([dbc.Col(dbc.Card(html.H3(children='Figures by states', className="text-center text-light bg-dark"),
                                  body=True, color="dark"),
                         className="mb-4")]),
        dbc.Row([dbc.Col(html.H5(children='Progress of covid confirmed cases across states in the USA', className="text-center"),
                         className="mt-4"), ]),
        dbc.Row([html.Div([dcc.Graph(figure=confirmed_choropleth)])]),
        dbc.Row([html.Div([dcc.Graph(figure=confirmed_us_bar)])]),
        dbc.Row([html.Div([dcc.Graph(figure=confirmed_us_sunburst)])]),
    ])
])

# choose between condensed table and full table
@app.callback([Output('datatable_us', 'data'),
               Output('datatable_us', 'columns')],
              [Input('table_type', 'value')])
def update_columns(value):
    df = confirmed_us_states.tail(1)

    condensed_col = ['combined_key', 'population', 'time_period', 'confirmed', 'cumulative_confirmed']
    full_col = ['index', 'lat', 'iso2', 'uid', 'province_state', 'fips', 'combined_key', 'admin2', 'country_region',
                'code3', 'population', 'iso3', 'long_', 'time_period', 'confirmed', 'cumulative_confirmed', 'state_code']

    columns = [{"name": i, "id": i} for i in full_col]
    data = df.to_dict('records')
    if value == 'Condensed table':
        columns = [{"name": i, "id": i} for i in condensed_col]
        data = df.to_dict('records')

    return data, columns

app.run_server(mode='inline')