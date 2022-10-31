### Importing libraries
import pandas as pd
import urllib
import streamlit as st


### Setting up webpage attributes
st.set_page_config(
    page_title="IMBd Dashboard",
    page_icon=":syringe:",
    layout="wide"
)


### Retrieving dataset
local_filename = 'assets/imdb_top_1000.csv'

def get_dataset():
    remote_url = 'https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-regioni/dpc-covid19-ita-regioni.csv'
    try:
        urllib.request.urlretrieve(remote_url, local_filename)
    except urllib.error.URLError as err:
        reason = err.reason
        st.error(f"Network error: {reason}")

# '@' denotes a decorator
@st.cache(suppress_st_warning=True)
def load_dataset():
    df = pd.read_csv(local_filename)
    df['Gross'] = df['Gross'].str.replace(',', '')
    df['Gross'] = df['Gross'].astype(float)
    df['Runtime'] = df['Runtime'].str.replace(' min', '')
    df['Runtime'] = df['Runtime'].astype(int)
    return df

def get_genre():
    genre_list = []
    temp = []
    temp = df['Genre'].tolist()
    for elem in temp:
        x = elem.split(',')
        for n in x:
            if n in genre_list:
                pass
            else:
                genre_list.append(n)
    genre_list = [x.strip(' ') for x in genre_list ]
    return genre_list

df = load_dataset()

df = df.drop('Poster_Link', axis=1)

### Filter sidebar
st.sidebar.header("Filtri")

films = st.sidebar.text_input(
    "Film Name"
)

actors = st.sidebar.text_input(
    "Actor Name"
)

start_date = st.sidebar.slider(
    "Start Year",
    min_value=min(df["Released_Year"]),
    max_value=max(df["Released_Year"]),
    value = min(df["Released_Year"])
)

end_date = st.sidebar.slider(
    "Ending Year",
    min_value=min(df["Released_Year"]),
    max_value=max(df["Released_Year"]),
    value=max(df["Released_Year"])
)

start_IMDB = st.sidebar.slider(
    "Minimum IMDb rating",
    min_value= min(df["IMDB_Rating"]),
    max_value=max(df["IMDB_Rating"]),
    value = min(df["IMDB_Rating"])
)

end_IMDB = st.sidebar.slider(
    "Maximum IMDb rating",
    min_value= min(df["IMDB_Rating"]),
    max_value=max(df["IMDB_Rating"]),
    value = max(df["IMDB_Rating"])
)

start_meta = st.sidebar.slider(
    "Minimum Metacritic rating",
    min_value = min(df["Meta_score"]),
    max_value = max(df["Meta_score"]),
    value = min(df["Meta_score"])
)

end_meta = st.sidebar.slider(
    "Maximum Metacritic rating",
    min_value = min(df["Meta_score"]),
    max_value = max(df["Meta_score"]),
    value = max(df["Meta_score"])
)

genre = st.sidebar.multiselect(
    'Genre',
    get_genre()
)

min_gross = st.sidebar.number_input(
    "Min Gross",
    min_value = 0.0,
    value = min(df['Gross']),
    step = 10000.0
)
max_gross = st.sidebar.number_input(
    "Max Gross",
    value=max(df['Gross']),
    step = 10000.0
)

###Filter dataframe
###base ed expr sono stati utilizzati per costruire delle espressioni regolari (RegEx) per filtrare
###i generi dei film. In particolare con questra espressione si cerca all'interno del dataframe una colonna che comprende
###contemporaneamente tutti gli elementi della lista 'genre'

base = r'^{}'
expr = '(?=.*{})'

df_filtered = df[
    (df["Released_Year"] >= start_date) &
    (df["Released_Year"] <= end_date) &
    (df["Series_Title"].str.contains(films,case=False)) &
    (df["Genre"].str.contains( base.format(''.join(expr.format(w) for w in genre)))) &
    ((df["Star1"].str.contains(actors,case=False)) |
     (df["Star2"].str.contains(actors,case=False)) |
     (df["Star3"].str.contains(actors,case=False)) |
     (df["Star4"].str.contains(actors,case=False))) &
    (df["IMDB_Rating"] >= start_IMDB) &
    (df["IMDB_Rating"] <= end_IMDB) &
    (df["Meta_score"] >= start_meta) &
    (df["Meta_score"] <= end_meta) &
    (df["Gross"] >= float(min_gross)) &
    (df["Gross"] <= float(max_gross))
    ]


### Title and last update section
#last_update = max(df["data"])

st.title("IMBd dashboard :camera:")
#st.text(f"Data ultimo aggiornamento: {last_update}")


### Showing dataset
st.dataframe(df_filtered)
