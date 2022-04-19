from functions import *


def recovered_globals(df):
    df = convert_columns_to_lowercase(df)
    df = replace_character_in_column_names(df, "/", "_")
    df = delete_columns(df, ['province_state', 'lat', 'long'])
    df = rename_date_columns(df, {'country_region'}, '_')
    df = convert_to_month_wise_df(df, {'country_region'}, '/')
    df = melt_columns_to_rows(df, ['country_region'], "time_period", "cumulative_recovered")
    df = df.groupby(['country_region', 'time_period'], as_index=False).sum()
    df = unroll_cumulative_sum(df, ['country_region', 'cumulative_recovered'], ['country_region'])
    df.columns = ['country', 'time_period', 'cumulative_recovered', 'recovered']
    df['time_period'] = df['time_period'] <= '2021-08'
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
    df['recovered'].clip(lower=0, inplace=True)
    df.reset_index(level=0, inplace=True, drop=True)
    return df

def confirmed_globals(df):
    df = convert_columns_to_lowercase(df)
    df = replace_character_in_column_names(df, "/", "_")
    df = delete_columns(df, ['province_state', 'lat', 'long'])
    df = rename_date_columns(df, {'country_region'}, '_')
    df = convert_to_month_wise_df(df, {'country_region'}, '/')
    df = melt_columns_to_rows(df, ['country_region'], "time_period", "cumulative_confirmed")
    df = df.groupby(['country_region', 'time_period'], as_index=False).sum()
    df = unroll_cumulative_sum(df, ['country_region', 'cumulative_confirmed'], ['country_region'])
    df.columns = ['country', 'time_period', 'cumulative_confirmed', 'confirmed']
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
    df['confirmed'].clip(lower=0, inplace=True)
    df.reset_index(level=0, inplace=True, drop=True)
    return df


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

def confirmed_us(df):
    df.columns = map(str.lower, df.columns)
    ok_columns_set = {'uid', 'iso2', 'iso3', 'code3', 'fips', 'admin2', 'province_state',
                      'country_region', 'lat', 'long_', 'combined_key', 'population'}
    not_ok_states = ['American Samoa', 'Diamond Princess', 'Grand Princess', 'Guam', 'Puerto Rico',
                     'Northern Mariana Islands', 'Virgin Islands', 'District of Columbia']
    confirmed_us_df = replace_character_in_column_names(df, "/", "_")
    confirmed_us_df = delete_columns(confirmed_us_df,
                                     ['uid', 'iso2', 'iso3', 'code3', 'fips', 'country_region', 'lat', 'long_',
                                      'combined_key'])
    confirmed_us_df = rename_date_columns(confirmed_us_df, ok_columns_set, '_')
    #print(confirmed_us_df.head())
    confirmed_us_df = convert_to_month_wise_df(confirmed_us_df, {'admin2', 'province_state', 'population'}, '/')
    confirmed_us_df = melt_columns_to_rows(confirmed_us_df, ['admin2', 'province_state', 'population'], "time_period",
                                           "cumulative_confirmed")
    confirmed_us_df = unroll_cumulative_sum(confirmed_us_df, ['admin2', 'province_state', 'cumulative_confirmed'],
                                            ['admin2', 'province_state'])

    confirmed_us_df = remove_unfit_states(confirmed_us_df, not_ok_states)
    confirmed_us_df = remove_unfit_provinces(confirmed_us_df, None)
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
    df = clean_state_names(confirmed_us_df, states_mapper)
    confirmed_us_df_latest = df[df['time_period'] == df['time_period'].max()]
    print("hi",confirmed_us_df_latest.columns)
    return confirmed_us_df_latest

