from functions import *

# Read input
deaths_us_df = pd.read_csv("data/deaths_us.csv")
deaths_us_df.columns = map(str.lower, deaths_us_df.columns)
confirmed_us_df = pd.read_csv("data/confirmed_us.csv")
confirmed_us_df.columns = map(str.lower, confirmed_us_df.columns)
deaths_global_df = pd.read_csv("data/deaths_global.csv")
deaths_global_df.columns = map(str.lower, deaths_global_df.columns)

# Deaths Global - deaths_global_df
deaths_global_df = rename_date_columns(deaths_global_df, {'province/state', 'country/region', 'lat', 'long'})
deaths_global_df = pivot_date_columns(deaths_global_df, ['country/region', 'province/state', 'lat', 'long'], 'deaths')
deaths_global_df = get_cumulative_deaths(deaths_global_df, ['country/region'])
deaths_global_df = remove_unfit_countries(deaths_global_df, ['Kosovo', 'Diamond Princess', 'MS Zaandam'])
countries_mapper = {
    'Congo (Kinshasa)': 'Congo',
    'West Bank and Gaza': 'Israel',
    'Congo (Brazzaville)': 'Congo',
    'Holy See': 'Holy See (Vatican City State)',
    'Korea, South': 'Korea, Republic of',
    'Summer Olympics 2020': 'Japan',
    'Burma': 'Myanmar',
    'US': 'United States',
    'Winter Olympics 2022': 'China',
    'Taiwan*': 'Taiwan, Province of China',
    "Cote d'Ivoire": "Côte d'Ivoire",
    'Moldova': 'Moldova, Republic of',
    'Syria': 'Syrian Arab Republic',
    'Venezuela': 'Venezuela, Bolivarian Republic of',
    'Iran': 'Iran, Islamic Republic of',
    'Russia': 'Russian Federation',
    'Micronesia': 'Micronesia, Federated States of',
    'Bolivia': 'Bolivia, Plurinational State of',
    'Laos': "Lao People's Democratic Republic",
    'Brunei': 'Brunei Darussalam',
    'Vietnam': 'Viet Nam',
    'Tanzania': 'Tanzania, United Republic of'
}
deaths_global_df = clean_country_names(deaths_global_df, countries_mapper)
deaths_global_df = get_country_iso_code(deaths_global_df)

# Deaths US - deaths_us_df, death_us_states_normalized
ok_columns_set = {'uid', 'iso2', 'iso3', 'code3', 'fips', 'admin2', 'province_state',
                  'country_region', 'lat', 'long_', 'combined_key', 'population'}
ok_columns_list = list(ok_columns_set)
deaths_us_df = rename_date_columns(deaths_us_df, ok_columns_set)
deaths_us_df = pivot_date_columns(deaths_us_df, ok_columns_list, 'deaths')
deaths_us_df = get_cumulative_deaths(deaths_us_df, ['province_state'])
not_ok_states = ['American Samoa', 'Diamond Princess', 'Grand Princess', 'Guam', 'Puerto Rico',
                 'Northern Mariana Islands', 'Virgin Islands', 'District of Columbia']
deaths_us_df = remove_unfit_states(deaths_us_df, not_ok_states)
deaths_us_df = remove_unfit_provinces(deaths_us_df, None)
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
deaths_us_df = clean_state_names(deaths_us_df, states_mapper)
# Create new dataframes from deaths_us_df
death_us_states = deaths_us_df.groupby('province_state', as_index=False)['deaths'].sum()
population_us_states = deaths_us_df[deaths_us_df['time_period'] == deaths_us_df['time_period'].max()] \
    [['province_state', 'population']].groupby('province_state', as_index=False).sum()
death_us_states.set_index(['province_state'], inplace=True)
population_us_states.set_index(['province_state'], inplace=True)
deaths_us_states_normalized = death_us_states.join(population_us_states).reset_index()
death_us_states.reset_index(level=0, inplace=True)
population_us_states.reset_index(level=0, inplace=True)
deaths_us_states_normalized['death_percent'] = \
        deaths_us_states_normalized['deaths'] / deaths_us_states_normalized['population']

# Write to SQL
print(deaths_us_df.shape)
print(write_to_sql(deaths_us_df, 'test', 'deaths_us'))
print(write_to_sql(deaths_us_states_normalized, 'test', 'deaths_us_normalized'))
