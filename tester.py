from faker import Faker

print(Faker().latitude())

@st.cache_data(persist=True)
def load_data():
    faker = Faker()

    # # Fonction pour générer des coordonnées localisées
    # def generate_localized_latlng():
    #     regions = {
    #         "France": {"lat": (41.0, 51.0), "lon": (-5.0, 8.0)},  # France métropolitaine
    #         "Senegal": {"lat": (12.0, 16.0), "lon": (-17.0, -11.0)},
    #         "US": {"lat": (25.0, 49.0), "lon": (-125.0, -66.0)},
    #         "Canada": {"lat": (42.0, 83.0), "lon": (-141.0, -52.0)},
    #         "China": {"lat": (18.0, 54.0), "lon": (73.0, 135.0)},
    #         "Australia": {"lat": (-44.0, -10.0), "lon": (113.0, 154.0)}
    #     }
    #     # Choisir un pays aléatoire
    #     selected_country = np.random.choice(list(regions.keys()))
    #     lat_range = regions[selected_country]['lat']
    #     lon_range = regions[selected_country]['lon']
    #     latitude = np.random.uniform(*lat_range)
    #     longitude = np.random.uniform(*lon_range)
    #     return latitude, longitude
    #
    # # Charger les données
    # try:
    #     data = pd.read_csv(DATA_URL)
    # except Exception as e:
    #     st.error(f"Failed to load data: {e}")
    #     st.stop()
    #
    # # Convertir la colonne date en datetime
    # data.tweet_created = pd.to_datetime(data.tweet_created)
    #
    # # Générer des coordonnées localisées pour les valeurs manquantes
    # data['tweet_coord'] = data['tweet_coord'].apply(
    #     lambda x: x if pd.notnull(x) else f"[{generate_localized_latlng()[0]}, {generate_localized_latlng()[1]}]"
    # )
    #
    # # Extraire les latitudes et longitudes
    # data[['lat', 'lon']] = pd.DataFrame(
    #     data['tweet_coord'].apply(extract_lat_long).tolist(),
    #     index=data.index
    # )
    #
    # return data