def confirmed_us_normalized(df):
    # Create new normalized dataframe for states
    print(df.columns)
    confirmed_us_states = df.groupby('province_state', as_index=False)['cumulative_confirmed'].sum()
    print(confirmed_us_states.head())
    population_us_states=df.groupby('province_state', as_index=False)['population'].sum()
    # population_us_states = confirmed_us_states[confirmed_us_states['time_period'] == confirmed_us_states['time_period'].max()] \
    #     [['province_state', 'population']].groupby('province_state', as_index=False).sum()
    confirmed_us_states.set_index(['province_state'], inplace=True)
    population_us_states.set_index(['province_state'], inplace=True)
    confirmed_us_states_normalized = confirmed_us_states.join(population_us_states).reset_index()
    confirmed_us_states_normalized = confirmed_us_states_normalized.loc[:,
                                     ~confirmed_us_states_normalized.columns.duplicated()]
    confirmed_us_states_normalized = confirmed_us_states_normalized.T.drop_duplicates().T
    confirmed_us_states_normalized = confirmed_us_states_normalized.astype(
        {"cumulative_confirmed": int, "population": int, })
    confirmed_us_states.reset_index(level=0, inplace=True, drop=True)
    population_us_states.reset_index(level=0, inplace=True, drop=True)
    confirmed_us_states_normalized['confirmed_percent'] = confirmed_us_states_normalized['cumulative_confirmed'] / \
                                                          confirmed_us_states_normalized['population']
    print(confirmed_us_states_normalized)
    return confirmed_us_states_normalized


if __name__ == '__main__':
    # JHU data
    deaths_global_source = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/" \
                    "csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
    deaths_us_source = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/" \
                       "csse_covid_19_time_series/time_series_covid19_deaths_US.csv"
    confirmed_us_source = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/" \
                       "csse_covid_19_time_series/time_series_covid19_confirmed_US.csv"
    recovered_global_source= "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/" \
                             "csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
    confirmed_global_source="https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/" \
                            "csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
    recovered_global_df=recovered_globals(pd.read_csv(recovered_global_source))
    deaths_global_df = death_globals(pd.read_csv(deaths_global_source))
    confirmed_global_df=confirmed_globals(pd.read_csv(confirmed_global_source))
    deaths_us_df = deaths_us(pd.read_csv(deaths_us_source))
    deaths_us_df_latest = deaths_us_df[deaths_us_df['time_period'] == deaths_us_df['time_period'].max()]
    deaths_us_states_normalized = deaths_us_normalized(deaths_us_df_latest)

    #merging population column from death_us_df to confirmed_us_df
    def extract_and_marge(deaths_us_source,confirmed_us_source ):
        deaths_us_df_rd=pd.read_csv(deaths_us_source)
        deaths_us_df_rd.columns = map(str.lower, deaths_us_df_rd.columns)
        confirmed_us_df_rd=pd.read_csv(confirmed_us_source)
        confirmed_us_df_rd.columns = map(str.lower, confirmed_us_df_rd.columns)
        population_us_df_rd = deaths_us_df_rd.filter(
            ['population', 'province_state', 'country_region', 'lat', 'long_', 'admin2', 'uid'], axis=1)
        confirmed_us_df = pd.merge(confirmed_us_df_rd, population_us_df_rd,
                               on=['province_state', 'country_region', 'lat', 'long_', 'admin2', 'uid'],
                               how='inner')
        return confirmed_us_df
    confirmed_us_df = confirmed_us(extract_and_marge(deaths_us_source,confirmed_us_source))
    confirmed_us_states_normalized = confirmed_us_normalized(confirmed_us_df)

    # CDC data
    missing_values = ["NaN", "Missing", "Unknown", "NA", "nul", "null"]
    fields = ['age_group', 'sex', 'race', 'underlying_conditions_yn',
              'res_state', 'death_yn', 'hosp_yn', 'icu_yn', 'case_month']
    cdc_df = pd.read_csv('data/cdc_out.csv', skipinitialspace=True, usecols=fields,
                         na_values=missing_values, low_memory=False).dropna()

    # Write to SQL
    # print(write_to_sql(deaths_us_df, 'covid_viz_hub', 'deaths_us'))
    # print(write_to_sql(deaths_global_df, 'covid_viz_hub', 'deaths_global'))
    # print(write_to_sql(recovered_global_df, 'covid_viz_hub', 'recovered_global'))
    # print(write_to_sql(confirmed_global_df, 'covid_viz_hub', 'confirmed_global'))
    # print(write_to_sql(deaths_us_states_normalized, 'covid_viz_hub', 'deaths_us_normalized'))
    # print(write_to_sql(cdc_df, 'covid_viz_hub', 'cdc_out'))
    # print(write_to_sql(confirmed_us_df, 'covid_viz_hub', 'confirmed_us'))
    # print(write_to_sql(confirmed_us_states_normalized, 'covid_viz_hub', 'confirmed_us_normalized'))
