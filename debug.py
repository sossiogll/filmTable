### Importing libraries
import datetime
import pandas as pd # https://pandas.pydata.org/docs/
import urllib



### Retrieving dataset
local_filename = 'assets/imdb_top_1000.csv'

def get_dataset():
    remote_url = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv'
    try:
        urllib.request.urlretrieve(remote_url, local_filename)
    except urllib.error.URLError as err:
        reason = err.reason

def load_dataset():
    #get_dataset()
    df = pd.read_csv(local_filename)
    df['Gross'] = df['Gross'].str.replace(',', '')
    df['Gross'] = df['Gross'].astype(float)
    df['Runtime'] = df['Runtime'].str.replace(' min', '')
    df['Runtime'] = df['Runtime'].astype(int)
    return df

df = load_dataset()
df = df.dropna(axis=1)


