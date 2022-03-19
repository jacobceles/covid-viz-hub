from functions import *

import pandas as pd
import numpy as np

# Read input
confirmed_us_df = pd.read_csv("data/confirmed_us.csv")
confirmed_us_df.columns = map(str.lower, confirmed_us_df.columns)

deaths_us_df = pd.read_csv("data/deaths_us.csv")
deaths_us_df.columns = map(str.lower, deaths_us_df.columns)
population_us_df=deaths_us_df.filter(['population','province_state','country_region', 'lat', 'long_','admin2','uid'], axis=1)

confirmed_us_df = pd.merge(confirmed_us_df, population_us_df,
                   on=['province_state', 'country_region', 'lat', 'long_','admin2','uid'],
                   how='inner')


ok_columns_set = {'uid', 'iso2', 'iso3', 'code3', 'fips', 'admin2', 'province_state',
                  'country_region', 'lat', 'long_', 'combined_key','population'}
ok_columns_list = list(ok_columns_set)
confirmed_us_df = rename_date_columns(confirmed_us_df, ok_columns_set)
confirmed_us_df = pivot_date_columns(confirmed_us_df, ok_columns_list, 'confirmed')
confirmed_us_df = get_cumulative_confirmed(confirmed_us_df, ['province_state', 'admin2'])
confirmed_us_df['cumulative_confirmed'] = confirmed_us_df.groupby(['province_state', 'admin2']).agg({'confirmed':'cumsum'})
confirmed_us_df = remove_unfit_states(confirmed_us_df, not_ok_states)
confirmed_us_df = remove_unfit_provinces(confirmed_us_df, None)
states_mapper = {
    'Alaska': 'AK',
    'Alabama': 'AL',
    'Arkansas': 'AR',
    'Arizona': 'AZ',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'District of Columbia': 'DC',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Iowa': 'IA',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Massachusetts': 'MA',
    'Maryland': 'MD',
    'Maine': 'ME',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Missouri': 'MO',
    'Mississippi': 'MS',
    'Montana': 'MT',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Nebraska': 'NE',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'Nevada': 'NV',
    'New York': 'NY',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Virginia': 'VA',
    'Vermont': 'VT',
    'Washington': 'WA',
    'Wisconsin': 'WI',
    'West Virginia': 'WV',
    'Wyoming': 'WY'
}
confirmed_us_df = clean_state_names(confirmed_us_df, states_mapper)
confirmed_us_states = confirmed_us_df.groupby('province_state', as_index=False)['confirmed'].max()
#print(confirmed_us_states)
population_us_states = confirmed_us_df[confirmed_us_df['time_period'] == confirmed_us_df['time_period'].max()] \
                         [['province_state', 'population']].groupby('province_state', as_index=False).sum()
print(population_us_states)
confirmed_us_states.set_index(['province_state'], inplace=True)
population_us_states.set_index(['province_state'], inplace=True)
confirmed_us_states_normalized = confirmed_us_states.join(population_us_states).reset_index()
confirmed_us_states.reset_index(level=0, inplace=True)
population_us_states.reset_index(level=0, inplace=True)
confirmed_us_states_normalized['confirmed_percent'] = \
         confirmed_us_states_normalized['confirmed'] / confirmed_us_states_normalized['population']
# Write to SQL
print(write_to_sql(confirmed_us_df, 'test', 'confirmed_us'))
print(write_to_sql(confirmed_us_states_normalized, 'test', 'confirmed_us_normalized'))
