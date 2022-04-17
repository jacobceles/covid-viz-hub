# import pandas as pd
# from functions import *
# import calendar
#
# confirmed_global_df = pd.read_csv("data/confirmed_global_df.csv")
# confirmed_global_df.columns = map(str.lower, confirmed_global_df.columns)
#
# confirmed_global_df = rename_date_columns(confirmed_global_df, {'province/state', 'country/region', 'lat', 'long','confirmed','time_period'})
# confirmed_global_df = pivot_date_columns(confirmed_global_df, ['country/region', 'province/state', 'lat', 'long'], 'confirmed')
# confirmed_global_df = get_cumulative_cases(confirmed_global_df, ['country/region'])
# confirmed_global_df = remove_unfit_countries(confirmed_global_df, ['Kosovo', 'Diamond Princess', 'MS Zaandam'])
# countries_mapper = {
#     'Congo (Kinshasa)': 'Congo',
#     'West Bank and Gaza': 'Israel',
#     'Congo (Brazzaville)': 'Congo',
#     'Holy See': 'Holy See (Vatican City State)',
#     'Korea, South': 'Korea, Republic of',
#     'Summer Olympics 2020': 'Japan',
#     'Burma': 'Myanmar',
#     'US': 'United States',
#     'Winter Olympics 2022': 'China',
#     'Taiwan*': 'Taiwan, Province of China',
#     "Cote d'Ivoire": "Côte d'Ivoire",
#     'Moldova': 'Moldova, Republic of',
#     'Syria': 'Syrian Arab Republic',
#     'Venezuela': 'Venezuela, Bolivarian Republic of',
#     'Iran': 'Iran, Islamic Republic of',
#     'Russia': 'Russian Federation',
#     'Micronesia': 'Micronesia, Federated States of',
#     'Bolivia': 'Bolivia, Plurinational State of',
#     'Laos': "Lao People's Democratic Republic",
#     'Brunei': 'Brunei Darussalam',
#     'Vietnam': 'Viet Nam',
#     'Tanzania': 'Tanzania, United Republic of'
# }
# confirmed_global_df = clean_country_names(confirmed_global_df, countries_mapper)
# confirmed_global_df = get_country_iso_code_2(confirmed_global_df)
# confirmed_global_df = get_country_iso_code_3(confirmed_global_df)
# confirmed_global_df = get_country_continent(confirmed_global_df)
#
#
#
# #confirmed_global_df = read_from_sql('test', 'confirmed_global')
# available_countries = confirmed_global_df['country/region'].unique()
# latest_time_period = confirmed_global_df['time_period'].max()
# latest_year = latest_time_period.split("-")[0]
# latest_month = calendar.month_name[int(latest_time_period.split("-")[1])]
# confirmed_global_df_latest = confirmed_global_df[confirmed_global_df['time_period'] == latest_time_period]\
#     .groupby('continent', as_index=False).sum()
#
# # Write to SQL
# print(write_to_sql(confirmed_global_df, 'test', 'confirmed_global'))