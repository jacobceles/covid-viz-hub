import pycountry
import pandas as pd
import pycountry_convert as pc

from sqlalchemy import create_engine


def convert_columns_to_lowercase(df):
    """
    :param df: Input dataframe
    :return: Output dataframe with all column names in lowercase
    """
    df.columns = map(str.lower, df.columns)
    return df


def pivot_date_columns(df, ok_columns, value_name):
    """
    :param df: Input dataframe
    :param ok_columns: List of columns which are not dates
    :param value_name: Name of the value column
    :return: A dataframe
    """
    return df.melt(id_vars=ok_columns, var_name="time_period", value_name=value_name)


def replace_character_in_column_names(df, char_to_replace, char_to_replace_with):
    """
    :param df: Input dataframe
    :param char_to_replace: Character to be replaced
    :param char_to_replace_with: Character to be replaced with
    :return: Output dataframe with all characters in column names replaced
    """
    df.columns = df.columns.str.replace(char_to_replace, char_to_replace_with)
    return df


def delete_columns(df, column_names):
    """
    :param df: Input dataframe
    :param column_names: List of columns to be deleted as a list
    :return: Output dataframe with columns deleted
    """
    for col in column_names:
        del df[col]
    return df


def rename_date_columns(df, ok_columns, split_character):
    """
    :param df: Input dataframe
    :param ok_columns: Set of columns which are not dates
    :param split_character: Character based on which date is to be split
    :return: A dataframe with the date columns renamed
    """
    date_columns = set(df.columns) - ok_columns
    for col in date_columns:
        mm, dd, yy = col.split(split_character)
        new_name = ("{:02}/{:02}/20" + yy).format(int(mm), int(dd))
        df.rename(columns={col: new_name}, inplace=True)
    return df


def convert_to_month_wise_df(df, ok_columns, split_character):
    """
    for every row, for each month, put the greatest value of that month in the final column
    :param df: Input dataframe
    :param ok_columns: Set of columns which are not dates
    :param split_character: Character based on which date is to be split
    :return: A dataframe with only the month end date columns
    """
    date_columns = set(df.columns) - ok_columns
    for current_date in date_columns:
        mm, dd, yy = map(int, current_date.split(split_character))
        current_month_end_date = pd.Period(year=yy, month=mm, day=dd, freq='M').end_time.date().strftime('%m/%d/%Y')
        if current_date != current_month_end_date:
            del df[current_date]
        else:
            month_name = str(yy) + "-" + "{:02}".format(int(mm))
            df.rename(columns={current_date: month_name}, inplace=True)
    return df


def melt_columns_to_rows(df, ok_columns, var_name, value_name):
    """
    :param df: Input dataframe
    :param ok_columns: Set of columns which are not to be transformed
    :param var_name: Name of the new column variable after melting
    :param value_name: Name of the new column which holds the value after melting
    :return: A dataframe after melting multiple columns into just two columns
    """
    return df.melt(id_vars=ok_columns, var_name=var_name, value_name=value_name)


def unroll_cumulative_sum(df, non_str_columns, group_by_column):
    """
    :param df: Input dataframe
    :param non_str_columns: List of non string columns in dataframe
    :param group_by_column: List of columns based on which grouping should happen
    :return: Output dataframe with a new column after unrolling cumulative sum
    """
    unrolled_df = df[non_str_columns].groupby(group_by_column, as_index=False).diff().fillna(df)
    return pd.concat([df, unrolled_df], axis=1)


def remove_unfit_countries(df, not_ok_countries):
    """
    :param df: Input dataframe
    :param not_ok_countries: List of columns which are to be removed
    :return: A dataframe
    """
    for country in not_ok_countries:
        df = df[(df['country'] != country)]
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
    df['country'] = df['country'].replace(countries_mapper, inplace=False)
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
    df['iso_alpha_2'] = df['country'].apply(lambda country: pycountry.countries.get(name=country).alpha_2)
    return df


def get_country_iso_code_3(df):
    """
    :param df: Input dataframe
    :return: A dataframe with column 'iso_alpha_3' added which holds the iso country code for the respective country
    """
    df['iso_alpha_3'] = df['country'].apply(lambda country: pycountry.countries.get(name=country).alpha_3)
    return df


def get_cumulative_confirmed(df, level_list):
    """
    :param df: Input dataframe
    :param level_list: List of columns on which the cumulative deaths are to be calculated
    :return: A dataframe
    """
    df['cumulative_confirmed'] = df.groupby(level_list)['confirmed'].cumsum()
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
    sql_engine = create_engine('mysql+pymysql://root:@127.0.0.1/{}'.format(db_name), pool_recycle=3600)
    db_connection = sql_engine.connect()
    df = pd.read_sql("select * from {}.{}".format(db_name, table_name), db_connection)
    db_connection.close()
    return df


def racing_bar(df):
    covid = df[["time_period", "country", "Confirmed", "continent", "cumulative_confirmed"]]
    grouped = covid.groupby(['country', 'time_period'])
    covid_confirmed = grouped.sum().reset_index().sort_values(['time_period'], ascending=False)
    df = (
        covid_confirmed[covid_confirmed['Date'].eq("05/01/2021")].sort_values(by="Confirmed", ascending=False).head(10))
    return df
