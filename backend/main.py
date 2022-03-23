from functions import *


def death_globals(df):
    # Deaths Global - deaths_global_df
    df = convert_columns_to_lowercase(df)
    df = replace_character_in_column_names(df, "/", "_")
    df = delete_columns(df, ['province_state', 'lat', 'long'])
    df = rename_date_columns(df, {'country_region'}, '_')
    df = convert_to_month_wise_df(df, {'country_region'}, '/')
    df = melt_columns_to_rows(df, ['country_region'], "time_period", "cumulative_deaths")
    df = df.groupby(['country_region', 'time_period'], as_index=False).sum()
    df = unroll_cumulative_sum(df, ['country_region', 'cumulative_deaths'], ['country_region'])
    df.columns = ['country', 'time_period', 'cumulative_deaths', 'deaths']
    df = remove_unfit_countries(df, ['Kosovo', 'Diamond Princess', 'MS Zaandam', 'Estonia',
                                     'Kyrgyzstan', 'Monaco', 'Sao Tome and Principe', 'Venezuela'])
    countries_mapper = {'Congo (Kinshasa)': 'Congo', 'West Bank and Gaza': 'Israel', 'Congo (Brazzaville)': 'Congo',
                        'Holy See': 'Holy See (Vatican City State)', 'Korea, South': 'Korea, Republic of',
                        'Summer Olympics 2020': 'Japan', 'Burma': 'Myanmar', 'US': 'United States',
                        'Winter Olympics 2022': 'China', 'Taiwan*': 'Taiwan, Province of China',
                        "Cote d'Ivoire": "Côte d'Ivoire", 'Moldova': 'Moldova, Republic of',
                        'Syria': 'Syrian Arab Republic', 'Venezuela': 'Venezuela, Bolivarian Republic of',
                        'Iran': 'Iran, Islamic Republic of', 'Russia': 'Russian Federation',
                        'Micronesia': 'Micronesia, Federated States of', 'Bolivia': 'Bolivia, Plurinational State of',
                        'Laos': "Lao People's Democratic Republic", 'Brunei': 'Brunei Darussalam',
                        'Vietnam': 'Viet Nam', 'Tanzania': 'Tanzania, United Republic of'}
    df = clean_country_names(df, countries_mapper)
    df = get_country_iso_code_2(df)
    df = get_country_iso_code_3(df)
    df = get_country_continent(df)
    df['deaths'].clip(lower=0, inplace=True)
    df.reset_index(level=0, inplace=True, drop=True)
    return df


def deaths_us(df):
    # Deaths US - deaths_us_df, death_us_states_normalized
    df = convert_columns_to_lowercase(df)
    df = replace_character_in_column_names(df, "/", "_")
    df = delete_columns(df, ['uid', 'iso2', 'iso3', 'code3', 'fips', 'country_region', 'lat', 'long_', 'combined_key'])
    df = rename_date_columns(df, {'admin2', 'province_state', 'population'}, '_')
    df = convert_to_month_wise_df(df, {'admin2', 'province_state', 'population'}, '/')
    df = melt_columns_to_rows(df, ['admin2', 'province_state', 'population'], "time_period", "cumulative_deaths")
    df = unroll_cumulative_sum(df, ['admin2', 'province_state', 'cumulative_deaths'], ['admin2', 'province_state'])
    not_ok_states = ['American Samoa', 'Diamond Princess', 'Grand Princess', 'Guam', 'Puerto Rico',
                     'Northern Mariana Islands', 'Virgin Islands', 'District of Columbia']
    df = remove_unfit_states(df, not_ok_states)
    df = remove_unfit_provinces(df, None)
    states_mapper = {'Alaska': 'AK', 'Alabama': 'AL', 'Arkansas': 'AR', 'Arizona': 'AZ', 'California': 'CA',
                     'Colorado': 'CO', 'Connecticut': 'CT', 'District of Columbia': 'DC', 'Delaware': 'DE',
                     'Florida': 'FL', 'Georgia': 'GA', 'Hawaii': 'HI', 'Iowa': 'IA', 'Idaho': 'ID', 'Illinois': 'IL',
                     'Indiana': 'IN', 'Kansas': 'KS', 'Kentucky': 'KY', 'Louisiana': 'LA', 'Massachusetts': 'MA',
                     'Maryland': 'MD', 'Maine': 'ME', 'Michigan': 'MI', 'Minnesota': 'MN', 'Missouri': 'MO',
                     'Mississippi': 'MS', 'Montana': 'MT', 'North Carolina': 'NC', 'North Dakota': 'ND',
                     'Nebraska': 'NE', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM', 'Nevada': 'NV',
                     'New York': 'NY', 'Ohio': 'OH', 'Oklahoma': 'OK', 'Oregon': 'OR', 'Pennsylvania': 'PA',
                     'Rhode Island': 'RI', 'South Carolina': 'SC', 'South Dakota': 'SD', 'Tennessee': 'TN',
                     'Texas': 'TX', 'Utah': 'UT', 'Virginia': 'VA', 'Vermont': 'VT', 'Washington': 'WA',
                     'Wisconsin': 'WI', 'West Virginia': 'WV', 'Wyoming': 'WY'}
    df = clean_state_names(df, states_mapper)
    df.columns = ['province', 'state', 'population', 'time_period', 'cumulative_deaths', 'deaths', 'state_code']
    df['deaths'].clip(lower=0, inplace=True)
    df.reset_index(level=0, inplace=True, drop=True)
    return df


def deaths_us_normalized(df):
    # Create new normalized dataframe for states
    death_us_states = df[['state', 'cumulative_deaths']].groupby('state', as_index=False).sum()
    population_us_states = df[['state', 'population']].groupby('state', as_index=False).sum()

    death_us_states.set_index(['state'], inplace=True)
    population_us_states.set_index(['state'], inplace=True)
    normalized_df = death_us_states.join(population_us_states).reset_index()
    death_us_states.reset_index(level=0, inplace=True, drop=True)
    population_us_states.reset_index(level=0, inplace=True, drop=True)

    normalized_df['death_percent'] = normalized_df['cumulative_deaths'] / normalized_df['population']
    return normalized_df


if __name__ == '__main__':
    # JHU data
    deaths_global_df = death_globals(pd.read_csv("data/deaths_global.csv"))
    deaths_us_df = deaths_us(pd.read_csv("data/deaths_us.csv"))
    deaths_us_df_latest = deaths_us_df[deaths_us_df['time_period'] == deaths_us_df['time_period'].max()]
    deaths_us_states_normalized = deaths_us_normalized(deaths_us_df_latest)

    # CDC data
    missing_values = ["NaN", "Missing", "Unknown", "NA", "nul", "null"]
    fields = ['age_group', 'sex', 'race', 'underlying_conditions_yn',
              'res_state', 'death_yn', 'hosp_yn', 'icu_yn', 'case_month']
    cdc_df = pd.read_csv('data/cdc_out.csv', skipinitialspace=True, usecols=fields,
                         na_values=missing_values, low_memory=False).dropna()

    # Write to SQL
    print(write_to_sql(deaths_us_df, 'covid_viz_hub', 'deaths_us'))
    print(write_to_sql(deaths_global_df, 'covid_viz_hub', 'deaths_global'))
    print(write_to_sql(deaths_us_states_normalized, 'covid_viz_hub', 'deaths_us_normalized'))
    print(write_to_sql(cdc_df, 'covid_viz_hub', 'cdc_out'))
