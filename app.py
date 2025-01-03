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

st.sidebar.subheader("When and where are the users tweeting from?")
hour = st.sidebar.slider("Hour of day", 0, 23)
modified_data = data[data['tweet_created'].dt.hour == hour]

if not st.sidebar.checkbox("Hide Map", False):
    st.markdown("### Tweets locations based on time of day")
    st.markdown(f"{len(modified_data)} tweets between {hour}:00 and {hour+1}:00")
    st.map(modified_data)

    if st.sidebar.checkbox("Show Tweets", False):
        st.write(modified_data[['tweet_created','text', 'lat', 'lon']])

st.sidebar.subheader("Breakdown airline by sentiment")
choice = st.sidebar.multiselect("Airline", data["airline"].unique())
if len(choice) > 0:
    filtered_data = data[data['airline'].isin(choice)]
    fig_choice = px.histogram(filtered_data, x='airline_sentiment', color='airline', histfunc='count', barmode='group', labels={'airline_sentiment':'Tweets'}, height=400)
    st.plotly_chart(fig_choice)