import streamlit as st
import pandas as pd
import plotly.express as px
from faker import Faker

st.title("US Airlines Sentiments")
st.sidebar.title("US Airlines Sentiments")

st.markdown("This application is a streamlit dashboard to analyse the sentiments of the tweets about  US Airlines 🐦")
st.sidebar.markdown("This application is a streamlit dashboard to analyse the sentiments of the tweets about  US Airlines 🐦")

DATA_URL = "Tweets.csv"


def extract_lat_long(tweet_coord):
    if isinstance(tweet_coord, str) and ',' in tweet_coord:
        try:
            lat, long = tweet_coord.strip("[]").split(',')
            return float(lat.strip()), float(long.strip())
        except ValueError:
            return None, None
    return None, None


@st.cache_data(persist=True)
def load_data():
    faker = Faker()
    try:
        data = pd.read_csv(DATA_URL)
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        st.stop()
    data.tweet_created = pd.to_datetime(data.tweet_created)
    data['tweet_coord'] = data['tweet_coord'].apply(
        lambda x: x if pd.notnull(x) else f"[{faker.latitude()}, {faker.longitude()}]"
    )
    data[['lat', 'lon']] = pd.DataFrame(
        data['tweet_coord'].apply(extract_lat_long).tolist(),
        index=data.index
    )
    return data


data = load_data()

st.sidebar.subheader(" Show random tweet")
random_tweet = st.sidebar.radio("Sentiment", data["airline_sentiment"].unique(), index=0)
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')['text'].sample(n=1).values[0])

if st.sidebar.checkbox("Show raw data", False):
    st.write(data)

st.sidebar.markdown("### Number of tweets by sentiments")
select = st.sidebar.selectbox("Visualisation type", ["Histogram", "Pie"])
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment': sentiment_count.index, 'Tweets': sentiment_count.values})

if not st.sidebar.checkbox("Hide Graphics", False):
    st.subheader('Number of tweets by sentiments')
    if select == "Histogram":
        fig = px.bar(sentiment_count, x='Sentiment', y='Tweets', color='Tweets', height=400)
        st.plotly_chart(fig)
    elif select == "Pie":
        fig = px.pie(sentiment_count, values='Tweets', names='Sentiment', height=400)
        st.plotly_chart(fig)

if not st.sidebar.checkbox("Hide Map", False):
    st.map(data)