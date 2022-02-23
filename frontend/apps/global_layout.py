import plotly.express as px

from dash import dcc
from dash import html
from backend.functions import read_from_sql


""" Import data """
# Read data from SQL
deaths_global_df = read_from_sql('test', 'deaths_global')


""" Create graphs """
fig1 = px.choropleth(deaths_global_df,
                     locations="iso_alpha",
                     color="deaths",
                     hover_name="country/region",
                     animation_frame="time_period",
                     color_continuous_scale='agsunset',
                     title='Death Count',
                     height=600)

fig2 = px.choropleth(deaths_global_df,
                     locations="iso_alpha",
                     color="cumulative_deaths",
                     hover_name="country/region",
                     animation_frame="time_period",
                     color_continuous_scale='amp',
                     title='Cumulative Death Count',
                     height=600)


"""" Layout"""
layout = html.Div([
    dcc.Graph(figure=fig1),
    dcc.Graph(figure=fig2)
])
