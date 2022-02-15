from datetime import datetime, timedelta
import pandas as pd
from tqdm import tqdm
import time

import alpaca_trade_api as tradeapi
from alpaca_trade_api.rest import REST, TimeFrame

def break_period_in_dates_list(start_date, end_date, days_per_step):
    '''Break period between start_date and end_date in steps of days_per_step days.'''
    step_start_date = start_date
    delta = timedelta(days=days_per_step)
    dates_list = []
    while end_date > (step_start_date + delta):
        dates_list.append((step_start_date, step_start_date + delta))
        step_start_date += delta
    dates_list.append((step_start_date, end_date))
    return dates_list


def format_timestep_list(timestep_list):
    '''Format dates in ISO format plus timezone. Note that first day starts at 00:00 and last day ends at 23:00hs.'''
    for i, d in enumerate(timestep_list):
        timestep_list[i] = (d[0].isoformat() + '-04:00', (d[1].isoformat().split('T')[0] + 'T23:00:00-04:00'))
    return timestep_list


def get_df_from_barset(barset):
    '''Create a Pandas Dataframe from a barset.'''
    df_rows = []
    for symbol, bar in barset.items():
        rows = bar.__dict__.get('_raw')
        for i, row in enumerate(rows):
            row['symbol'] = symbol
        df_rows.extend(rows)

    return pd.DataFrame(df_rows)


def download_data(aps, symbols, start_date, end_date, filename='data.csv'):
    '''Download data from REST manager for list of symbols, from start_date at 00:00hs to end_date at 23:00hs,
    and save it to filename as a csv file.'''
    timesteps = format_timestep_list(break_period_in_dates_list(start_date, end_date, 10))
    df = pd.DataFrame()

    for timestep in tqdm(timesteps):
        barset = aps.get_bars(symbols, '5Min', limit=1000, start=timestep[0], end=timestep[1])
        df = df.append(get_df_from_barset(barset))
        time.sleep(0.1)

    df.to_csv(filename)


# Call method.
# aps = tradeapi.REST(key_id='57ba0f433806ebb8cf74bbea8edad97f',
#                     secret_key='52c7f9f8e056d2882693ab3b1668055e9ffe2fc4',
#                     base_url='https://paper-api.alpaca.markets')

aps = tradeapi.REST(key_id='946be299bd81418abf78a6f27fff17e3',
                    secret_key='46b65e9e3a333529501a82e8f76853e6c122cd5b',
                    base_url='https://paper-api.alpaca.markets')
api = REST()
api.get_bars("AAPL", TimeFrame.Hour, "2021-06-08", "2021-06-08", adjustment='raw').df

download_data(aps=aps,
              symbols=['AAPL', 'GOOG'],
              start_date=datetime.strptime('01/01/20', '%d/%m/%y'),
              end_date=datetime.strptime('01/02/20', '%d/%m/%y'),
              filename='test.csv')