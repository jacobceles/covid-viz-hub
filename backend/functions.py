import pycountry
import pandas as pd
import pycountry_convert as pc

from sqlalchemy import create_engine


def rename_date_columns(df, ok_columns):
    """
    :param df: Input dataframe
    :param ok_columns: List of columns which are not dates
    :return: A dataframe which converts and groups the date columns to a month level
    """
    rename_columns = set(df.columns) - ok_columns
    for col in rename_columns:
        mm, dd, yy = col.split("/")
        new_name = '20' + yy + "-" + "{:02}".format(int(mm))
        df.rename(columns={col: new_name}, inplace=True)
    return df.groupby(df.columns, axis=1).sum()


def pivot_date_columns(df, ok_columns, value_name):
    """
    :param df: Input dataframe
    :param ok_columns: List of columns which are not dates
    :param value_name: Name of the value column
    :return: A dataframe
    """
    return df.melt(id_vars=ok_columns, var_name="time_period", value_name=value_name)


def get_cumulative_deaths(df, level_list):
    """
    :param df: Input dataframe
    :param level_list: List of columns on which the cumulative deaths are to be calculated
    :return: A dataframe
    """
    df['cumulative_deaths'] = df.groupby(level_list)['deaths'].cumsum()
    return df


def remove_unfit_countries(df, not_ok_countries):
    """
    :param df: Input dataframe
    :param not_ok_countries: List of columns which are to be removed
    :return: A dataframe
    """
    for country in not_ok_countries:
        df = df[(df['country/region'] != country)]
    return df


def remove_unfit_states(df, not_ok_states):
    """
    :param df: Input dataframe
    :param not_ok_states: List of states which are to be removed
    :return: A dataframe
    """
    for state in not_ok_states:
        df = df[(df['province_state'] != state)]
    return df


def remove_unfit_provinces(df, not_ok_provinces=None):
    """
    :param df: Input dataframe
    :param not_ok_provinces: List of provinces which are to be removed
    :return: A dataframe
    """
    df = df[df['admin2'] != 'Unassigned']
    if not_ok_provinces:
        for province in not_ok_provinces:
            df = df[(df['admin2'] != province)]
    return df


def clean_country_names(df, countries_mapper):
    """
    :param df: Input dataframe
    :param countries_mapper: Dictionary which maps countries to their standardized names
    :return: A dataframe
    """
    df['country/region'] = df['country/region'].replace(countries_mapper, inplace=False)
    return df


def clean_state_names(df, states_mapper):
    """
    :param df: Input dataframe
    :param states_mapper: Dictionary which maps states with their state code
    :return: A dataframe
    """
    df['state_code'] = df['province_state'].replace(states_mapper, inplace=False)
    return df


def get_country_iso_code_2(df):
    """
    :param df: Input dataframe
    :return: A dataframe with column 'iso_alpha_2' added which holds the iso country code for the respective country
    """
    df['iso_alpha_2'] = df['country/region'].apply(lambda country: pycountry.countries.get(name=country).alpha_2)
    return df


def get_country_iso_code_3(df):
    """
    :param df: Input dataframe
    :return: A dataframe with column 'iso_alpha_3' added which holds the iso country code for the respective country
    """
    df['iso_alpha_3'] = df['country/region'].apply(lambda country: pycountry.countries.get(name=country).alpha_3)
    return df


def get_country_continent(df):
    """
    :param df: Input dataframe with iso iso_alpha_2 value
    :return: A dataframe with column 'continent' added which holds the continent name for the respective country
    """
    continents = {
        'NA': 'North America',
        'SA': 'South America',
        'AS': 'Asia',
        'OC': 'Australia',
        'AF': 'Africa',
        'EU': 'Europe'
    }
    for index, row in df.iterrows():
        country_code = row['iso_alpha_2']
        if country_code == 'AQ':
            df.loc[index, 'continent'] = 'Antarctica'
        elif country_code == 'VA':
            df.loc[index, 'continent'] = 'Europe'
        elif country_code == 'TL':
            df.loc[index, 'continent'] = 'Asia'
        else:
            df.loc[index, 'continent'] = continents[pc.country_alpha2_to_continent_code(country_code)]
    return df


def write_to_sql(df, db_name, table_name):
    """
    :param df: Input dataframe
    :param db_name: Database name
    :param table_name: Table name
    :return: A dataframe
    """
    df.reset_index(level=0, drop=True, inplace=True)
    sql_engine = create_engine('mysql+pymysql://root:@127.0.0.1/{}'.format(db_name), pool_recycle=3600)
    db_connection = sql_engine.connect()
    try:
        df.to_sql(table_name, db_connection, if_exists='replace')
        db_connection.close()
        return "Table {} created successfully.".format(table_name)
    except Exception as e:
        db_connection.close()
        return "An error occurred: {}".format(e)


def read_from_sql(db_name, table_name):
    """
    :param db_name: Database name
    :param table_name: Table name
    :return: The table as a dataframe
    """
    sql_engine = create_engine('mysql+pymysql://root:@127.0.0.1', pool_recycle=3600)
    db_connection = sql_engine.connect()
    df = pd.read_sql("select * from {}.{}".format(db_name, table_name), db_connection)
    db_connection.close()
    return df
