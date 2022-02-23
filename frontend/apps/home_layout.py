import plotly.express as px

from dash import dcc
from dash import html
from backend.functions import read_from_sql


""" Import data """
# Read data from SQL
deaths_us_normalized_df = read_from_sql('test', 'deaths_us_normalized')
deaths_global_df = read_from_sql('test', 'deaths_global')
deaths_us_df = read_from_sql('test', 'deaths_us')


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

fig3 = px.choropleth(deaths_us_df,
                     locations='state_code',
                     color="deaths",
                     animation_frame="time_period",
                     color_continuous_scale="orrd",
                     locationmode='USA-states',
                     hover_name="province_state",
                     scope="usa",
                     range_color=(0, 20),
                     title='Deaths in US by State',
                     height=600)

fig4 = px.bar(deaths_us_normalized_df, x="death_percent", y="province_state", orientation='h')

states = ['Connecticut', 'Louisiana', 'Massachusetts', 'Mississippi', 'New York', 'New Jersey', 'Rhode Island']
fig5 = px.sunburst(deaths_us_df[deaths_us_df['province_state'].isin(states)],
                   path=['province_state', 'admin2'], values='deaths', height=600, template="plotly")


"""" Layout"""
layout = html.Div([
    dcc.Graph(figure=fig1),
    dcc.Graph(figure=fig2),
    dcc.Graph(figure=fig3),
    dcc.Graph(figure=fig4),
    dcc.Graph(figure=fig5)
])