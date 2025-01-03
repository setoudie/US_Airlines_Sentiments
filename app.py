import streamlit as st
import pandas as pd
import plotly.express as px
from faker import Faker
from wordcloud import wordcloud
import matplotlib.pyplot as plt

st.title("US Airlines Sentiments")
st.sidebar.title("US Airlines Sentiments")

st.markdown("This application is a streamlit dashboard to analyse the sentiments of the tweets about  US Airlines 🐦")
st.sidebar.markdown("This application is a streamlit dashboard to analyse the sentiments of the tweets about  US Airlines 🐦")

DATA_URL = "Tweets.csv"


def extract_lat_long(tweet_coord):
    """
    Extracts latitude and longitude from a string containing coordinates.

    This function processes a string representation of geographical coordinates in the
    format "[latitude,longitude]" and attempts to extract latitude and longitude values
    as floating-point numbers. If the input string is not in the correct format or if
    conversion to float fails, it returns None for both latitude and longitude.

    :param tweet_coord: A string representing geographical coordinates in the format
        "[latitude,longitude]".
    :type tweet_coord: str
    :return: A tuple containing latitude and longitude as floats if successfully parsed,
        or (None, None) if parsing or conversion fails.
    :rtype: tuple(float, float) | tuple(None, None)
    """
    if isinstance(tweet_coord, str) and ',' in tweet_coord:
        try:
            lat, long = tweet_coord.strip("[]").split(',')
            return float(lat.strip()), float(long.strip())
        except ValueError:
            return None, None
    return None, None


@st.cache_data(persist=True)
def load_data():
    """
    Loads and processes the tweet data from a pre-defined data source. The function attempts
    to read the data, convert specific columns, and enrich the data with geographical
    coordinates. If data loading fails, the operation is halted with an error message.

    :return: A pandas DataFrame containing the processed tweet data with added fields for
        'lat' (latitude) and 'lon' (longitude).
    :rtype: pandas.DataFrame

    :raises Exception: When the data source cannot be read, or an error occurs in processing.
    """
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


st.sidebar.subheader("What are the most common words?")
word_sentiment = st.sidebar.radio("Displays wordcloud for what sentiment?", data["airline_sentiment"].unique(), index=0)

# Constants for word cloud settings
WORDCLOUD_WIDTH = 800
WORDCLOUD_HEIGHT = 400
WORDCLOUD_RANDOM_STATE = 21
WORDCLOUD_MAX_FONT_SIZE = 119


def display_wordcloud(filtered_data, sentiment):
    """
    Generate and display a word cloud visualization for the text data corresponding
    to a specific sentiment. This function uses a combination of word frequency and
    visual aesthetics to create a graphical representation, offering insights into
    the common words associated with the provided sentiment data.

    :param filtered_data: Contains the filtered data frame with a 'text' column
        holding the text data. Ensure the data is pre-filtered for the desired
        sentiment before invoking this function.
    :type filtered_data: pandas.DataFrame
    :param sentiment: Specifies the sentiment category for which the word cloud
        is generated. It is used as contextual information for filtering or
        annotation purposes when interacting with the function.
    :type sentiment: str
    :return: None. The function renders a word cloud image directly into the
        Streamlit application interface using Matplotlib and Streamlit's
        rendering tools.
    :rtype: None
    """
    # Combine all text related to the sentiment
    wordcloud_data = filtered_data['text'].str.cat(sep=' ')

    # Generate the word cloud object
    wordcloud_object = wordcloud.WordCloud(
        width=WORDCLOUD_WIDTH,
        height=WORDCLOUD_HEIGHT,
        random_state=WORDCLOUD_RANDOM_STATE,
        max_font_size=WORDCLOUD_MAX_FONT_SIZE
    ).generate(wordcloud_data)

    # Create a figure and axes for Matplotlib
    fig, ax = plt.subplots()
    ax.imshow(wordcloud_object, interpolation="bilinear")
    ax.axis("off")

    # Display the plot using Streamlit
    st.pyplot(fig)


# Sidebar interaction
if st.sidebar.checkbox("Display Wordcloud", False):
    st.markdown(f"### Wordcloud for {word_sentiment}")
    filtered_data = data[data['airline_sentiment'] == word_sentiment]
    display_wordcloud(filtered_data, word_sentiment)
