import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px


st.title("US Airlines Sentiments")
st.sidebar.title("US Airlines Sentiments")

st.markdown("This application is a streamlit dashboard to analyse the sentiments of the tweets about  US Airlines 🐦")
st.sidebar.markdown("This application is a streamlit dashboard to analyse the sentiments of the tweets about  US Airlines 🐦")

DATA_URL = "Tweets.csv"

@st.cache_data(persist=True)
def load_data():
    data = pd.read_csv(DATA_URL)
    data.tweet_created = pd.to_datetime(data.tweet_created)
    # data['lat'] = data['tweet_coord'].values[0]
    # data['long'] = data['tweet_coord'].values[1]
    # data[['latitude', 'longitude']] = pd.DataFrame(data['tweet_coord'].tolist(), index=data.index)
    return data

data = load_data()

# st.write(data)
st.sidebar.subheader(" Show random tweet")
random_tweet = st.sidebar.radio("Sentiment", data["airline_sentiment"].unique(), index=0)
st.sidebar.markdown(data.query('airline_sentiment == @random_tweet')['text'].sample(n=1).values[0])

if st.sidebar.checkbox("Show raw data", False):
    st.subheader('Raw data')
    st.write(data)

st.sidebar.markdown("### Number of tweets by sentiments")
select = st.sidebar.selectbox("Visualisation type", ["Histogram", "Pie"])
sentiment_count = data['airline_sentiment'].value_counts()
sentiment_count = pd.DataFrame({'Sentiment': sentiment_count.index, 'Tweets': sentiment_count.values})
# st.write(sentiment_count)

if not st.sidebar.checkbox("Hide", False):
    st.subheader('Number of tweets by sentiments')
    if select == "Histogram":
        fig = px.bar(sentiment_count, x='Sentiment', y='Tweets', color='Tweets', height=400)
        st.plotly_chart(fig)
    elif select == "Pie":
        fig = px.pie(sentiment_count, values='Tweets', names='Sentiment', height=400)
        st.plotly_chart(fig)

# st.map(data)
st.write(data.tweet_coord.values.to_list[820][0])